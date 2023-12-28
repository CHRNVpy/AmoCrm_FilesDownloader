import argparse
import asyncio
import json
import os
import time
from pprint import pprint

import aiohttp
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('client_id')
CLIENT_SECRET = os.getenv('client_secret')
CODE = os.getenv('code')
REDIRECT_URI = os.getenv('redirect_uri')
AMOCRM_SUBDOMAIN = os.getenv('subdomain')


class AmoCrm:

    def authorize(self):
        headers = {
            'Content-Type': 'application/json',
        }

        if not os.path.exists('amocrm.json'):

            json_data = {
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'grant_type': 'authorization_code',
                'code': CODE,
                'redirect_uri': REDIRECT_URI,
            }
            print('Creating access token')

        else:

            with open('amocrm.json', 'r') as access_file:
                token = json.load(access_file)

            json_data = {
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'grant_type': 'refresh_token',
                'refresh_token': token['refresh_token'],
                'redirect_uri': REDIRECT_URI,
            }
            print('Updating access token')

        response = requests.post(f'https://{AMOCRM_SUBDOMAIN}.amocrm.ru/oauth2/access_token',
                                 headers=headers,
                                 json=json_data)
        print(response.json())
        with open('amocrm.json', 'w') as json_file:
            json.dump(response.json(), json_file, indent=2)

    def get_files_url(self):
        if os.path.exists('amocrm.json'):
            with open('amocrm.json', 'r') as file:
                token = json.load(file)
        # pprint(token['access_token'])
        access_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token["access_token"]}'
        }

        params = {
            'with': 'drive_url'
        }

        # get files url
        setup = requests.get(f'https://{AMOCRM_SUBDOMAIN}.amocrm.ru/api/v4/account', headers=access_headers,
                             params=params)
        # print(setup.json())
        return setup.json()['drive_url']

    def get_files(self, page):
        if os.path.exists('amocrm.json'):
            with open('amocrm.json', 'r') as file:
                token = json.load(file)
        # pprint(token['access_token'])
        access_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token["access_token"]}'
        }
        # get files
        base_url = self.get_files_url()
        files = requests.get(f'{base_url}/v1.0/files?limit=50&page={str(page)}', headers=access_headers)
        # pprint(files.json())
        return files.json()

    def get_entity(self, file_uuid):
        if os.path.exists('amocrm.json'):
            with open('amocrm.json', 'r') as file:
                token = json.load(file)
        # pprint(token['access_token'])
        access_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token["access_token"]}'
        }
        # get entity
        entity = requests.get(f'https://{AMOCRM_SUBDOMAIN}.amocrm.ru/api/v4/files/{file_uuid}/links',
                              headers=access_headers)
        # pprint(entity.json())
        return entity.json()

    def get_files_list(self, page):
        files = []
        print(f'Searching files for page {page}')
        all_files = self.get_files(page)
        for file in all_files['_embedded']['files']:
            info = {}
            file_link = file['_links']['download']['href']
            info['file_link'] = file_link
            file_uuid = file['uuid']
            entity_info = self.get_entity(file_uuid)
            # pprint(entity_info)
            if entity_info['entities']:
                entities = [{'entity_type': item['entity_type'], 'entity_id': item['id']} for item in
                            entity_info['entities']]
            else:
                entities = [{'entity_type': 'None', 'entity_id': 'None'}]
            info['entities'] = entities
            files.append(info)
        return files

    def download_files(self, page):
        files = self.get_files_list(page)
        base_folder = "downloads"

        for entry in files:
            entities = entry.get('entities', [])
            file_link = entry.get('file_link', '')

            if entities and file_link:
                entity_type = entities[0].get('entity_type', '')
                entity_id = entities[0].get('entity_id', '')

                if entity_type and entity_id:
                    # Create folders if they don't exist
                    entity_folder = os.path.join(base_folder, entity_type, str(entity_id))
                    os.makedirs(entity_folder, exist_ok=True)

                    # Extract file name from the URL
                    file_name = os.path.basename(file_link.split('?')[0])

                    # Download the file
                    response = requests.get(file_link)
                    file_path = os.path.join(entity_folder, file_name)

                    # Save the file locally
                    with open(file_path, 'wb') as file:
                        file.write(response.content)

                    print(f"File saved to: {file_path}")

    async def download_file(self, entry, base_folder):
        entities = entry.get('entities', [])
        file_link = entry.get('file_link', '')

        if entities and file_link:
            entity_type = entities[0].get('entity_type', '')
            entity_id = entities[0].get('entity_id', '')

            if entity_type and entity_id:
                # Create folders if they don't exist
                entity_folder = os.path.join(base_folder, entity_type, str(entity_id))
                os.makedirs(entity_folder, exist_ok=True)

                # Extract file name from the URL
                file_name = os.path.basename(file_link.split('?')[0])

                # Download the file asynchronously
                async with aiohttp.ClientSession() as session:
                    async with session.get(file_link) as response:
                        file_path = os.path.join(entity_folder, file_name)

                        # Save the file locally
                        with open(file_path, 'wb') as file:
                            file.write(await response.read())

                        print(f"File saved to: {file_path}")

    async def download_files_async(self, page):
        files = self.get_files_list(page)
        base_folder = "downloads"

        tasks = [self.download_file(entry, base_folder) for entry in files]

        # Run the tasks asynchronously
        await asyncio.gather(*tasks)


def main():
    parser = argparse.ArgumentParser(description='AmoCrm Files Downloader')
    parser.add_argument('-a', action='store_true', help='Authorize')
    parser.add_argument('-df', action='store_true', help='Download files')
    parser.add_argument('--start', type=int, default=1, help='Start range for file download')
    parser.add_argument('--stop', type=int, default=200, help='Stop range for file download')

    args = parser.parse_args()

    crm_worker = AmoCrm()

    if args.a:
        crm_worker.authorize()

    if args.df:
        start_range = args.start
        stop_range = args.stop

        for i in range(start_range, stop_range + 1):
            asyncio.run(crm_worker.download_files_async(i))


if __name__ == '__main__':
    main()
