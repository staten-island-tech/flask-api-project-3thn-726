from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def show_elements():
    api_url = "https://periodic-table-api.vercel.app/api/element/all"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        elements = response.json()
        return render_template('elements.html', elements=elements)
    else:
        return f"Failed to fetch data from API. Status code: {response.status_code}", 500

if __name__ == '__main__':
    app.run(debug=True)
