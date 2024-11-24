import os
from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import spacy
from backend.backendMain import passToNLP, mainfunction

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables to hold the processed data
df = None  # The preprocessed dataframe
# Define weights for ranking
HIERARCHY_WEIGHTS = {
    'Price_Range': 5,
    'Miles_Range': 4,
    'Body': 4,
    'Fuel_Type': 3,
    'Drivetrain': 3,
    'Make': 3,
    'Year': 3,
    'Transmission': 2,
    'PassengerCapacity': 2,
    'Style_Description': 2,
    'Ext_Color_Generic': 2,
    'InteriorColor': 1,
}

def initialize_app():
    """Run setup code that should execute only once when the app starts."""
    global df

    print("Initializing app and loading data...")
    
    # Load and preprocess the vehicle data
    df = pd.read_csv('vehicles.csv')

    # Eliminate unnecessary columns
    columns_to_drop = ['MRSP', 'Int_Uphalstery', 'Internet_Price']
    df = df.drop(columns=columns_to_drop, errors='ignore')

    # Create Price_Range column
    price_bins = [0, 10000, 20000, 30000, 50000, float('inf')]
    price_labels = ['$0-$10K', '$10K-$20K', '$20K-$30K', '$30K-$50K', '$50K+']
    df['Price_Range'] = pd.cut(df['SellingPrice'], bins=price_bins, labels=price_labels)
    string_columns = df.select_dtypes(include=["object"]).columns
    df[string_columns] = df[string_columns].applymap(lambda x: x.lower() if isinstance(x, str) else x)

    # Create Miles_Range column
    miles_bins = [0, 10000, 30000, 60000, 100000, float('inf')]
    miles_labels = ['0-10K', '10K-30K', '30K-60K', '60K-100K', '100K+']
    df['Miles_Range'] = pd.cut(df['Miles'], bins=miles_bins, labels=miles_labels)

    # Drop rows with missing ranges
    df = df.dropna(subset=['Price_Range', 'Miles_Range'])

    # Perform backend initialization
    mainfunction()
    print("Initialization complete.")

def calculate_vehicle_score(vehicle, user_criteria):
    """Calculate a score for a vehicle based on user criteria."""
    score = 0
    for key, value in user_criteria.items():
        if pd.notna(vehicle.get(key)) and vehicle.get(key) == value:
            score += HIERARCHY_WEIGHTS.get(key, 0)
    return score

def rank_vehicles(df, user_criteria, top_n=10):
    """Rank vehicles based on user criteria."""
    if df.empty:
        return []
    df['Score'] = df.apply(lambda row: calculate_vehicle_score(row, user_criteria), axis=1)
    ranked_vehicles = df.sort_values(by='Score', ascending=False)
    return ranked_vehicles.head(top_n)

def filter_vehicles(parsed_criteria):
    """Filter vehicles based on parsed criteria."""
    print("In filtering vehicles")
    filtered_df = df.copy()
    for key, value in parsed_criteria.items():
        if key in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[key] == value.lower()]
    return filtered_df

@app.route('/filter', methods=['POST'])
def filter_and_rank_vehicles():
    i=0
    print(i)
    """API endpoint to filter and rank vehicles."""
    try:
        i+=1
        print("FILTERINGI VEHICLES")
        # Parse incoming JSON data
        parsed_criteria = request.json
        user_message = parsed_criteria.get('userMessage', '')
        print(f"Got user message:{user_message}")
        # Process NLP criteria via backend
        criteria = passToNLP(user_message)
        print(f"NLP Returned: {criteria}")

        if not criteria:
            return jsonify("NLP couldn't match any features. Please update your search criteria.")

        # Mocked NLP criteria extraction (replace with actual NLP logic)
        mock_criteria = {
            "Price_Range": "$20K-$30K",
            "Miles_Range": "30K-60K",
        }
       
        # Filter and rank vehicles
        filtered_df = filter_vehicles(criteria)
        print(f"Length of df with the given nlp output: {len(filtered_df)}")
        if filtered_df.empty:
            return jsonify("No matches found. Please update your search criteria.")

        ranked_vehicles = rank_vehicles(filtered_df, mock_criteria)
        if ranked_vehicles.empty:
            return jsonify("No matches found after ranking.")

        # Convert results to a readable format
        response = ranked_vehicles[[
            "Year", "Make", "Model", "SellingPrice", "Miles", "Body",
            "Ext_Color_Generic", "Price_Range", "Miles_Range", "Score"
        ]].to_dict(orient="records")

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        print("Initializing backend...")
        initialize_app()  # Run the initialization code once
    

    app.run(debug=True)

@app.route('/compare', methods=['POST'])
def get_comparison_data():
    """
    API endpoint to fetch detailed information about selected vehicles for comparison.
    """
    try:
        # Parse the incoming JSON data
        request_data = request.json
        print(f"Request data is: {request_data}")
        vin_list = request_data.get('vinList', [])  # Expecting a list of VINs
        print(f"Received VIN list for comparison: {vin_list}")

        if not vin_list:
            return jsonify({'error': 'VIN list is empty. Please provide VINs to compare.'}), 400

        # Filter the dataframe for the selected VINs
        comparison_data = df[df['VIN'].isin(vin_list)]

        if comparison_data.empty:
            return jsonify({'error': 'No vehicles found for the provided VINs.'}), 404

        # Convert the results to a readable format
        response = comparison_data[[
            "VIN", "Year", "Make", "Model", "SellingPrice", "Miles", "Body",
            "Ext_Color_Generic", "Int_Color_Generic", "Drivetrain", "Fuel_Type",
            "CityMPG", "HighwayMPG", "PassengerCapacity", "Transmission"
        ]].to_dict(orient="records")

        return jsonify(response)

    except Exception as e:
        print(f"Error fetching comparison data: {e}")
        return jsonify({'error': str(e)}), 500

