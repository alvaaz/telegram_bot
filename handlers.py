import logging
import cloudinary
from cloudinary.uploader import upload

from telegram import (
    ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext, ConversationHandler

from config import (
  api_key, api_secret, cloud_name, db
)

cloudinary.config(
  cloud_name=cloud_name,
  api_key=api_key,
  api_secret=api_secret
)

#Conf Logging
logging.basicConfig(
  level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger()

# Define options
QUOTE, MEDIA = range(2)

def random_quote(update, context: CallbackContext):
  quote_data = db.aggregate([{ "$sample": { "size": 1 } }])
  chat_id = update.effective_chat['id']
  logger.info(f"el usuario {chat_id} ha solicitado una frase")
  for quote in quote_data:
    context.bot.sendPhoto(chat_id = chat_id, photo = quote['media'], parse_mode="HTML", caption = f"<i>{quote['content']}</i>")

def start(update, context):
  logger.info(f"El usuario {update.effective_user['username']}, ha iniciado un proceso de creación")
  chat_id = update.effective_chat['id']
  context.bot.sendMessage(chat_id = chat_id, parse_mode="HTML", text="Ok, dame la frase de mierda (recuerda tener la imagen porque te la pediré acontinuación)")
  return QUOTE

def add_quote(update, context):
  logger.info(f"El usuario {update.effective_user['username']}, subió text")
  chat_id = update.effective_chat['id']
  context.bot.sendMessage(chat_id = chat_id, parse_mode="HTML", text="Estamos con la frase, pero me falta la imagen. Envíamela.")
  quote: str = update.message.text
  context.user_data['new_quote'] = quote
  return MEDIA

def add_media(update: Update, context: CallbackContext):
  logger.info(f"El usuario {update.effective_user['username']}, subió foto")
  quote = context.user_data["new_quote"]
  photo = context.bot.getFile(update.message.photo[-1].file_id)
  file_ = open("product_image", "wb")
  photo.download(out=file_)
  send_photo = upload("product_image", width=200, height=150, crop='thumb')
  record = {
    "content": quote,
    "media": send_photo["secure_url"]
  }

  # db.insert_one(record)
  # context.user_data.clear()
  # chat_id = update.effective_chat['id']
  # context.bot.sendMessage(chat_id = chat_id, parse_mode="HTML", text="Estamos listos! prueba con /random")
  # return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
  update.message.reply_text(
    'Adios.',
    reply_markup=ReplyKeyboardRemove()
  )
  return ConversationHandler.END
