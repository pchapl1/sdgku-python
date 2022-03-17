from flask import Flask, render_template

app = Flask('Server')


@app.route('/')
def index():
    return 'hello from flask'

@app.route('/me')
def about_me():
    return 'Phil Chaplin'


app.run(debug=True)