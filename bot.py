
import codecs
import compressor
import telebot
import requests
import site_parser

API_TOKEN = "388453697:AAF75xbYwSPxaz8eUUvVFTEIjS6QU5UWhGs"
bot = telebot.TeleBot(API_TOKEN)

command = 0


def command_status_compress(message):
    return command == 1


def command_status_decompress(message):
    return command == 2


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I can compress text files\n You can send me a document or link")


@bot.message_handler(commands=['compress'])
def compress(message):
    bot.send_message(message.chat.id, "Enter file or link to compress")
    global command
    command = 1


@bot.message_handler(commands=['decompress'])
def decompress(message):
    bot.send_message(message.chat.id, "Enter file to decompress")
    global command
    command = 2


@bot.message_handler(content_types=['document'], func=lambda x: command == 1 or command == 2)
def file_handler(message):
    try:
        global command
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))
        t = file.text
        with codecs.open("text_to_compress.txt", "w", encoding='utf-8') as input_file:
            input_file.write(t)
        if (command == 1):
            compressor.Compressor.compress_file("text_to_compress", "compressed_text")
            with codecs.open("compressed_text.txt", "r",  encoding='utf-8') as output_file:
                bot.send_document(message.chat.id, output_file)
        else:
            compressor.Compressor.decompress_file("text_to_compress", "decompressed_text")
            with codecs.open("decompressed_text.txt", "r", encoding="utf-8") as output_file:
                bot.send_document(message.chat.id, output_file)
        command = 0
    except:
        photo = open('maxresdefault.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(regexp='https?://[^ ]*$', func=lambda x: command == 1)
def link_handler(message):
    try:
        names = site_parser.retrieve_text(message.text)
        if len(names) == 0:
            bot.send_message(message.chat.id, "Nothing to compress")
        else:
            for name in names:
                compressor.Compressor.compress_file(name[:-4], name[:-4]+"compressed")
                with codecs.open(name[:-4]+"compressed.txt", "r", encoding='utf-8') as output_file:
                    bot.send_document(message.chat.id, output_file)
        command = 0
    except:
        bot.send_message(message.chat.id, "Cannot connect to the site. Try again")


@bot.message_handler(func=lambda x: command == 1)
def warn_message(message):
    bot.send_message(message.chat.id, "Enter correct file or link to compress")


@bot.message_handler(func=lambda x: command == 2)
def warn_message(message):
    bot.send_message(message.chat.id, "Enter correct file to decompress")


@bot.message_handler()
def warn_message(message):
    bot.send_message(message.chat.id, "Select the bot mode")



bot.polling()