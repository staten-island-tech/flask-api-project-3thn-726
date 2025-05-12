from flask import Flask, render_template, abort, request, redirect, url_for, session
import requests
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Ensure you have this for session management

DATA_URL = "https://raw.githubusercontent.com/neelpatel05/periodic-table-api/refs/heads/master/data.json"

# Fetch elements from the external API
def fetch_elements():
    response = requests.get(DATA_URL)
    if response.status_code == 200:
        return response.json()
    return []

# Home route showing all elements
@app.route('/')
def index():
    elements = fetch_elements()
    return render_template('elements.html', elements=elements)

# Show details of a single element
@app.route('/element/<int:atomic_number>')
def element_detail(atomic_number):
    elements = fetch_elements()
    element = next((el for el in elements if el["atomicNumber"] == atomic_number), None)
    if element:
        return render_template('element.html', element=element)
    else:
        abort(404, description="Element not found")

# Search route for searching elements
@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    elements = fetch_elements()

    if not query:
        return render_template('search.html', query=query, results=[])

    results = []
    for el in elements:
        if (query in str(el['atomicNumber']).lower() or
            query in el['name'].lower() or
            query in el['symbol'].lower()):
            results.append(el)
    
    return render_template('search.html', query=query, results=results)

# Start the guessing game
@app.route('/game-web')
def start_game_web():
    elements = fetch_elements()
    element = random.choice(elements)
    session['element'] = {
        'name': element['name'],
        'symbol': element['symbol'],
        'atomicNumber': element['atomicNumber']
    }
    session['attempts'] = 0
    return render_template('game.html', hint=element['atomicNumber'])

# Handle the guess in the game
@app.route('/game/guess-web', methods=['POST'])
def guess_element_web():
    if 'element' not in session:
        return redirect(url_for('start_game_web'))

    guess = request.form.get('guess', '').strip().lower()
    target = session['element']
    session['attempts'] += 1

    if guess == target['name'].lower() or guess == target['symbol'].lower():
        message = f"🎉 Correct! It was {target['name']} ({target['symbol']}). Attempts: {session['attempts']}"
        session.pop('element', None)
        return render_template('game.html', message=message)
    else:
        hint = target['atomicNumber']
        message = "❌ Incorrect guess. Try again!"
        return render_template('game.html', hint=hint, message=message)

# Main entry point to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
