from flask import Flask, json, request, jsonify, render_template
import flask
from bson import json_util
from app import app
# from app import db
from flask_httpauth import HTTPTokenAuth
from .perguntas import functions
from .usuarios import user_functions
import base64
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "dmlhc29mdGNoYXZldG9rZW5zZWVkaW4yMDIx": "token_viasoft",
    "123": "bla",
}


@auth.verify_token
def verify_token(token):
    print(token)
    print(tokens)
    if token in tokens:
        return tokens[token]

@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@auth.login_required
def index():
    return render_template("chatbot.html")
    # return flask.jsonify(json.loads(json_util.dumps(db.chatbot.find({}).sort("_id", 1))))


@app.route('/perguntas', methods=['GET'])
@auth.login_required
def all():
    return flask.jsonify(json.loads(json_util.dumps(functions.perguntasAll())))


@app.route('/pergunta', methods=['POST'])
@auth.login_required
def getone():
    json_data = request.json
    if json_data is not None:
        code = json_data["code"]
        result = functions.pergunta(code)
        if result != False:
            return flask.jsonify(json.loads(json_util.dumps(result)))
        else:
            return False
    else:
        return False


@app.route('/perguntas', methods=['POST'])
@auth.login_required
def create():
    json_data = request.json
    # views.salvarNovo(json_data)
    if json_data is not None:
        code_relation = json_data["code_relation"]
        question = json_data["question"]
        answer = json_data["answer"]
        active = json_data["active"]
        result = functions.salvarNovo(code_relation, question, answer, active)
        if result != False:
            return jsonify(mensagem='pergunta criada')
        else:
            return jsonify(mensagem='pergunta não criada'), 404
    else:
        return jsonify(mensagem='pergunta não criada'), 404


@app.route("/chatbot", methods=['POST'])
def chatbot():
    json_data = request.json
    if json_data is not None:
        # db.chatbot.insert_one(json_data)
        code_user = json_data["code_user"]
        code_before = json_data["code_before"]
        question = json_data["question"]
        result = functions.questao(code_user, code_before, question)
        return result
    else:
        return jsonify(mensagem='pergunta não criada'), 404


@app.route("/perguntaDEL", methods=["POST"])
@auth.login_required
def delete():
    json_data = request.json
    if json_data is not None:
        code = json_data["code"]
        result = functions.salvarDelecao(code)
        if result == True:
            return flask.jsonify(json.loads(json_util.dumps({"result": result})))
        else:
            return jsonify(mensagem='pergunta não deletada')
    else:
        return flask.jsonify(json.loads(json_util.dumps({"result": False}))), 404


@app.route('/pergunta', methods=['PUT'])
@auth.login_required
def update():
    json_data = request.json
    if json_data is not None:
        code = json_data["code"]
        code_relation = json_data["code_relation"]
        question = json_data["question"]
        answer = json_data["answer"]
        active = json_data["active"]
        print(json_data)
        result = functions.salvarEdicao(
            code, code_relation, question, answer, active)
        if result != False:
            return flask.jsonify(json.loads(json_util.dumps({"result": result})))
        else:
            return flask.jsonify(json.loads(json_util.dumps({"result": False}))), 404
    else:
        return flask.jsonify(json.loads(json_util.dumps({"result": False}))), 404

# usuarios


@app.route('/registro', methods=['POST'])
def create_user():
    json_data = request.json
    # views.salvarNovo(json_data)
    if json_data is not None:
        email = str(json_data["email"])
        senha = json_data["senha"]
        if email.count('@') == 1 and email.count('.') >= 1:
            email = email.strip()
            if email[-1] == '.':
                email = email[0:-1]
            email = str(email.replace(',', '').replace(
                ';', '').replace('!', '').replace('"', '').replace("'", ''))
            result = user_functions.salvarNovo(
                email, senha)
            if result != False:
                return jsonify(mensagem='Usuario criado')
            else:
                return jsonify(mensagem='Usuario não criado'), 404
        else:
            return jsonify(mensagem='Usuario não criado'), 404
    else:
        return jsonify(mensagem='Usuario não criado'), 404


def getCODE():
    from datetime import datetime
    dataHora = datetime.now()
    code = str(dataHora.year)
    code += str(dataHora.month)
    code += str(dataHora.day)
    code += str(dataHora.hour)
    code += str(dataHora.minute)
    code += str(dataHora.second)
    code = str(int(round(int(code)/2, 0)))
    return code


@app.route('/login', methods=['POST'])
def login():
    json_data = request.json
    # views.salvarNovo(json_data)
    if json_data is not None:
        email = str(json_data["email"])
        senha = json_data["senha"]
        if email.count('@') == 1 and email.count('.') >= 1:
            email = email.strip()
            if email[-1] == '.':
                email = email[0:-1]
            email = str(email.replace(',', '').replace(
                ';', '').replace('!', '').replace('"', '').replace("'", ''))
            result = user_functions.entrar(
                email, senha)
            if result != False:
                # print(result)
                code = result[0].get('code')
                email = result[0].get('email')
                token = code+getCODE()+email
                token_bytes = token.encode('ascii')
                base64_bytes = base64.b64encode(token_bytes)
                base64_message = base64_bytes.decode('ascii')
                print(base64_message)
                tokens[token] = email
                print(tokens)
                return flask.jsonify(json.loads(json_util.dumps({"result": result, "token": token})))
            else:
                return jsonify(mensagem='Dados errados'), 404
        else:
            return jsonify(mensagem='Dados errados'), 404
    else:
        return jsonify(mensagem='Dados errados'), 404


@app.route('/validate', methods=['POST'])
@auth.login_required
def validate():
    json_data = request.json
    # views.salvarNovo(json_data)
    if json_data is not None:
        email = str(json_data["email"])
        id = json_data["id"]
        code = json_data["code"]
        if email.count('@') == 1 and email.count('.') >= 1:
            email = email.strip()
            if email[-1] == '.':
                email = email[0:-1]
            email = str(email.replace(',', '').replace(
                ';', '').replace('!', '').replace('"', '').replace("'", ''))
            result = user_functions.validate(
                email, id, code)
            if result != False:
                return flask.jsonify(json.loads(json_util.dumps({"result": result})))
            else:
                return jsonify(mensagem='Dados errados'), 404
        else:
            return jsonify(mensagem='Dados errados'), 404
    else:
        return jsonify(mensagem='Dados errados'), 404
