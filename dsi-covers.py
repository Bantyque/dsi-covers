#!/usr/bin/env python3
import sys
import getpass
import requests
import logging
from PIL import Image
from pathlib import Path
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)


def main():

    # Монтирование микросд и синхронизация обложек с ромами

    user = getpass.getuser()

    mounts = [
        Path(f'/media/{user}'),
        Path(f'/run/media/{user}'),
    ]

    base_folder = None
    marker_folder = "_nds/TWiLightMenu"

    for mount_base in mounts:
        if mount_base.exists():
            for drive in mount_base.iterdir():
                try:
                    if drive.is_dir():
                        if (drive / marker_folder).exists():
                            base_folder = drive
                            break
                except PermissionError:
                    continue
        if base_folder:
            break
    if not base_folder:
        tqdm.write('Флешка не найдена')
        sys.exit(0)
    tqdm.write('Флешка найдена')

    roms_folder = base_folder / 'roms' / 'nds'
    boxart_folder = base_folder / '_nds' / 'TWiLightMenu' / 'boxart'

    tqdm.write(f'Папка с играми найдена: {roms_folder}')
    tqdm.write(f'Папка с обложками найдена: {boxart_folder}')

    roms = {}
    for file in roms_folder.glob('*.nds'):
        with open(file, 'rb') as f:
            f.seek(12)
            game_id = f.read(4).decode('ascii')
        roms[file.stem] = {
            'id': game_id,
            'name': file.stem
        }

    boxart = {}
    for img in boxart_folder.glob('*.png'):
        clear_name = img.stem.replace('.nds', '')
        boxart[clear_name] = clear_name

    queue = {
        name: title
        for name, title in roms.items()
        if name not in boxart
    }
    tqdm.write(f'Нужно скачать - {len(queue)} обложек')
    if len(queue) == 0:
        tqdm.write('У тебя уже есть все обложки')
        sys.exit(0)


# Скачивание обложек с интернета

    for name, info in tqdm(
        queue.items(), desc='Скачивание обложек...', unit='g'
    ):
        game_id = info['id']
        regions = ['EN', 'EU', 'US', 'JA', 'KO']
        for reg in regions:
            roms_url = f'https://art.gametdb.com/ds/coverHQ/{
                reg}/{game_id}.jpg'
            response = requests.get(roms_url)

            if response.status_code == 200:
                tqdm.write(f'Обложка {info["name"]}, {reg} найдена ')
                save_path = boxart_folder / f'{name}.nds.png'
                with open(save_path, 'wb') as f_out:
                    f_out.write(response.content)

                with Image.open(save_path) as img:
                    resized_img = img.resize((128, 115))
                    resized_img.save(save_path)
                break
        else:
            tqdm.write(f'Обложка для {info["name"]} не найдена')


if __name__ == "__main__":
    main()
