import os
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Bot de Consulta de CEP*\n\n"
        "📮 Envie um CEP com 8 números.\n"
        "Exemplo:\n"
        "`01001000`",
        parse_mode="Markdown"
    )

async def buscar_cep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    cep = texto.replace("-", "")

    await update.message.reply_text("🔎 Buscando CEP...")

    if not cep.isdigit() or len(cep) != 8:
        await update.message.reply_text("❌ CEP inválido. Use 8 números.")
        return

    url = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        r = requests.get(url, timeout=5)
        dados = r.json()

        if "erro" in dados:
            await update.message.reply_text("❌ CEP não encontrado.")
            return

        msg = (
            "📍 *Endereço encontrado:*\n\n"
            f"🏠 Rua: {dados.get('logradouro', 'N/A')}\n"
            f"🏘 Bairro: {dados.get('bairro', 'N/A')}\n"
            f"🏙 Cidade: {dados.get('localidade', 'N/A')}\n"
            f"🗺 Estado: {dados.get('uf', 'N/A')}\n"
            f"📮 CEP: {dados.get('cep', cep)}"
        )

        await update.message.reply_text(msg, parse_mode="Markdown")

    except:
        await update.message.reply_text("⚠️ Erro ao consultar o CEP.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buscar_cep))
    print("🤖 Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
