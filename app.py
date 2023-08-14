from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData,PredictPipeline


# Creating the application.

application=Flask(__name__)
app=application


## Route for a home page

@app.route('/')
def index():
    return render_template('index.html') 


# Route for predictdata page.
 
@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    # Renders the home.html if the request method is GET.
    if request.method=='GET':
        return render_template('home.html')
    # Calls the CustomData class from Predict_pipeline if the request method is POST.
    else:
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))

        )
        pred_df=data.get_data_as_dataframe()
        print(pred_df)
        print("Before Prediction")

        predict_pipeline=PredictPipeline()
        print("Mid Prediction")
        results=predict_pipeline.predict(pred_df)
        print("after Prediction")
        return render_template('home.html',results=results[0])
    

# Running the app.

if __name__=="__main__":
    app.run(host="0.0.0.0")




