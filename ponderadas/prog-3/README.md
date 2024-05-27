# Atividade Ponderada - Construção de Aplicativo Híbrido com Flutter

- O backend para está atividade deve, OBRIGATORIAMENTE, ser desenvolvido em Microsserviços. A aplicação deve ser desenvolvida utilizando o Flutter. Minha sugestão é que o backend seja desenvolvido em Python.

- A aplicação deve estar conteinerizada e deve ser entregue com o Dockerfile e o docker-compose.yml. O repositório da aplicação deve ser entregue com o README.md contendo as instruções para execução da aplicação.

## Entrega

- Aplicativo Flutter enviando as imagens para o processamento;
- Backend em Microsserviços que recebe as imagens e as processa, retornando o resultado para o aplicativo;
- Backend em Microsserviços que realiza o log das ações que o usuário realiza no aplicativo (por hora só login, criação de conta e envio de imagens);
- Serviço de notificação que envia uma notificação para o usuário quando o processamento da imagem termina.
