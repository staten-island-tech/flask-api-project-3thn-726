from flask import Flask, render_template, abort, request
import requests

app = Flask(__name__)
DATA_URL = "https://raw.githubusercontent.com/neelpatel05/periodic-table-api/refs/heads/master/data.json"

def fetch_elements():
    response = requests.get(DATA_URL)
    if response.status_code == 200:
        return response.json()
    return []

@app.route('/')
def index():
    elements = fetch_elements()
    return render_template('elements.html', elements=elements)

@app.route('/element/<int:atomic_number>')
def element_detail(atomic_number):
    elements = fetch_elements()
    element = next((el for el in elements if el["atomicNumber"] == atomic_number), None)
    if element:
        return render_template('element.html', element=element)
    else:
        abort(404, description="Element aint not found")

@app.route("/testing")
def testing():
    return render_template('testing.html')

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

if __name__ == '__main__':
    app.run(debug=True)
