from flask import Flask, render_template, request, redirect, url_for, session
import requests
import random

app = Flask(__name__)
app.secret_key = 'mysecretkey'

DATA_URL = "https://raw.githubusercontent.com/neelpatel05/periodic-table-api/refs/heads/master/data.json"

def fetch_elements():
    response = requests.get(DATA_URL)
    return response.json()

@app.route('/')
def index():
    try:
        elements = fetch_elements()
        return render_template('elements.html', elements=elements)
    except:
        return render_template('error.html')

@app.route('/element/<int:atomic_number>')
def element_detail(atomic_number):
    try:
        elements = fetch_elements()
        for element in elements:
            if element.get("atomicNumber") == atomic_number:
                return render_template('element.html', element=element)
        return render_template('error.html')
    except:
        return render_template('error.html')

@app.route('/game-web')
def start_game_web():
    try:
        elements = fetch_elements()
        element = random.choice(elements)
        session['name'] = element.get('name', '')
        session['symbol'] = element.get('symbol', '')
        session['atomicNumber'] = element.get('atomicNumber', 0)
        session['attempts'] = 0
        return render_template('game.html', hint=session['atomicNumber'])
    except:
        return render_template('error.html')

@app.route('/game/guess-web', methods=['POST'])
def guess_element_web():
    try:
        guess = request.form.get('guess', '').strip().lower()
        name = session.get('name', '').lower()
        symbol = session.get('symbol', '').lower()
        atomic_number = session.get('atomicNumber')
        session['attempts'] += 1

        if guess == name or guess == symbol:
            msg = f"Correct! It was {name.title()} ({symbol.upper()}). Attempts: {session['attempts']}"
            session.clear()
            return render_template('game.html', message=msg)
        else:
            return render_template('game.html', hint=atomic_number, message="Wrong guess. Try again!")
    except:
        return render_template('error.html')

# Optional: Show error.html for 500 Internal Server Errors
@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html'), 500

# Optional: Show error.html for page not found
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
