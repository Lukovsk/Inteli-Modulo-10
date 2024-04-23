# Atividade 1: Implementação de uma API 

## Enunciado

- Collections do Insomnia para testar a API
- YAML do OpenAPI (Swagger) para documentar a API
- Código fonte da API
- Instruções para executar a API

Obrigatóriamente ela deve ser uma API de grau de maturidade 2, ou seja, ela deve ser capaz de fazer a autenticação do usuário e permitir que ele crie, leia, atualize e delete tarefas. Você podem utilizar o código fornecido como base.

## Estrutura de pastas
<pre><code>prog-1/
│
├── app/
└── requirements.txt</code></pre>

Onde:
```app/```: Diretório que possui a api completa;
```requirements.txt```: Arquivo de texto com as dependências necessárias para executar a aplicação.

## Como usar
Primeiro, certifique-se de possuir o [Python](https://www.python.org/) instalado.

Agora, abra um ambiente virtual python executando o comando:
<pre><code>python -m venv venv</code></pre>

Instale as dependências neste diretório:
<pre><code>python -m pip install -r requirements.txt</code></pre>

Agora, com o servidor estará rodando em [http://localhost:5000/](http://localhost:5000/).

### Páginas
Existe uma página de [login](http://localhost:5000/login), [registro](http://localhost:5000/register) e o [conteúdo restrito](http://localhost:5000/content).
Em [http://localhost:5000/api](http://localhost:5000/api) você tem acesso à documentação da API para testá-la!

O projeto contem uma coleção do postman para testar a api, disponível em ``Ponderada 1.postman_collection.json``.