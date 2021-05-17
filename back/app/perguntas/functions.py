# from app import app
from app import db
# from bson.objectid import ObjectId
from unidecode import unidecode
import logging
from flask import render_template
from bson.objectid import ObjectId
logging.basicConfig(level=logging.INFO)


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


def salvarNovo(code_relation,question,answer,active):
    try:
        code = getCODE()
        code_user = "0"
        active = active
        code_relation = code_relation
        question = question
        answer = answer
        db.chatbot.insert_one(
            {"code": code,
             "code_user": code_user,
             "active": active,
             "code_relation": code_relation,
             "question": question,
             "answer": answer})
        return True
    except:
        return False

# nlp - processamento de linguagem natural


def questao(code_user, code_before, question):
    question = question.replace('%20', ' ')
    qTemp = question.lower()
    if code_before > 0:
        logging.info('1')
        consulta = db.chatbot.find(
            {"code_user": code_user, "code_relation": code_before,"active":1})

        if consulta.count() <= 0:
            logging.info('2')
            consulta = db.chatbot.find(
                {"code_user": code_user,"active":1})
    else:
        logging.info('3')
        consulta = db.chatbot.find({"code_user": code_user,"active":1})
        # print(list(consulta))
    logging.info(consulta.count())
    # inserção de resultados da captura
    lista = list()
    # controle de abreviações
    qTemp = qTemp.replace('vc', 'voce')
    qTemp = qTemp.replace('vcs', 'voces')
    qTemp = qTemp.replace('eh', 'e')
    qTemp = qTemp.replace('tb', 'tambem')
    qTemp = qTemp.replace('tbm', 'tambem')
    qTemp = qTemp.replace('oq', 'o que')
    qTemp = qTemp.replace('dq', 'de que')
    qTemp = qTemp.replace('td', 'tudo')
    qTemp = qTemp.replace('pq', 'por que')
    # cria uma lista com query da consulta
    if consulta.count() <= 0:
        lista.append({
            'code_current': 0,
            'code_user': code_user,
            'code_before': code_before,
            'question': question,
            'input': question,
            'output': 'Desculpe, mas não sei informar.'
        })
    else:
        for x in consulta:
            lista.append({
                'code_current': x.get('code'),
                'code_user': x.get('code_user'),
                'code_before': code_before,
                'question': x.get('question'),
                'input': question,
                'output': x.get('answer'),
            })

    # remove acentuação e espaços
    questao_recebida = unidecode(question)
    questao_recebida.replace('?', '')
    questao_recebida = questao_recebida.strip()
    # coloca em minúsculas
    questao_recebida = questao_recebida.lower()
    # elimina as três últimas letras de cada palavra com tokenização
    temp1 = questao_recebida.split(' ')
    temp2 = list()
    for x in temp1:
        if len(x) > 3:
            temp2.append(x[0:len(x)-3])
        else:
            temp2.append(x)
    questao_recebida = ' '.join(temp2)
    # percorre a lista de registros econtrados
    iguais = 0
    code = ''
    for x in lista:
        # remove acentuação e espaços
        questao_encontrada = unidecode(str(x['question']))
        questao_encontrada.replace('?', '')
        questao_encontrada = questao_encontrada.strip()
        # coloca em minúsculas
        questao_encontrada = questao_encontrada.lower()
        # elimina as três últimas letras de cada palavra com tokenização
        temp1 = questao_encontrada.split(' ')
        temp2 = list()
        for y in temp1:
            if len(y) > 3:
                temp2.append(y[0:len(y)-3])
            else:
                temp2.append(y)
        questao_encontrada = ' '.join(temp2)
        # cria uma lista para a questão recebida e uma para a questão encontrada
        qrList = questao_recebida.split(' ')
        qeList = questao_encontrada.split(' ')
        # conta as palavras recebidas que coincidem com as palavras de cada questão encontrada
        qtd = 0
        for y in qrList:
            if y in qeList:
                qtd += 1
        if qtd >= iguais:
            iguais = qtd
            code = x['code_current']
    if iguais == 0:
        code = 0
    # deixa na lista somente a resposta correspondente
    correspondente = list()
    for x in lista:
        if code == x['code_current']:
            correspondente.append(x)
            break
    lista = correspondente
    return {"lista": lista}


def api():
    return render_template("chatbot.html")

def salvarEdicao(code,code_relation,question,answer,active):
    if code is not None and db.chatbot.find_one({'code': code}) is not None:
        try:
            result = db.chatbot.update_one({'code': code}, {"$set": {'code_relation': code_relation, 'question': question,
                             'answer': answer, 'active': active}})
            return True
        except:
            return False
    else:
        return False
def salvarDelecao(code):
    try:
        result = db.chatbot.delete_one({'code': code})
        if(result.deleted_count > 0):
            return True
        else:
            return False
    except:
        return False

def perguntasAll():
    try:
        result = db.chatbot.find({}).sort("_id", 1)
        return result
    except:
        return False
def pergunta(code):
    try:
        result = db.chatbot.find_one({'code': code})
        return result
    except:
        return False
