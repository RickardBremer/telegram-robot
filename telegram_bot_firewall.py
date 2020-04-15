import re
from telegram.ext import Updater, CommandHandler
import requests
import subprocess

def get_url():
    contents = requests.get('https://random.dog/woof.json').json() 
    url = contents['url']
    return url


def get_image_url():
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


def bop(bot, update):
    url = get_image_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

def fortune(bot, update):
    fortune = subprocess.getoutput('fortune')
    update.message.reply_text(fortune)
    
def main():
    updater = Updater('1244083311:AAHpqDOv38tDtgm7IRAaHQRYtGsHZeukB8E')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop', bop))
    dp.add_handler(CommandHandler('fortune', fortune))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
