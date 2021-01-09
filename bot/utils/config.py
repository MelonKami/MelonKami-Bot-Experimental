import codecs, json
from termcolor import colored
from os import path

class Config():
  def __init__(self):
    if path.exists('config.json') == False:
      print(colored("Hello, welcome to the bot's setup. To get started with the bot, you need to input your token and prefix", "green"))
      print()
      input_token = input("Token: ")
      input_prefix = input("Prefix: ")
      print()
      print()

      with open('config.json', 'x') as File:
        json.dump({"token": input_token, "prefix": input_prefix}, File, indent=4)

    with codecs.open('config.json','r', encoding='utf-8-sig') as File:
      self.config = json.load(File)

  def token(self):
    return self.config["token"]

  def hello_world(self):
    print("Hello World")

  def change_value(self, value, change):
    self.config[value] = change

  def save_config(self):
    with codecs.open('config.json', 'w', encoding='utf8') as File:
        json.dump(self.config, File, sort_keys=True, indent=4, ensure_ascii=False)
