import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- CONFIGURAÇÃO DAS CHAVES ---
# O Token do Telegram que você forneceu e a chave do Gemini
TELEGRAM_TOKEN = "8624351446:AAGa34_bzOYk40ys48fliHMLCP_za9Unyks"
GEMINI_API_KEY = "AIzaSyCu2admBo64LrbKwCyzKsW_2SF4pC1Ri3g" # <-- COLOQUE SUA CHAVE DO GOOGLE AQUI

# Configuração da Inteligência Artificial
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Inicialização do Bot do Telegram
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# --- SERVIDOR WEB (Para o Render manter o bot online) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot do Diego está Online!"

def run_flask():
    # O Render exige que o app escute em uma porta (geralmente 10000 ou definida pelo sistema)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- LÓGICA DE MENSAGENS DO TELEGRAM ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    texto_boas_vindas = (
        "Olá! 🤖\n\n"
        "Sou seu assistente inteligente integrado ao Gemini.\n"
        "Pode me enviar qualquer pergunta ou mensagem que eu responderei usando IA!"
    )
    bot.reply_to(message, texto_boas_vindas)

@bot.message_handler(func=lambda m: True)
def chat_with_gemini(message):
    try:
        # Mostra que o bot está "digitando..." para o usuário não achar que travou
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Envia a pergunta do Telegram para o Gemini
        response = model.generate_content(message.text)
        
        # Responde no Telegram com o texto gerado pela IA
        bot.reply_to(message, response.text)
        
    except Exception as e:
        print(f"Erro detalhado: {e}")
        bot.reply_to(message, "Desculpe, tive um problema ao processar isso agora. Tente novamente em instantes.")

# --- INICIALIZAÇÃO DO PROJETO ---
if __name__ == "__main__":
    # 1. Inicia o servidor web em segundo plano
    t = Thread(target=run_flask)
    t.start()
    
    # 2. Inicia o bot (Polling infinito)
    print("Bot iniciado com sucesso...")
    bot.infinity_polling()
