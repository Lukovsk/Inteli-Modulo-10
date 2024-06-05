# Atividade Ponderada - Construção de Aplicativo Híbrido com Flutter

- O backend para está atividade deve, OBRIGATORIAMENTE, ser desenvolvido em Microsserviços. A aplicação deve ser desenvolvida utilizando o Flutter. Minha sugestão é que o backend seja desenvolvido em Python.

- A aplicação deve estar conteinerizada e deve ser entregue com o Dockerfile e o docker-compose.yml. O repositório da aplicação deve ser entregue com o README.md contendo as instruções para execução da aplicação.

## Entrega

- Aplicativo Flutter enviando as imagens para o processamento;
- Backend em Microsserviços que recebe as imagens e as processa, retornando o resultado para o aplicativo;
- Backend em Microsserviços que realiza o log das ações que o usuário realiza no aplicativo (por hora só login, criação de conta e envio de imagens);
- Serviço de notificação que envia uma notificação para o usuário quando o processamento da imagem termina.

## Estrutura de pastas

<pre><code>prog-3/backend/
│
├── gateway/
├── image_service/
├── log_service/
├── notify_service/
├── todo_service/
├── user_service/
├── .env
└── docker-compose.yaml</code></pre>

Onde:
```gateway/```: Diretório que possui a configuração do nginx como load balancer;
```image_service/```: Diretório que possui o microsserviço que cuida do processamento de imagens;
```log_service/```: Diretório que possui o microsserviço que cuida da emissão de logs;
```notify_service/```: Diretório que possui o microsserviço que notifica o aplicativo quando uma imagem é processada;
```todo_service/```: Diretório que possui o microsserviço que gerencia as tasks;
```user_service/```: Diretório que possui o microsserviço que gerencia os usuários (incluindo login);
```.env.example```: Arquivo .env de exemplo para o funcionamento da aplicação como um todo;
```docker-compose.yaml```: Arquivo yaml que dockeriza a aplicação como um todo;

## Como usar

