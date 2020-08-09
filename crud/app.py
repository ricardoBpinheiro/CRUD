from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)  # cria o BD


class Pessoa(db.Model):
    __tablename__ = 'cliente'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    telefone = db.Column(db.String)
    cpf = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self, nome, telefone, cpf, email):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.email = email


db.create_all()


@app.route("/")  # Define uma rota
def index():
    return render_template("index.html")


@app.route("/cadastrar")  # Define rotas no site | Redireciona para a pagina cadastro.html
def cadastrar():
    return render_template("cadastro.html")


@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":  # Se a requisição for igual a POST
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        cpf = request.form.get("cpf")
        email = request.form.get("email")

        if nome and telefone and cpf and email:  # Se as informações forem passadas para o <form>
            p = Pessoa(nome, telefone, cpf, email)
            db.session.add(p)  # Adiciona as informações no Banco de dados
            db.session.commit()

    return redirect(url_for("index"))  # Depois cadastrar volta para a index


@app.route("/lista")
def lista():
    pessoas = Pessoa.query.all()  # Pega todas pessoas da lista
    return render_template("lista.html", pessoas=pessoas)  # Redireciona para lista.html


@app.route("/excluir/<int:id>")  # Deleta passando o ID
def excluir(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()  # Filtra as querys por ID
    db.session.delete(pessoa)  # Apaga a pessoa q achou pelo o id
    db.session.commit()

    # Depois que exclui o cliente, a pagina volta pra a pagina de listas so que com cliente excluido
    pessoas = Pessoa.query.all()
    return render_template("lista.html", pessoas=pessoas)


@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])  # atualiza passando o ID
def atualizar(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()  # Filtra as querys por ID

    if request.method == "POST":  # Se a requisição for igual a POST
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        cpf = request.form.get("cpf")
        email = request.form.get("email")

        if nome and telefone and cpf and email:  # Se as informações forem passadas para o <form>
            pessoa.nome = nome
            pessoa.telefone = telefone
            pessoa.cpf = cpf
            pessoa.email = email

            db.session.commit()

            return redirect(url_for("lista"))

    return render_template("atualizar.html", pessoa=pessoa)


if __name__ == "__main__":
    app.run(debug=True)  # Roda a aplicação



