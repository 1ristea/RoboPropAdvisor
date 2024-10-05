from flask import Flask,render_template,request
import google.generativeai as genai
import os
import numpy as np
import textblob as textblob

model = genai.GenerativeModel("gemini-1.5-flash")
api = os.getenv("MAKERSUITE")
genai.configure(api_key=api)

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/prediction_DBS",methods=["GET","POST"])
def prediction_DBS():
    return(render_template("prediction_DBS.html"))

@app.route("/prediction_result_DBS",methods=["GET","POST"])
def prediction_result_DBS():
    q = float(request.form.get("q"))
    r = (-50.6*q) + 90.2
    return(render_template("prediction_result_DBS.html",r=r))

@app.route("/faq",methods=["GET","POST"])
def faq():
    return(render_template("faq.html"))

@app.route("/prediction_creditability",methods=["GET","POST"])
def prediction_creditability():
    return(render_template("prediction_creditability.html"))

@app.route("/prediction_result_creditability",methods=["GET","POST"])
def prediction_result_creditability():
    q = float(request.form.get("q"))
    r = (-0.00010249*q) + 1.19310109
    r = np.where(r>=0.5,"Creditable","Not Creditable")
    return(render_template("prediction_result_creditability.html",r=r))

@app.route("/sentiment_analysis",methods=["GET","POST"])
def sentiment_analysis():
    return(render_template("sentiment_analysis.html"))

@app.route("/sentiment_analysis_result",methods=["GET","POST"])
def sentiment_analysis_result():
    q = request.form.get("q")
    r = textblob.TextBlob(q).sentiment
    return(render_template("sentiment_analysis_result.html",r=r))

@app.route("/q1",methods=["GET","POST"])
def q1():
    r = model.generate_content("How should I diversify my investment portfolio?")
    return(render_template("q1_reply.html",r=r))

@app.route("/q2",methods=["GET","POST"])
def q2():
    q = request.form.get("q")
    r = model.generate_content(q)
    return(render_template("q2_reply.html",r=r))

if __name__ == "__main__":
    app.run()
                        
