import os
from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import spacy
from backend.backendMain import passToNLP, mainfunction
from google.cloud import dialogflow
from rapidfuzz import process, fuzz
from google.cloud.dialogflow_v2.types import TextInput, QueryInput
import uuid
from google.protobuf.json_format import MessageToDict


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
   # mainfunction()
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
            if pd.api.types.is_numeric_dtype(filtered_df[key]):
                filtered_df = filtered_df[filtered_df[key] == value]
            else:
                filtered_df = filtered_df[filtered_df[key] == value]
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
    

def find_best_match(user_input, choices):
    if not user_input or not choices:
        print("Missing user input or choices.")
        return None

    # Ensure choices is a list of strings
    if not isinstance(choices, list) or not all(isinstance(choice, str) for choice in choices):
        print("Invalid choices format. Expected a list of strings.")
        return None

    print(f"Choices provided for matching: {choices}")
    print(f"User input: {user_input}")

    # Perform fuzzy matching
    try:
        result = process.extractOne(user_input, choices, scorer=fuzz.WRatio)
        if result and result[1] >= 80:  # Check if result exists and meets the threshold
            return result[0]  # Return the matched string
        else:
            print(f"No match found. Highest score: {result[1] if result else 'N/A'}")
            return None
    except ValueError as e:
        print(f"Error in extractOne: {e}")
        return None


def handle_search_car(parameters):
    global df
    # Extract parameters
    print("HANDLING SEARCH")
    make_input = parameters.get('Make')
    model_input = parameters.get('Model')
    year_input = parameters.get('Year')
    body_input = parameters.get('Body')
    color_input = parameters.get('Color')
    transmission_input = parameters.get('Transmission')
    fuel_type_input = parameters.get('Fuel_type')
    type_input = parameters.get('Type')
    # Add other parameters as needed
    # Normalize inputs
    make_input = make_input.lower() if make_input else None
    model_input = model_input.lower() if model_input else None
    year_input = int(year_input) if year_input else None
    body_input = body_input.lower() if body_input else None
    color_input = color_input.lower() if color_input else None
    transmission_input = transmission_input.lower() if transmission_input else None
    fuel_type_input = fuel_type_input.lower() if fuel_type_input else None
    type_input = type_input.lower() if type_input else None

    if make_input:
        makes_list = df['Make'].dropna().unique().tolist()
        makes_list_lower = [make.lower() for make in makes_list]
        matched_make = find_best_match(make_input, makes_list_lower)
        if matched_make:
            make_input = matched_make  # Use the matched make
        else:
            response_text = f"Sorry, I couldn't find a make matching '{make_input}'. Could you please specify the make again?"
            return {
            'response_text': response_text,
            'recommendations': []  # Empty list when no recommendations
            }
            

    # Perform fuzzy matching for 'Model'
    if model_input:
        models_list = df['Model'].dropna().unique().tolist()
        models_list_lower = [model.lower() for model in models_list]
        matched_model = find_best_match(model_input, models_list_lower)
        if matched_model:
            model_input = matched_model  # Use the matched model
        else:
            response_text = f"Sorry, I couldn't find a model matching '{make_input}'. Could you please specify the model again?"
            return {
            'response_text': response_text,
            'recommendations': []  # Empty list when no recommendations
            }


    # Process the recommendation algorithm
    recommendations = get_recommendations(make_input, model_input, year_input,body_input,color_input,transmission_input,fuel_type_input,type_input)
    print("Getting recs")
    if recommendations.empty:
        response_text = "I'm sorry, I couldn't find any cars matching your criteria."
        return {
            'response_text': response_text,
            'recommendations': []  # Empty list when no recommendations
        }
    else:
        response_text = "Here are some cars that match your criteria:"
        # Convert recommendations to a list of dictionaries
        recommendations_list = recommendations.to_dict(orient='records')
        #print(f"Serialized Recommendations: {recommendations_list}")  # Debugging log

        return {
            'response_text': response_text,
            'recommendations': recommendations_list
        }

def get_recommendations(make, model, year, body,color,transmission,fuel_type,type_):
    user_criteria = {}
    if make:
        user_criteria['Make'] = make
    if model:
        user_criteria['Model'] = model
    if year:
        user_criteria['Year'] = year
    if body:
        user_criteria['Body'] = body
    if color:
        user_criteria['Ext_Color_Generic'] = color
    if transmission:
        user_criteria['Transmission'] = transmission
    if fuel_type:
        user_criteria['Fuel_type'] = fuel_type
    if type_:
        user_criteria['Type'] = type_


    """ if vin:
        user_criteria['VIN'] = vin
    if doors:
        user_criteria['Doors'] = doors
    if certified:
        user_criteria['Certified'] = certified
    if drivetrain:
        user_criteria['Drivetrain'] = drivetrain
    if mile:
        user_criteria['Miles'] = mile
    if transmission:
        user_criteria['Transmission'] = transmission
    if fuel_type:
        user_criteria['Fuel_type'] = fuel_type"""
        # Filter vehicles
    print(f"USER CRITERIA IS: {user_criteria}")
    filtered_df = filter_vehicles(user_criteria)
    print(f"LENGTH OF DF is :{len(filtered_df)}")
    if filtered_df.empty:
            return None  # Return None if no matches

        # Rank vehicles
    ranked_vehicles = rank_vehicles(filtered_df, user_criteria)
    if ranked_vehicles.empty:
        return None  # Return None if ranking yields no results

        # Return the ranked vehicles
    return ranked_vehicles

