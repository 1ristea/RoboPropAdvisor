from flask import Flask, render_template, request

app = Flask(__name__)

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
    base_price = 1000
    property_type_factor = {'HDB': 1.0, 'Condo': 1.5, 'Landed': 2.0}.get(property_type, 1.0)
    location_factor = {'Bedok': 1.1, 'Tampines': 1.3, 'Jurong': 1.5}.get(location, 1.0)
    rooms_factor = {'1R': 0.8, '2R': 1.0, '3R': 1.2, '4R': 1.5}.get(rooms, 1.0)

    # Calculate the estimated rent
    estimated_rent = base_price * property_type_factor * location_factor * rooms_factor

    return render_template('result.html', rent=estimated_rent)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
