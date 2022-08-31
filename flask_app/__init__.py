import os
import pickle
from flask import Flask, render_template, request
import pandas as pd
import math


# ML 파일 가져오기
PKL_PATH = os.path.join(os.getcwd(), 'flask_app/model.pkl') 
model = None
with open(PKL_PATH,'rb') as pickle_file:
   model = pickle.load(pickle_file)


# FLASK 생성
def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/search', methods=['POST'])
    def search():
        menu = request.form.getlist("menu")
        location = request.form.getlist("location")
        nokidszone = request.form.getlist("nokidszone")[0].split(',')
        booking = request.form.getlist("booking")[0].split(',')
        reviewyear = request.form.getlist("reviewyear")

        result1 = len(nokidszone)*len(booking)/math.gcd(len(nokidszone), len(booking))
        result2 = result1*len(reviewyear)/math.gcd(int(result1), len(reviewyear))
        repeatnum = int(result2)
        
        X_test = pd.DataFrame({
            '별점': [100]*repeatnum,
            '노키즈존여부': nokidszone*int(repeatnum/len(nokidszone)),
            '예약가능여부': booking*int(repeatnum/len(booking)),
            '메뉴대분류': menu*repeatnum,
            '리뷰작성연도': reviewyear*int(repeatnum/len(reviewyear)),
            '위치': location*repeatnum
        })
        y_pred = model.predict(X_test)
        mlresult = pd.DataFrame(y_pred).value_counts()
        resultvalue = [mlresult.index[i][0] for i in range(len(mlresult))]

        return render_template('search.html', data=resultvalue)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
