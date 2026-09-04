from datetime import datetime
from pathlib import Path
import asyncio

import aiofiles
import aiofiles.os
import aiohttp


BASE_DIR = Path(__file__).parent
CATS_DIR = BASE_DIR / 'cats'
URL = 'https://api.thecatapi.com/v1/images/search'

# Асинхронная функция для получения нового изображения.
async def get_new_image_url():
    # Создать асинхронную сессию для выполнения HTTP-запроса.
    async with aiohttp.ClientSession() as session:
        # Выполнить асинхронный GET-запрос на указанный URL.
        response = await session.get(URL)
        # Асинхронно получить тело ответа в формате JSON.
        data = await response.json()
        # Извлечь URL случайного изображения из ответа.
        random_cat = data[0]['url']
        # Вернуть URL изображения.
        return random_cat

# Асинхронная функция для загрузки файла по URL.
async def download_file(url):
    # Получить имя файла из URL. 
    filename = url.split('/')[-1] 
    # Создать асинхронную сессию для выполнения HTTP-запросов.
    async with aiohttp.ClientSession() as session:
        # Выполнить асинхронный GET-запрос по заданному URL.
        result = await session.get(url)
        # Открыть файл для записи в двоичном режиме.
        async with aiofiles.open(CATS_DIR / filename, 'wb') as f:
             # Прочитать содержимое ответа и записать его в файл.
            f.write(await result.read())

async def download_new_cat_image():
    url = await get_new_image_url()
    await download_file(url)

# Определить асинхронную функцию для создания директории.
async def create_dir(dir_name):
    # Асинхронно создать директорию.
    await aiofiles.os.makedirs(
        dir_name,  
        exist_ok=True 
    )

async def list_dir(dir_name):
    # Асинхронно получить список файлов и поддиректорий в указанной директории.
    files_and_dirs = await aiofiles.os.listdir(dir_name)
    # Напечатать каждый элемент содержимого директории, 
    # разделяя их переносом строки.
    print(*files_and_dirs, sep='\n') 

# Главная асинхронная функция.
async def main():
    await create_dir(CATS_DIR)
    # Создать список задач для асинхронного выполнения.
    tasks = [
        # Асинхронно выполнить функцию get_new_image_url() 100 раз.
        asyncio.ensure_future(download_new_cat_image()) for _ in range(100)
    ]
    # Подождать, пока выполнятся все задачи.
    await asyncio.wait(tasks)

# Точка входа в программу.
if __name__ == '__main__':
    # Записать текущее время начала выполнения программы.
    start_time = datetime.now()
    
    # Получить текущий событийный цикл.
    loop = asyncio.get_event_loop()
    # Запустить основную корутину и подождать, пока она завершится.
    loop.run_until_complete(main())
    
    # Записать текущее время окончания выполнения программы.
    end_time = datetime.now()
    # Напечатать время выполнения программы.
    print(f'Время выполнения программы: {end_time - start_time}.')

    # Запустить асинхронную функцию list_dir.
    asyncio.run(list_dir(CATS_DIR))