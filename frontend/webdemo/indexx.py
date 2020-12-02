from flask import Flask, render_template, request
from to_1min import runPy

app = Flask(__name__)

@app.route('/',methods=['Get'])
def index():
   return render_template('index.html')

@app.route('/chart',methods=['GET', 'POST'])
def chart():
   if request.method == 'POST':
      print("here")
      runPy()
      return render_template('chart.html')
   else:
      return render_template('chart.html')

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)