Primeiro, certifique-se de possuir o [Docker](https://www.docker.com/) instalado.

Agora, com este repositório clonado, execute o comando abaixo:
<pre><code>docker compose up -d</code></pre>

Com isso, o servidor em microsserviços estará rodando em [http://localhost:80/](http://localhost:80/).

### Microsserviços

Aqui está uma breve explicação de como cada microsserviço funciona.

Inclusive, todos os microsserviços possuem uma estrutura básica:

- Utilizam [FastAPI](https://fastapi.tiangolo.com) como framework para backend, inicializado em um arquivo ``app.py``;
- Possuem um ``Dockerfile`` para o build do python em docker;
- Possuem um arquivo ``requirements.txt`` para a instalação das dependências necessárias apenas do microsserviço;

<pre> **_OBSERVAÇÃO:_** Algumas tecnologias citadas nos próximos tópicos podem _ainda_ não estar implementadas. Estou tendo alguns problemas com o SDK do flutter e não tenho espaço (no windows) para utilizar devidamente o docker. Por enquanto, vou colocar uma marcação _em itálico_ e, quando as implementar, atualizarei este **README.md** com as novas implementações. </pre>

#### Log service

O microsserviço de logs tem o propósito de registrar os logs das ações de cada outro microsserviço, garantindo o monitoramento desses serviços. Aqui, deve-se encontrar:

- [MongoDB](https://www.mongodb.com): Utilizei uma integração com o mongodb para o armazenamento dos logs de forma não relacional e desestruturada, permitindo o armazenamento de logs sem um schema específico. **_ainda não implementado_**
- Além disso, em todos os outros microsserviços, criei uma classe para efetuar os logs de forma consistente:

<code><pre>**LoggerClient**:

##### Descrição

`LoggerClient` é uma classe que facilita a criação e envio de logs para um servidor de logging.

##### Atributos

- `service` (str): Nome do serviço que está gerando os logs.
- `route` (str): Rota específica no servidor de logging para onde os logs serão enviados.
- `url` (str): URL do servidor de logging, obtida das variáveis de ambiente.
- `_serverOk` (bool): Indica se o servidor de logging está acessível.
- `_first_logged` (bool): Indica se o primeiro log (de inicialização) já foi enviado.

##### Métodos

###### `__init__(self, service: str, route: str)`

Inicializa a instância do LoggerClient.

**Args:**

- `service` (str): Nome do serviço que está gerando os logs.
- `route` (str): Rota específica no servidor de logging para onde os logs serão enviados.

###### `log(self, user_id: str, action: str, result: str = "Success", cause: str = None) -> None`

Cria e envia um log para o servidor. Envia um log de inicialização se for o primeiro log.

**Args:**

- `user_id` (str): Identificação do usuário responsável pelo log.
- `action` (str): Ação que está sendo logada.
- `result` (str, optional): Resultado da ação. Padrão é "Success".
- `cause` (str, optional): Causa do erro (se o resultado não for "Success"). Padrão é None.

###### `_first_log(self)`

Envia um log indicando que o logger foi iniciado.

###### `_request(self, log_entry: LogEntry)`

Faz uma requisição POST para o servidor de logging com a entrada de log fornecida.

**Args:**

- `log_entry` (LogEntry): A entrada de log a ser enviada.

**Returns:**

- `json`: Resposta do servidor de logging.

###### `_ping(self)`

Envia uma requisição de ping para verificar a disponibilidade do servidor de logging.

**Returns:**

- `dict`: Resposta do servidor de logging.

###### `_verify_server_ok(self) -> None`

Verifica se o servidor de logging está acessível e atualiza o estado interno.

</pre></code>

#### Image service

O microsserviço de image tem o propósito de processar imagens e armazená-las. Por enquanto, o único processamento existente nesse serviço é a remoção do background das imagens, utilizando uma biblioteca que facilita esses processo. As tecnologias utilizadas envolvem:

- [Supabase](https://supabase.com): O Supabase é um Firebase open source que permite o armazenamento de arquivos e a utilização de bancos de dados gratuitamente em nuvem. **_ainda não implementado_**
- [PostgreSQL](http://www.postgresql.org/): O Postgress é um banco de dados relacional muito utilizado no mercado. Aqui, ele vai permitir o armazenamento dos metadados das imagens, além da relação dessas imagens com o usuário. O Postgress estará na nuvem por meio do Supabase. **_ainda não implementado_**
- [RemBG](https://github.com/danielgatis/rembg): O Rembg é uma biblioteca de python que permite a remoção do background de imagens de forma simplificada.

Por fim, o image service faz uma requisição ao serviço de notificação para que o aplicativo seja notificado quando a imagem for processada (a imagem é processada utilizando o objecto ``BackgroundTasks`` do próprio ``FastAPI``).

#### Notify service

O microsserviço de notificação tem o propósito de enviar notificações aos aplicativos. **_Por enquanto, essa funcionalidade não está implementada pela atual dificuldade na utilização do Firebase_**. As tecnologias utilizadas envolvem:

- [Firebase](https://firebase.google.com/): O Firebase é um dos melhores serviços de cloud para aplicativos. Ele possui diversas funcionalidades extremamente úteis para o desenvolvimento mobile, incluindo autenticação, armazenamento e cloud messaging. **_ainda não implementado_**.

#### User e Todo services

Os microsserviços de usuário e tarefas são os mesmos descritos na [ponderada 1](https://github.com/Lukovsk/Inteli-Modulo-10/tree/main/ponderadas/prog-1), eles possuem os propósitos de gerenciamento e armazenamento de tarefas e usuários. Tecnologias utilizadas envolvem:

- [PostgreSQL](http://www.postgresql.org/)
- [Ormar](https://collerek.github.io/ormar/latest/): ORM assíncrona para python com suporte para PostgresSQL
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/): Biblioteca de python para utilização de JWT (Json web tokens) para fins de autenticação de usuário.

### Aplicativo mobile

O aplicativo mobile foi desenvolvido em [Flutter](https://flutter.dev/). Ainda estou com dificuldade na utilização do Firebase com SDK do flutter atual no meu computador. Ainda assim, o projeto será o mesmo desenvolvido na [ponderada 2](https://github.com/Lukovsk/Inteli-Modulo-10/tree/main/ponderadas/prog-2), com a adição de uma tela de perfil que permitirá a alteração da foto de perfil. Contudo, esse aprimoramento ainda está em desenvolvimento.

## Demonstração

https://github.com/Lukovsk/Inteli-Modulo-10/assets/99260684/4183fe75-b11b-49ca-9844-02e7325bfdd2


