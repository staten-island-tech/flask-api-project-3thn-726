from flask import Flask, render_template
import requests

response = requests.get("https://raw.githubusercontent.com/neelpatel05/periodic-table-api/refs/heads/master/data.json")
elements = response.json()

@app.route('/')
def index():
    return render_template('elements.html', elements=elements)