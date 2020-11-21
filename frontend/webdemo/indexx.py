from flask import Flask, render_template
app = Flask(__name__)

@app.route('/',methods=['Get'])
def index():
   return render_template('index.html')

@app.route('/hello',methods=['Get'])
def hello_world():
   return 'hello world'

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)