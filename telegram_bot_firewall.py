import subprocess
from github import Github
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from shutil import which


def project(update: Update, context: CallbackContext):
    update.message.reply_text("Redmine : http://64.227.73.149/redmine/\
                              \nGithub: https://github.com/alpha031/firewall/")


def is_tool(name):
    return which(name) is not None


def latest_commit(update, context):
    with open('git_token') as file:
        git_token = file.read()
        git_token = git_token.rstrip('\n')
        access = Github(git_token)
        branch = access.get_repo("RickardBremer/telegram-bot-firewall").get_branch("master")
        update.message.reply_text(branch.commit.sha)


def help_commands(update, context):
    help_commands = "Commands available :\n "
    commands = ["help", "fortune", "latest_commit", "project"]
    for item in commands:
        help_commands += item + "\n"
    update.message.reply_text(help_commands)


def fortune(update, context):
    if which('fortune'):
        fortune = subprocess.getoutput('fortune')
        update.message.reply_text(fortune)
    else:
        update.message.reply_text('Sorry, fortune not installd')


def main():
    with open('telegram_token') as file:
        telegram_token = file.read()
        telegram_token = telegram_token.rstrip('\n')
    updater = Updater(telegram_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('fortune', fortune))
    dp.add_handler(CommandHandler('latest_commit', latest_commit))
    dp.add_handler(CommandHandler('help', help_commands))
    dp.add_handler(CommandHandler('project', project))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
