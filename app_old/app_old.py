from flask import Flask
from flask import request, jsonify
from flask_mongoengine import MongoEngine
import urllib.request, json

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'middleware',
    'host': 'db',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

@app.route('/report')
def report_by_country():
    country_arg = request.args.get('country')
    #print(country_arg)
    db_pbi = Pbi.objects(country=country_arg).first()
    db_presidente = President.objects(country=country_arg).first()
    #print(db_pbi)
    #print(db_presidente)
    feriados = get_holidays(country_arg)
    print(feriados)
    if not db_pbi or not db_presidente:
        return jsonify({'error': 'data not found'})
    else:
        report = Report(country_arg, db_pbi.valor, db_presidente.presidente, feriados)
        return jsonify(report.to_json())

def get_holidays(country):
    url = "https://date.nager.at/api/v2/publicholidays/2023/{}".format(country)

    response = urllib.request.urlopen(url)
    data = response.read()
    list_feriados = json.loads(data)
    feriados = []
    # print(len(list_feriados))
    for valores in list_feriados:
        feriados.append(Holiday(valores["date"], valores["localName"]).__dict__)

    return feriados

class Pbi(db.Document):
    country = db.StringField()
    valor = db.StringField()
    def to_json(self):
        return {"Country": self.country,
                "Valor": self.valor}

class President(db.Document):
    country = db.StringField()
    presidente = db.StringField()
    def to_json(self):
        return {"Country": self.country,
                "Presidente": self.presidente}

class Report:
    def __init__(self, country, pbi, presidente, feriados) -> None:
        self.country = country
        self.pbi = pbi
        self.presidente = presidente
        self.feriados = feriados
    def to_json(self):
        return {"Country": self.country,
                "PBI": self.pbi,
                "Presidente": self.presidente,
                "Feriados" : self.feriados}

class Holiday:
    def __init__(self, fecha, nombre):
        self.fecha = fecha
        self.nombre = nombre
    def to_json(self):
        return {"Fecha": self.fecha,
                "Nombre": self.nombre}


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=6100)

    