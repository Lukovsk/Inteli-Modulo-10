from flask import Flask
from db.db import db
from flask import render_template
from routes import user_app
from flask_jwt_extended import jwt_required, JWTManager


app = Flask(__name__, template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
app.config["JWT_SECRET_KEY"] = "goku-vs-vegeta"
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
jwt = JWTManager(app)

# Verifica se o parâmetro create_db foi passado na linha de comando
import sys

if len(sys.argv) > 1 and sys.argv[1] == "create_db":
    # cria o banco de dados
    with app.app_context():
        db.create_all()
    # Finaliza a execução do programa
    print("Database created successfully")
    sys.exit(0)

app.register_blueprint(user_app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/content", methods=["GET"])
@jwt_required()
def content():
    return render_template("content.html")


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)
