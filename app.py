from flask import Flask,render_template,request
import google.generativeai as genai
import os
import textblob as textblob

model = genai.GenerativeModel("gemini-1.5-flash")
api = os.getenv("ROBOPROP")
genai.configure(api_key=api)

app = Flask(__name__)

@app.route("/predict_rent_result",methods=["GET","POST"])
def predict_rent_result():
    data = request.json
    property_type = data.get('propertyType')
    location = data.get('location')
    rooms = data.get('rooms')

    # Convert budget to a numerical value
    rooms_num = {
        '1R': 1,
        '2R': 2,
        '3R': 3,
        '4R': 4
    }.get(rooms, 0)
    
    # Define multipliers based on property type and location
    property_type_num = {
        'hdb': 1.0,
        'condo': 1.2,
        'landed': 1.5
    }.get(property_type, 1.0)
    
    location_num = {
        'bedok': 1.1,
        'tampines': 1.3,
        'jurong': 1.5
    }.get(location, 1.0)

    # Calculate estimated value
    r = 100 + 0.5*property_type_num +0.5*location_num + 0.5*rooms_num

    return(render_template("predict_rent_result.html",r=r))

if __name__ == '__main__':
    app.run(debug=True)
