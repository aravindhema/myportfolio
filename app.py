from flask import Flask, render_template
import pandas as pd

# Configure application
app = Flask(__name__)

@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def index():

    greeting = 'Welcome to My Data Science Portfolio Website'

    return render_template('/index.html',
                            greeting=greeting)

@app.route('/about', methods=['POST', 'GET'])
def about():
    dataset1 = pd.read_csv('skills.csv')
    skill_dict = {}
    skill_dict = dataset1.to_dict('records')
    #print(skill_dict.items())
    return render_template('/about.html',skill_dict=skill_dict)

if __name__ == '__main__':
    app.run(port=5000)