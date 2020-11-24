from flask import Flask, render_template
app = Flask(__name__)

@app.route('/',methods=['Get'])
def index():
   return render_template('index.html')

@app.route('/chart',methods=['Get'])
def hello_world():
   return render_template('generic.html')

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)