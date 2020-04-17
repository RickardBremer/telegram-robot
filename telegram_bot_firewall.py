import subprocess
from github import Github
from datetime import datetime, timedelta
from telegram.ext import Updater, CommandHandler


def project(bot, update):
    update.message.reply_text("Redmine : http://64.227.73.149/redmine/\nGithub: https://github.com/alpha031/firewall/")

def latest_commit(bot, update):
    with open('git_token') as file:
        git_token = file.read()
        git_token = git_token.rstrip('\n')
        access = Github(git_token)
        org = access.get_organization('alpha031')
        code = org.get_repo('firewall')
        since = datetime.now() - timedelta(days=1)
        commits = code.get_commits(since=since)
        update.message.reply_text(commits[0])


def help_commands(bot, update):
    help_commands = "Commands available : "
    commands = ["help", "fortune", "latest_commit", "project"]
    for item in commands:
        help_commands += item + " : "     
    update.message.reply_text(help_commands)


def fortune(bot, update):
    fortune = subprocess.getoutput('fortune')
    update.message.reply_text(fortune)


def main():
    with open('telegram_token') as file:
        telegram_token = file.read()
        telegram_token = telegram_token.rstrip('\n')
    updater = Updater(telegram_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('fortune', fortune))
    dp.add_handler(CommandHandler('latest_commit', latest_commit))
    dp.add_handler(CommandHandler('help', help_commands))
    dp.add_handler(CommandHandler('project', project))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
