import os
import telebot
import google.generativeai as genai

# Substitua pelos seus tokens
# COPIE E COLE EXATAMENTE ASSIM (COM AS ASPAS):

TELEGRAM_TOKEN = "8624351446:AAGa34_bzOYk40ys48fliHMLCP_za9Unyks"
GEMINI_API_KEY = "COLE_AQUI_SUA_CHAVE_DO_GEMINI_DENTRO_DAS_ASPAS"

# Configuração do Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Inicialização do Bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Eu sou um bot integrado ao Gemini. Como posso te ajudar hoje?")

@bot.message_handler(func=lambda m: True)
def chat_with_gemini(message):
    try:
        # Envia a mensagem do usuário para o Gemini
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Ops, tive um erro ao processar sua resposta.")

bot.infinity_polling()
