from flask import Flask, render_template, abort
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
        abort(404, description="Element  aint not found")

if __name__ == '__main__':
    app.run(debug=True)
