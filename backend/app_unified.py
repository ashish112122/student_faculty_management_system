# Unified backend application - placeholder for old version
# This file was part of the old implementation
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Unified Backend - Old Version"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
