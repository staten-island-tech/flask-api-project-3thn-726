from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

DATA_URL = "https://raw.githubusercontent.com/neelpatel05/periodic-table-api/refs/heads/master/data.json"

def fetch_elements():                          #serves as a database
    response = requests.get(DATA_URL)
    return response.json()

@app.route('/')
def index():
    try:
        elements = fetch_elements()                                        #elements becomes the database
        return render_template('elements.html', elements=elements)
    except:
        return render_template('error.html')

@app.route('/element/<int:atomic_number>')     #creates a page for each element and organizes it based on the elements periodic table
def element_detail(atomic_number):
    try:
        elements = fetch_elements()
        for element in elements:
            if element.get("atomicNumber") == atomic_number:              
                return render_template('element.html', element=element) #references the code in element.html to create the page for the element
        return render_template('error.html')
    except:
        return render_template('error.html')

@app.route('/game-web')
def start_game_web():
    try:
        elements = fetch_elements()
        element = random.choice(elements)
        return render_template('game.html', hint=element['atomicNumber'], answer_name=element['name'], answer_symbol=element['symbol'])
    except:
        return render_template('error.html')

@app.route('/game/guess-web', methods=['POST'])
def guess_element_web():
    try:
        guess = request.form.get('guess', '').strip().lower()
        answer_name = request.form.get('answer_name', '').strip().lower()
        answer_symbol = request.form.get('answer_symbol', '').strip().lower()

        if guess == answer_name or guess == answer_symbol:
            msg = f"Correct! It was {answer_name.title()} ({answer_symbol.upper()})."
            return render_template('game.html', message=msg)
        else:
            return render_template('game.html', message="Wrong guess. Try again!", hint=request.form.get('hint'), answer_name=answer_name, answer_symbol=answer_symbol)
    except:
        return render_template('error.html')

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html'), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
