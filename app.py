import numpy as np
import flask
import pickle
from flask import Flask, redirect, url_for, request, render_template

#creating instance of Flask class

app = Flask(__name__, template_folder='templates')

# url trigger for the flask app
@app.route('/')
@app.route('/index')
def index():
  return flask.render_template('index.html')


#prediction function
def Prediction(predictions):
  predict_item = np.array(predictions).reshape(1,2)
  clustering_model = pickle.load(open('kmeans.pkl',"rb")) #load the trained K-Means model with pickle
  result = clustering_model.predict(predict_item) # make prediction after loading the pickle model 
  return result[0]

@app.route('/result', methods=['POST'])
def result():
  if request.method == 'POST':
    to_pred_list = request.form.values()
    to_pred_list = list(map(float, to_pred_list))
    result = Prediction(to_pred_list)

    if float(result) == 0:
      prediction_res = 'Cluster 0: Customer with medium annual income and medium annual spend'
    elif float(result) == 1:
      prediction_res = 'Cluster 1: Customer with meidum to high annual income and low annual spend'
    elif float(result) == 2:
      prediction_res = 'Cluster 2: Customer with low annual income and low annual spend'
    elif float(result) == 3:
      prediction_res = 'Cluster 3: Customer with low annual income and high annual spend'
    elif float(result) == 4:
      prediction_res = 'Cluster 4: Customer with medium to high annual income and high annual spend'

    return render_template("result.html", prediction=prediction_res)


# run the flask app
if __name__ == "__main__":
  app.run() 