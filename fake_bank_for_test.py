from flask import Flask

app = Flask(__name__)

@app.route('/paiement')
def commande():
    return "{true}"

@app.route('/extraction')
def do_commande():
    return '{"127.0.0.1:4242": {"compte": 10}, "127.0.0.1:4243": {"compte": 0}}'

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=4244)
