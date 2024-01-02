# AmoCrm API Files downloader

## Установка

1. Клонируйте репозиторий
```
git clone https://github.com/CHRNVpy/AmoCrm_FilesDownloader.git
```
2. Перейдите в папку репозитория
```
cd AmoCrm_FilesDownloader
```
3. Создайте виртуальное окружение
```
python -m venv venv
```
4. Активируйте виртуальное окружение
#### Ubuntu
```
source venv/bin/activate
```
#### Windows
```
venv\Scripts\activate
```
3. Установите зависимости
```
pip install -r requirements.txt
```

## Использование

1. Создайте файл .env с вашими ключами по примеру .env_sample (можно использовать любой текстовый редактор для создания)
2. Запустите скрипт с флагом `-a` для авторизации
```
python amocrm.py -a
```
3. Запустите скрипт с флагом `-df --start 1 --stop 10` для начала загрузки файлов в диапазоне страниц 1 - 10, например
```
python amocrm.py -df --start 1 --stop 10
```

> [!Note]
> Если при запуске с флагом `-df` выходит ошибка, скорее всего истек access_token и нужно заново запустить скрипт с флагом `-a`