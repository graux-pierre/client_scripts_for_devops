from flask import Flask

app = Flask(__name__)

@app.route('/commande')
def commande():
    return "{\"prix\": 2, \"banque\": \"127.0.0.1:4244\"}"

@app.route('/go')
def do_commande():
    return "{true}"

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=4242)
