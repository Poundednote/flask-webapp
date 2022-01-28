from flask import Flask, render_template
app = Flask(__name__)

gyms = [
    {
        'gym': 'AcademiaBjjLifestyle',
        'instructor': 'Lucio',
        'ranking': '5'
    },
    {
        'gym': 'Stealth BJJ',
        'instructor': 'Steve',
        'ranking': '5'
    }
]
        


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', gyms=gyms)

@app.route('/about')
def about():
    return '<h1>About us</h1>'
