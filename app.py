from flask import Flask, render_template, request
from analyzer import analyze_website

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form['url']
    report = analyze_website(url)
    return render_template('result.html', report=report, url=url)

if __name__ == '__main__':
    app.run(debug=True)
