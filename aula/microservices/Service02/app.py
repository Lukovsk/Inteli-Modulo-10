# Serviço 2 - recebe as mensagens via RabbitMQ e as armazena em um banco de dados em memória

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import pika
import os

app = FastAPI()
banco_em_memoria = []


class Message(BaseModel):
    date: datetime = None
    msg: str


# Cria uma função que recebe as mensagens para o RabbitMQ
def receive_message_rabbitmq():
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
    channel.queue_declare(queue=os.environ["RABBITMQ_QUEUE"], durable=True)
    channel.basic_consume(
        queue=os.environ["RABBITMQ_QUEUE"], on_message_callback=callback, auto_ack=True
    )
    channel.start_consuming()


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
    banco_em_memoria.append(body)


@app.get("/messages")
async def get_messages():
    return banco_em_memoria


# Executa a aplicação com a informação de HOST e PORTA enviados por argumentos
if __name__ == "__main__":
    import uvicorn
    import os

    print(os.environ)
    if "SERVICE_02_HOST" in os.environ and "SERVICE_02_PORT" in os.environ:
        receive_message_rabbitmq()
        uvicorn.run(
            app, host=os.environ["SERVICE_02_HOST"], port=os.environ["SERVICE_02_PORT"]
        )
    else:
        raise Exception("HOST and PORT must be defined in environment variables")
