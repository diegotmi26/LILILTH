import os
import telebot
import google.generativeai as genai

# Configuração das chaves (usando variáveis de ambiente para segurança)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Inicializando Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Inicializando Bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá Diego! Bot online no Koyeb. Pode perguntar!")

@bot.message_handler(func=lambda m: True)
def chat(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    print("Bot iniciado...")
    bot.infinity_polling()
