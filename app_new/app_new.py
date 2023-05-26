from flask import Flask, request, jsonify
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

class Pbi(db.Document):
    country = db.StringField()
    valor = db.StringField()

class President(db.Document):
    country = db.StringField()
    presidente = db.StringField()

@app.route('/president')
def get_president():
    country_arg = request.args.get('country')
    db_presidente = President.objects(country=country_arg).first()
    if not db_presidente:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(db_presidente.to_json())

@app.route('/pbi')
def get_pbi():
    country_arg = request.args.get('country')
    db_pbi = Pbi.objects(country=country_arg).first()
    if not db_pbi:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(db_pbi.to_json())

@app.route('/holidays')
def get_holidays():
    country_arg = request.args.get('country')
    url = "https://date.nager.at/api/v2/publicholidays/2023/{}".format(country_arg)
    response = urllib.request.urlopen(url)
    data = response.read()
    list_feriados = json.loads(data)
    feriados = [{"Fecha": feriado["date"], "Nombre": feriado["localName"]} for feriado in list_feriados]
    return jsonify(feriados)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=6100)