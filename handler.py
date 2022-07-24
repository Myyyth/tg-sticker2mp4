import gzip
import os
import re
import shutil
import subprocess

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from config import dp
from state import StickerUpload


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Send me a lottie sticker and I\'ll convert it to .mp4')


@dp.message_handler(content_types=ContentType.STICKER)
async def convert(message: types.Message, state: FSMContext):
    if not message.sticker.is_animated:
        await message.answer('Not animated sticker (possibly just a video sticker, right click and save as .webm)')
        return

    lottie_fn = f'{message.from_id}.tgs'
    ungzip_fn = f'{message.from_id}.json'
    output_fn = f'{message.from_id}.mp4'

    await message.sticker.download(f'{message.from_id}.tgs')

    with gzip.open(lottie_fn, 'rb') as f_in:
        with open(ungzip_fn, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    await StickerUpload.color.set()

    async with state.proxy() as data:
        data['lottie_fn'] = lottie_fn
        data['ungzip_fn'] = ungzip_fn
        data['output_fn'] = output_fn

    await message.answer('Type color for a background in HEX (e.g. #42ECC4)')


@dp.message_handler(regexp=re.compile(r'^#(?:[0-9a-fA-F]{6})$'), state=StickerUpload.color)
async def color(message: types.Message, state: FSMContext):
    await message.answer('Rendering...')

    async with state.proxy() as data:
        subprocess.run(['puppeteer-lottie', '-i', data['ungzip_fn'], '-o', data['output_fn'], '-b', message.text])

        await message.answer_video(open(data['output_fn'], 'rb'))

        os.remove(data['lottie_fn'])
        os.remove(data['ungzip_fn'])
        os.remove(data['output_fn'])

    await state.finish()
