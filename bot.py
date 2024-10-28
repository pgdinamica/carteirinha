#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import io

from PIL import Image

from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, InputFile, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
from reportlab.lib.utils import ImageReader

from card import make_carteirinha
from preprocess import process_input, limit_img_size, crop_circle

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Olá, este o bot do Programação Dinâmica! Use o comando /help para descobrir todas as funcionalidades",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""

    answer = """Comandos:\n
    digite /carteirinha <nome> <username_youtube> <ano_que_virou_fã>
    """
    await update.message.reply_text(answer)


async def unknown(update: Update, 
                  context: ContextTypes.DEFAULT_TYPE) -> None:
    """Resposta para quando o bot não sabe o que fazer."""

    answer = """Não entendi, mas você pode se inscrever no canal Programação Dinâmica e aprender sobre programação, ciência de dados e inteligência artificial com o Hallison e com a Kizzy!"""

    await update.message.reply_text(answer)
    

async def membercard(update: Update, 
                     context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Por favor, informe seu nome, username do Youtube e ano em que se tornou fã do canal.")
        return
    user_info = process_input(context.args)
    context.user_data['user_info'] = user_info

    await update.message.reply_text("Dados recebidos! Pode enviar a foto 📸")

async def handle_photo(update: Update, 
                       context: ContextTypes.DEFAULT_TYPE):
    # recuperar os dados do usuário
    # Retrieve the overlay text
    user_info = context.user_data.get('user_info')
    if not user_info:
        await update.message.reply_text("Por favor, use o comando /carteirinha para enviar seus dados.")
        return
    # recuperar a foto da mensagem
    photo = update.message.photo[-1]
    photo_file = await photo.get_file()
    image_stream = io.BytesIO()
    await photo_file.download_to_memory(out=image_stream)
    image_stream.seek(0)

    # processar a imagem
    img = Image.open(image_stream)
    # reduzir o tamanho para no máximo 1024 x 1024
    img = limit_img_size(img)
    # cortar de forma circular
    img = crop_circle(img)
    # fazer a carteirinha
    output_stream = io.BytesIO()
    make_carteirinha(user_info, 
                     ImageReader(img), 
                     output_stream)
    # enviar a carteirinha como resposta
    await update.message.reply_document(
        InputFile(output_stream, "carteirinha.pdf"))


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    with open("token.txt") as tokenfile:
        token = tokenfile.read().strip()
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        CommandHandler("carteirinha", membercard))
    application.add_handler(
        MessageHandler(filters.PHOTO, handle_photo))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()