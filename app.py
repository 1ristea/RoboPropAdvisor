from flask import Flask, render_template, request
import openai
import os
import re

app = Flask(__name__)
openai.api_key = os.getenv("ROBOPROP")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get the selected values from the form
    property_type = request.form.get('propertyType')
    location = request.form.get('location')
    rooms = request.form.get('rooms')

    # Perform calculation or any logic based on the dropdown selections
    # For example, calculating a hypothetical rental price based on inputs
    
    property_type_factor = {'HDB': 1, 'Condo': 2, 'Landed': 3}.get(property_type, 1)
    location_factor = {'Central': 1, 'East': 2, 'Northwest': 3,'West': 4,'North': 5}.get(location, 1)
    rooms_factor = {'1': 1, '2': 2, '3': 3, '4': 4}.get(rooms, 1)

    # Calculate the estimated rent
    estimated_rent = 1901.76 + -243.20*location_factor + -403.86*property_type_factor + 1530.39*rooms_factor

    return render_template('predict_rent_result.html', rent=int(estimated_rent))

@app.route("/search_properties",methods=["POST"])
def search_properties():
    return(render_template("search_property_result.html"))

@app.route("/check_scam_result", methods=["POST"])
def check_scam_result():
    # Get the URL from the form submission
    url = request.form.get('url')  # Make sure to get the URL from the form data

    # Check if the URL is None or empty
    if not url or url.strip() == "":
        result_message = "No URL provided. Please enter a valid URL."
        return render_template("check_scam_result.html", r=result_message)

    # Feature extraction
    features = {
        'length': len(url),
        'has_https': int('https://' in url),
        'has_at_symbol': int('@' in url),
        'has_ip': int(re.search(r"\d+\.\d+\.\d+\.\d+", url) is not None),
        'count_dots': url.count('.')
    }
    
    # Calculate risk score based on features
    risk_score = (
        features['has_https'] + 
        features['has_at_symbol'] + 
        features['has_ip'] + 
        (features['length'] > 50)  # Penalize for long URLs
    )
    
    # Generate result message based on risk score
    if risk_score == 1:
        result_message = "This URL appears to be safe."
    elif risk_score == 2:
        result_message = "This URL is slightly suspicious. Be cautious."
    else:
        result_message = "This URL is suspicious. Beware of scams!"

    return render_template("check_scam_result.html", r=result_message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)