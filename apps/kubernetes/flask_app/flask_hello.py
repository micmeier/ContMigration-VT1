from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def query():
    return 'The answer is 42 \n'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')


