from flask import Flask, render_template, request
import google.generativeai as genai  
import os
from PIL import Image
import requests
 
app = Flask(__name__)

model = genai.GenerativeModel("gemini-1.5-flash")
api = os.getenv("ROBOPROP")
genai.configure(api_key=api) 

searchApiKey = os.getenv("SEARCHAPIKEY")

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

    # Pass variables to the template
    return render_template(
        'predict_rent_result.html', 
        rent=int(estimated_rent), 
        property_type=property_type, 
        location=location, 
        rooms=rooms)


@app.route("/search_properties",methods=["POST"])
def search_properties():
    location = '1.3521,103.8198'  # Latitude and Longitude for Singapore
    radius = 50000  # Search radius in meters
    query = 'apartment for rent in Singapore'
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&location={location}&radius={radius}&key={searchApiKey}"

    response = requests.get(url)
    data = response.json()

    # Check if the response contains results
    if data.get('status') == 'OK':
        properties = data.get('results', [])

        # Add photo URL and Google Maps link to each property if available
        for property in properties:
            # Add photo URL if available
            if 'photos' in property:
                photo_reference = property['photos'][0]['photo_reference']
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={searchApiKey}"
                property['photo_url'] = photo_url
            else:
                property['photo_url'] = url_for('static', filename='images/no_image.png')

            # Add link to the place details on Google Maps
            property['place_url'] = f"https://www.google.com/maps/place/?q=place_id:{property['place_id']}"

    else:
        properties = []

    return render_template('search_property_result.html', properties=properties)
 
@app.route("/check_scam_result", methods=["POST"])
def check_scam_result():
    if 'image' not in request.files:
        return "No file part", 400

    file = request.files['image']

    if file.filename == '':
        return "No selected file", 400

    if file:
        try:
            # Open the image file using PIL (Python Imaging Library)
            image = Image.open(file.stream)

            # Generate a prompt for the model analysis
            prompt = "Analyze if this advertisement is about renting/selling of property. If yes, rate its legitimacy on a scale from 1 to 10.."
            
            # Convert the image to the required format for the generative model
            # Use the `Image` object directly instead of BytesIO
            response = model.generate_content([image, prompt])  # Adjust this as necessary

            result = response.text if response else "Unable to analyze the image at this time."
        except Exception as e:
            result = f"An error occurred: {str(e)}"

    return render_template("check_scam_result.html", r=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)