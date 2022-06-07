from flask import Flask, render_template
app = Flask(__name__, template_folder='templates/')

# secrets: client id 


@app.route('/')
def hello_world():
    return render_template('index.html')

# endpoint rewquest authgrant
# endpoint excahgne para pedir o access token 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003, debug=True)
