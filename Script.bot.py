from twilio.rest import Client
from flask import Flask, request, jsonify
import openai

# Configurar sua chave da API da OpenAI
openai.api_key = " "

# Configurar credenciais do Twilio (obtenha-as em https://www.twilio.com/console)
TWILIO_ACCOUNT_SID = " "
TWILIO_AUTH_TOKEN = " "
TWILIO_PHONE_NUMBER = " "  # Deve ser um número Twilio

# Inicializar o cliente do Twilio
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Inicializar o aplicativo Flask
app = Flask(__name__)

# Rota para receber mensagens do WhatsApp
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_message = request.values.get("Body", "").lower()
    sender_number = request.values.get("From", "")

    # Processar a mensagem usando a OpenAI
    response = openai.Completion.create(
        engine="davinci",  # Use o mecanismo "davinci" da OpenAI
        prompt=incoming_message,
        max_tokens=50  # Limite o tamanho da resposta, se necessário
    )

    bot_response = response.choices[0].text

    # Enviar a resposta via WhatsApp
    client.messages.create(
        body=bot_response,
        from_=TWILIO_PHONE_NUMBER,
        to=sender_number
    )

    return "", 200

if __name__ == "__main__":
    app.run(debug=True)
