#!/usr/bin/env python3
"""
DesgraficBot - Um bot do Telegram em português
"""

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Ativar logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Silenciar logs chatos do httpx
logging.getLogger("httpx").setLevel(logging.WARNING)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    user = update.effective_user
    if user:
        await update.message.reply_html(
            f"Oi {user.mention_html()}! Bem-vindo(a) ao *DesgraficBot*! 🤖\n\n"
            f"Tô pronto pra te ajudar. Use /ajuda pra ver os comandos."
        )
    else:
        await update.message.reply_text("Oi! Bem-vindo(a) ao DesgraficBot! 🤖")


async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    help_text = """
🤖 *Comandos disponíveis:*

/start - Inicia o bot
/ajuda - Mostra esta mensagem
/sobre - Fala sobre o bot

Manda qualquer mensagem que eu repito pra você!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def sobre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    about_text = """
🤖 *Sobre o DesgraficBot*

Um bot feito em Python com a biblioteca `python-telegram-bot`.  
Criado com ❤️ e umas boas doses de paciência.
    """
    await update.message.reply_text(about_text, parse_mode='Markdown')


async def eco(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    await update.message.reply_text(f"Você disse: {update.message.text}")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Erro ao lidar com update:", exc_info=context.error)


def main() -> None:
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("A variável TELEGRAM_BOT_TOKEN não foi configurada!")
        return
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ajuda", ajuda))
    application.add_handler(CommandHandler("sobre", sobre))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, eco))
    application.add_error_handler(error_handler)
    logger.info("Iniciando DesgraficBot...")
    application.run_polling()


if __name__ == '__main__':
    main()