# Add other criteria as needed

    # Use your existing filtering and ranking logic
    # Return a list of recommended cars
    pass

def format_recommendations(recommendations):
    # Format the recommendations into a response string
    response_lines = []
    for car in recommendations:
        car_info = f"{car['Year']} {car['Make']} {car['Model']} priced at ${car['SellingPrice']}"
        response_lines.append(car_info)
    response_text = "Here are some cars that match your criteria:\n" + "\n".join(response_lines)
    return response_text

@app.route('/message', methods=['POST'])
def handle_message():
    global session_id
    print("HANDLING MESSAGE DIALOGFLOW")
    data = request.get_json()
    user_message = data.get('userMessage', '')
    session_id = data.get('sessionId', str(uuid.uuid4()))
    #print(f"Received user message: {user_message}")
    print(f"Received user message: {user_message}")  # Debugging log
    recommendations = []

    # Ensure user_message is not empty
    if not user_message.strip():
        return jsonify({'error': 'No user message provided'}), 400

    response_text, recommendations = get_dialogflow_response(user_message)
    print(f"RESPONSE IS:{response_text}")
    return jsonify({
        'response': response_text,
        'fulfillmentMessages': recommendations
    })



"""def serialize_recommendations(raw_recommendations):
    \"""Custom serialization for recommendations.\"""
    serialized = []
    for recommendation in raw_recommendations:
        try:
            if hasattr(recommendation, '_pb'):  # Check if it's a protobuf object
                serialized.append(MessageToDict(recommendation._pb))
            else:  # Fallback to dictionary conversion
                serialized.append(dict(recommendation))
        except Exception as e:
            print(f"Error serializing recommendation: {e}")
            serialized.append({"error": f"Serialization error: {e}"})
    return serialized
"""


def get_dialogflow_response(text):
    if not text.strip():
        raise ValueError("Input text is empty")
    global session_id
    project_id = 'newagent-hhex'  # Replace with your Dialogflow project ID
    language_code = 'en'
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print("In GET DIALOG FLOW RESPONSE")
    text_input = TextInput(text=text, language_code=language_code)
    query_input = QueryInput(text=text_input)

    # Detect intent
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})

    # Extract response text
    response_text = response.query_result.fulfillment_text
    #print(f"RESPONSEQUERYRESULTPAYLOAD Is:{response.query_result.fulfillment_text}")
    # Extract recommendations from the webhook payload if present
    #recommendations = []
    recommendations = []
    if response.query_result.webhook_payload:
        try:
            # Convert webhook_payload to dict
            #print(f"response IS:{response} ")
            #print(f"response Query result IS:{response.query_result} ")
            webhook_payload = MessageToDict(response.query_result._pb)
            #print(f"WEBHOOK_PAYLOAD IS:{webhook_payload} ")
            recommendations = webhook_payload.get('webhookPayload', {}).get('recommendations', [])
            #print(f"RECS FROM PAYLOAD:{recommendations}")
        except Exception as e:
            print(f"Error extracting recommendations: {e}")

    #print(f"RESPONSE TEXT IS : {response_text}")
    #print(f"Recommendations: {recommendations}")
    return response_text, recommendations


@app.route('/webhook', methods=['POST'])
def webhook():
    print("In WEBHOOK")
    req = request.get_json(force=True)
    intent_name = req.get('queryResult', {}).get('intent', {}).get('displayName')
    parameters = req.get('queryResult', {}).get('parameters', {})
    #print(f"PARAMETERS ARE: {parameters}")
    #print(f"INTENT IS : {intent_name}")
    if intent_name == 'SearchCar':
        print("SEARCHING FOR CAR")
        result = handle_search_car(parameters)
        response_text = result['response_text']
        recommendations = result['recommendations']
        # Return both the response text and recommendations
        #print(f"FINAL RECS IN WEBHOOK: {recommendations}")
        assert isinstance(recommendations, list), "Recommendations are not a list"
        assert all(isinstance(rec, dict) for rec in recommendations), "Not all recommendations are dictionaries"
        return jsonify({
            'fulfillmentText': response_text,
            'payload': {
                'recommendations': recommendations
            }
        })
    else:
        response_text = "I'm sorry, I didn't understand that."
        return jsonify({'fulfillmentText': response_text})




if __name__ == '__main__':
    #if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    print("Initializing backend...")
    initialize_app()  # Run the initialization code once
    

    app.run(debug=True)
