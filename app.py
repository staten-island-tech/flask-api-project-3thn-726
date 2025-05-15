from flask import Flask, render_template, abort, request, redirect, url_for, session
import requests
import random
import logging

app = Flask(__name__)
app.secret_key = 'nut_secrete_keys_trust'


DATA_URL = "https://raw.githubusercontent.com/neelpatel05/periodic-table-api/refs/heads/master/data.json"

logging.basicConfig(level=logging.INFO)

def fetch_elements():
    try:
        response = requests.get(DATA_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return render_template('error.html')
    except ValueError:
        return render_template('error.html')

@app.route('/')
def index():
    elements = fetch_elements()
    return render_template('elements.html', elements=elements)

@app.route('/element/<int:atomic_number>')
def element_detail(atomic_number):
    elements = fetch_elements()
    try:
        element = next((el for el in elements if el.get("atomicNumber") == atomic_number), None)
        if element:
            return render_template('element.html', element=element)
        else:
            return render_template('error.html')
    except (TypeError, KeyError):
        return render_template('error.html')

@app.route('/search')
def search():
    try:
        query = request.args.get('q', '').strip().lower()
        elements = fetch_elements()

        if not query:
            return render_template('search.html', query=query, results=[])

        results = []
        for el in elements:
            try:
                if (query in str(el.get('atomicNumber', '')).lower() or
                    query in el.get('name', '').lower() or
                    query in el.get('symbol', '').lower()):
                    results.append(el)
            except AttributeError as e:
                logging.warning(f"Malformed element data: {e}")
                continue
        
        return render_template('search.html', query=query, results=results)
    except Exception as e:
        logging.error(f"Search error: {e}")
        abort(500)

@app.route('/game-web')
def start_game_web():
    elements = fetch_elements()
    try:
        element = random.choice(elements)
        session['element'] = {
            'name': element.get('name', ''),
            'symbol': element.get('symbol', ''),
            'atomicNumber': element.get('atomicNumber', 0)
        }
        session['attempts'] = 0
        return render_template('game.html', hint=element.get('atomicNumber'))
    except (IndexError, KeyError, TypeError):
        return render_template('error.html')

@app.route('/game/guess-web', methods=['POST'])
def guess_element_web():
    try:
        if 'element' not in session:
            return redirect(url_for('start_game_web'))

        guess = request.form.get('guess', '').strip().lower()
        target = session.get('element', {})
        session['attempts'] = session.get('attempts', 0) + 1

        if guess == target.get('name', '').lower() or guess == target.get('symbol', '').lower():
            message = f"🎉 Correct! It was {target.get('name')} ({target.get('symbol')}). Attempts: {session['attempts']}"
            session.pop('element', None)
            return render_template('game.html', message=message)
        else:
            hint = target.get('atomicNumber', '?')
            message = "❌ Incorrect guess. Try again!"
            return render_template('game.html', hint=hint, message=message)
    except Exception:
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
