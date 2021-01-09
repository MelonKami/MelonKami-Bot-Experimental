import codecs, json
from termcolor import colored
from os import path

class Config():
    def __init__(self):
        if path.exists('config.json') == False:
            print(colored("First Launch mode: \nHello, welcome to the bot's setup. To get started with the bot, you need to input your token", "green"))
            print()
            input_token = input("Token: ")
            print()
            print()

            with open('config.json', 'x') as File:
                json.dump({"token": input_token, "guilds": {}}, File, indent=4)

        with codecs.open('config.json','r', encoding='utf-8-sig') as File:
            self.config = json.load(File)
        self.token = self.config["token"]

    def hello_world(self):
            print("Hello World")

    def save_config(self):
            with codecs.open('config.json', 'w', encoding='utf8') as File:
                json.dump(self.config, File, sort_keys=True, indent=4, ensure_ascii=False)
