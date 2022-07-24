# sticker2mp4
Simple telegram bot to convert lottie stickers to mp4. Available at [@sticker2mp4](http://t.me/sticker2mp4_bot)

## Prerequisites
* [Python 3.10](https://www.python.org/)
* [Pipenv](https://pipenv.pypa.io/en/latest/)
* [puppeteer-lottie-cli](https://github.com/transitive-bullshit/puppeteer-lottie-cli)

## Running
Copy **.env.example** to **.env**
```cp .env.example .env```
Modify **.env** and enter your Telegram bot token
Install dependencies
```pipenv install```
Run bot
```pipenv run python main.py```
