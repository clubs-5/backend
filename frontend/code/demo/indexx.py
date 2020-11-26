from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/',methods=['Get'])
def index():
   return render_template('index.html')

@app.route('/hello',methods=['Get'])
def hello_world():
   return 'hello world'

@app.route('/result',methods = ['POST', 'GET'])
def result():
   #if request.method == 'POST':
   if True:
      result = request.form
      return render_template("result.html",result = result)

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)