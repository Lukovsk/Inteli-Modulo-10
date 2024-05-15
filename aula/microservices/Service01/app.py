# Service01/app.py

# Adicionando a funcionalidade de enviar mensagens com data e hora para o broker do RabbitMQ

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import pika

app = FastAPI()


class Message(BaseModel):
    date: datetime = None
    msg: str


# Cria uma função que faz o envio das mensagens para o RabbitMQ
def send_message_rabbitmq(msg: Message):
    # Verifica se as variáveis de ambiente estão definidas
    if "RABBITMQ_HOST" not in os.environ or "RABBITMQ_PORT" not in os.environ:
        raise Exception(
            "RABBITMQ_HOST and RABBITMQ_PORT must be defined in environment variables"
        )

    credentials = pika.PlainCredentials(
        os.environ["RABBITMQ_DEFAULT_USER"], os.environ["RABBITMQ_DEFAULT_PASS"]
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            os.environ["RABBITMQ_HOST"], os.environ["RABBITMQ_PORT"], "/", credentials
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=os.environ["RABBITMQ_QUEUE"])
    channel.basic_publish(
        exchange="",
        routing_key=os.environ["RABBITMQ_QUEUE"],
        body=f"{msg.date} - {msg.msg}",
    )
    connection.close()


@app.post("/ping")
async def ping(msg: Message):
    msg.date = datetime.now()
    send_message_rabbitmq(msg)
    return {"message": f"Created at {msg.date}", "content": f"{msg.msg}"}


# Executa a aplicação com a informação de HOST e PORTA enviados por argumentos
if __name__ == "__main__":
    import uvicorn
    import os

    print(os.environ)
    if "SERVICE_01_HOST" in os.environ and "SERVICE_01_PORT" in os.environ:
        uvicorn.run(
            app, host=os.environ["SERVICE_01_HOST"], port=os.environ["SERVICE_01_PORT"]
        )
    else:
        raise Exception("HOST and PORT must be defined in environment variables")
