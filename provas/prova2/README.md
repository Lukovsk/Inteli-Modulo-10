# Prova 2 de Engenharia da Computação

## Enunciado

O que deve ser desenvolvido:

1. Realizar a adequação do projeto desenvolvido em Flask para FastAPI (até 1.0 ponto). ✅

2. Adicionar o log em todas as rotas do sistema. O log deve ficar armazenado em um arquivo. Logar apenas informações de nível WARNING em diante (até 3.0 pontos). ✅

3. Implementar o sistema em um container docker (até 1.0 ponto). ✅

4. Adicionar um container com um Gateway utilizando NGINX para o sistema (até 2.0 pontos). ✅

5. Criar um arquivo docker-compose que permita executar toda a aplicação (até 2.0 pontos). ✅

6. Implementar os testes da API com Postman (até 1.0 ponto).


## Executando a aplicação

### Sem o docker

Como essa aplicação se trata de um backend único, você pode simplesmente executar o arquivo `main.py` no diretório `app\` depois de instalar as dependências dele dentro de um ambiente virtual:

<code><pre>python -m venv venv
source venv/Scripts/activate
cd app/
python -m pip install -r requirements.txt
python main.py
</pre></code>

E o servidor estará executando no endereço [http://localhost:8001](http://localhost:8001).

### Usando o docker

Você também, com o Docker instalado, pode executar a aplicação como um todo em um contêiner, basta executar o `docker-compose` com o docker:

<code><pre>docker compose up -d</pre></code>