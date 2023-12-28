# AmoCrm API Files downloader

## Установка

1. Клонируйте репозиторий
```commandline
git clone https://github.com/CHRNVpy/AmoCrm_FilesDownloader.git
```
2. Перейдите в папку репозитория
```commandline
cd AmoCrm_FilesDownloader
```
3. Создайте виртуальное окружение
```commandline
python -m venv venv
```
4. Активируйте виртуальное окружение
#### Ubuntu
```commandline
source venv/bin/activate
```
#### Windows
```commandline
venv\Scripts\activate
```
3. Установите зависимости
```commandline
pip install -r requirements.txt
```

## Использование

1. Создайте файл .env с вашими ключами по примеру .env_sample (можно использовать любой текстовый редактор для создания)
2. Запустите скрипт с флагом "-a" для авторизации
```commandline
python amocrm.py -a
```
3. Запустите скрипт с флагом "-df --start 1 --stop 10" для начала загрузки файлов в диапазоне страниц 1 - 10, например
```commandline
python amocrm.py -df --start 1 --stop 10
```

#### Note: Если при запуске с флагом "-df" выходит ошибка, скорее всего истек access_token и нужно заново запустить скрипт с флагом "-a"