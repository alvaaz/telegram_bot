import handlers
import logging
import sys
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from config import (
  token, mode
)

logging.basicConfig(
  level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger()

updater = Updater(token=token, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", handlers.start))
dp.add_handler(CommandHandler("random", handlers.random_quote))
dp.add_handler(ConversationHandler(
  entry_points = [CommandHandler("new", handlers.start)],
  states={
    handlers.QUOTE: [
      MessageHandler(
          Filters.all, handlers.add_quote
      )
    ],
    handlers.MEDIA: [
      MessageHandler(Filters.photo, handlers.add_media)
    ]
  },
  fallbacks=[CommandHandler('cancel', handlers.cancel)],
  allow_reentry=True)
)

if mode == "dev":
  def run(updater):
    updater.start_polling()
    print("BOT LOAD")
    updater.idle()

elif mode == "prod":
  def run(updater):
    port = int(os.environ.get("PORT", "8443"))
    heroku_app_name = os.environ.get("HEROKU_APP_NAME")
    updater.start_webhook(
      listen="0.0.0.0",
      port=port,
      url_path=token,
      webhook_url=f"https://{heroku_app_name}.herokuapp.com/{token}"
    )

else:
  logger.info("No se especificó el mode")
  sys.exit(1)

run(updater)
