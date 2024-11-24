import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
import random
import matplotlib.pyplot as plt

def mainfunction():
    # Load a blank English model
    print("ENTERED MAIN FUNCITON")
    nlp = spacy.load("en_core_web_md")
    ner= nlp.get_pipe("ner")

    # Define your training examples with correct entity offsets
    examples = [
        ("I need a green SUV under $20,000.", {"entities": [(9, 14, "COLOR"), (15, 18, "Body"), (24, 31, "PRICE")]}),
        ("Show me a blue sedan for $25,000.", {"entities": [(10, 14, "COLOR"), (15, 20, "Body"), (25, 32, "PRICE")]}),
        ("Can you find me a red 4x4 around $50,000?", {"entities": [(18, 21, "COLOR"), (22, 25, "Body"), (33, 40, "PRICE")]}),
        ("Do you have silver trucks below $30,000?", {"entities": [(12, 18, "COLOR"), (19, 25, "Body"), (32, 39, "PRICE")]}),
        ("I'm interested in luxury SUVs costing $60,000.", {"entities": [(16, 22, "Body"), (31, 38, "PRICE")]}),
        ("Can I buy a car for less than $15,000?", {"entities": [(20, 27, "PRICE")]}),
        ("Find me a white sedan priced under $40,000.", {"entities": [(10, 15, "COLOR"), (16, 21, "Body"), (34, 41, "PRICE")]}),
        ("Are there black SUVs costing above $70,000?", {"entities": [(10, 15, "COLOR"), (16, 19, "Body"), (33, 40, "PRICE")]}),
        ("Can you show me an orange hatchback for $18,000?", {"entities": [(19, 25, "COLOR"), (26, 35, "Body"), (40, 47, "PRICE")]}),
        ("I'm looking for something costing between $25,000 and $50,000.", {"entities": [(41, 48, "PRICE"), (53, 60, "PRICE")]}),
        # Additional examples you provided
        ("I'm looking for a 2018 Toyota Camry with less than 50,000 miles.", {"entities": [(18, 22, "YEAR"), (23, 29, "MAKE"), (30, 35, "MODEL"), (47, 60, "MILES")]}),
        ("Do you have any electric SUVs?", {"entities": [(16, 24, "FUEL_TYPE"), (25, 28, "Body")]}),
        ("Can I get a 2-door coupe in red color?", {"entities": [(13, 19, "DOORS"), (20, 25, "Body"), (29, 32, "COLOR")]}),
        ("I'm interested in a black sedan with V6 engine.", {"entities": [(18, 23, "COLOR"), (24, 29, "Body"), (35, 37, "EngineCylinders")]}),
        ("Find me a used 2017 Ford F-150 with less than 60,000 miles and four-wheel drive.", {"entities": [(10, 14, "TYPE"), (15, 19, "YEAR"), (20, 24, "MAKE"), (25, 30, "MODEL"), (46, 59, "MILES"), (64, 79, "DRIVETRAIN")]}),
        ("Looking for a diesel truck with at least 400 horsepower.", {"entities": [(14, 20, "FUEL_TYPE"), (21, 26, "Body"), (38, 51, "Engine_Description")]}),
        ("Do you have any cars with seating for 7 passengers?", {"entities": [(16, 20, "Body"), (32, 43, "PassengerCapacity")]}),
        ("I'm interested in a compact SUV with good city MPG.", {"entities": [(18, 25, "Body"), (36, 45, "CityMPG")]}),
        ("I want a car with a sunroof and Bluetooth connectivity.", {"entities": [(9, 12, "Body"), (20, 27, "OPTIONS"), (32, 52, "OPTIONS")]}),
        ("Find me a 2015 or newer sedan under $15,000.", {"entities": [(9, 23, "YEAR"), (24, 29, "Body"), (36, 43, "PRICE")]}),
        ("I'd like an all-wheel-drive crossover with a panoramic sunroof.", {"entities": [(10, 25, "DRIVETRAIN"), (26, 35, "Body"), (44, 61, "OPTIONS")]}),
        ("Show me vehicles with VIN number ending in 1234.", {"entities": [(8, 16, "Body"), (34, 38, "VIN")]}),
        ("I need a vehicle with at least 300 horsepower.", {"entities": [(9, 16, "Body"), (27, 40, "Engine_Description")]}),
        ("Looking for a hybrid sedan with high highway MPG.", {"entities": [(14, 20, "FUEL_TYPE"), (21, 26, "Body"), (37, 48, "HighwayMPG")]}),
        ("Can you find me a luxury SUV with premium sound system?", {"entities": [(18, 22, "Body"), (28, 48, "OPTIONS")]}),
        ("I prefer a manual transmission sports car.", {"entities": [(10, 29, "TRANSMISSION"), (30, 40, "Body")]}),
        ("Do you have any certified pre-owned vehicles?", {"entities": [(16, 38, "Certified"), (39, 47, "Body")]}),
        ("I'm looking for a vehicle in stock number ABC123.", {"entities": [(18, 25, "Body"), (40, 46, "Stock")]}),
        ("Find me an SUV with engine displacement over 3.0L.", {"entities": [(11, 14, "Body"), (20, 42, "EngineDisplacement")]}),
        ("I want a car with automatic transmission and navigation system.", {"entities": [(9, 12, "Body"), (18, 39, "TRANSMISSION"), (44, 61, "OPTIONS")]}),
        ("Looking for a blue hatchback with less than 30,000 miles.", {"entities": [(14, 18, "COLOR"), (19, 28, "Body"), (40, 53, "MILES")]}),
        ("I'm seeking a vehicle no older than 2015 with under 80,000 miles.", {"entities": [(18, 25, "Body"), (39, 43, "YEAR"), (54, 67, "MILES")]}),
        ("Do you have any SUVs priced between $30,000 and $45,000?", {"entities": [(16, 19, "Body"), (35, 42, "PRICE"), (47, 54, "PRICE")]}),
        ("Looking for a sedan with over 200 horsepower.", {"entities": [(14, 19, "Body"), (25, 38, "Engine_Description")]}),
        ("Can I find a coupe that's no less than $25,000?", {"entities": [(14, 19, "Body"), (36, 43, "PRICE")]}),
        ("I need a truck not exceeding $35,000 with at least 15 MPG city.", {"entities": [(9, 14, "Body"), (30, 37, "PRICE"), (50, 60, "CityMPG")]}),
        ("Show me convertibles costing no more than $50,000.", {"entities": [(8, 20, "Body"), (36, 43, "PRICE")]}),
        ("I'm interested in a 4-door sedan from 2018 or newer.", {"entities": [(18, 24, "DOORS"), (25, 30, "Body"), (36, 49, "YEAR")]}),
        ("Find me an SUV with a wheelbase longer than 110 inches.", {"entities": [(11, 14, "Body"), (36, 47, "Wheelbase_Code")]}),
        ("Do you have any cars with engine displacement below 2.5L?", {"entities": [(16, 20, "Body"), (26, 48, "EngineDisplacement")]}),
        ("Looking for a minivan that's no more than 5 years old.", {"entities": [(14, 21, "Body"), (38, 49, "YEAR")]}),
        ("Can I get a vehicle with less than 50,000 miles and priced under $20,000?", {"entities": [(13, 20, "Body"), (32, 45, "MILES"), (59, 66, "PRICE")]}),
        ("I'm after a luxury sedan with a top speed exceeding 150 mph.", {"entities": [(14, 19, "Body"), (41, 52, "Engine_Description")]}),
        ("Show me trucks that are no older than 2016 and under $40,000.", {"entities": [(8, 14, "Body"), (32, 36, "YEAR"), (47, 54, "PRICE")]}),
        ("Do you have any cars not older than 3 years with Bluetooth?", {"entities": [(16, 20, "Body"), (34, 39, "YEAR"), (45, 54, "OPTIONS")]}),
        ("I'm interested in an SUV with seating for no less than 6 people.", {"entities": [(18, 21, "Body"), (43, 44, "PassengerCapacity")]}),
        ("Find me a vehicle with a fuel efficiency of at least 30 MPG highway.", {"entities": [(9, 16, "Body"), (44, 56, "HighwayMPG")]}),
        ("Looking for a hatchback priced at no more than $25,000.", {"entities": [(14, 23, "Body"), (40, 47, "PRICE")]}),
        ("Can you show me cars with a towing capacity over 5,000 lbs?", {"entities": [(17, 21, "Body"), (29, 53, "Engine_Description")]}),
        ("I need an all-wheel-drive vehicle with less than 70,000 miles.", {"entities": [(9, 25, "DRIVETRAIN"), (26, 33, "Body"), (45, 58, "MILES")]}),
        ("Do you have any electric cars under $35,000 with fast charging?", {"entities": [(16, 24, "FUEL_TYPE"), (25, 29, "Body"), (36, 43, "PRICE"), (49, 62, "OPTIONS")]}),
        # New examples covering additional columns
        ("I'm looking for a pickup truck with 4WD, leather seats, and under 50,000 km.", {"entities": [(18, 30, "Body"), (36, 39, "DRIVETRAIN"), (41, 54, "OPTIONS"), (65, 75, "MILES")]}),
        ("Do you have a sporty car with a sunroof and under 50,000 km?", {"entities": [(16, 19, "Body"), (29, 36, "OPTIONS"), (47, 57, "MILES")]}),
        ("Do you have a red convertible under 30,000 km?", {"entities": [(13, 16, "COLOR"), (17, 28, "Body"), (35, 45, "MILES")]}),
        ("Do you have a family SUV with leather seats and low mileage?", {"entities": [(16, 19, "Body"), (25, 38, "OPTIONS"), (43, 55, "MILES")]}),
        ("Do you have an electric car with a range of at least 300 miles and advanced safety features?", {"entities": [(13, 21, "FUEL_TYPE"), (22, 25, "Body"), (47, 58, "MILES"), (63, 89, "OPTIONS")]}),
        ("I'm looking for an SUV with captain's chairs and a panoramic sunroof.", {"entities": [(18, 21, "Body"), (27, 42, "OPTIONS"), (49, 65, "OPTIONS")]}),
        ("Do you have a minivan with stow-and-go seating and rear-seat entertainment?", {"entities": [(13, 20, "Body"), (26, 44, "OPTIONS"), (49, 73, "OPTIONS")]}),
        ("I'm looking for a high-performance car with launch control and Brembo brakes.", {"entities": [(18, 22, "Body"), (29, 47, "Engine_Description"), (53, 67, "OPTIONS"), (72, 86, "OPTIONS")]}),
        ("Do you have the car with VIN 1HGCM82633A123456?", {"entities": [(16, 19, "Body"), (29, 46, "VIN")]}),
        ("I'm looking for the car with VIN 5FNYF6H57LB789012.", {"entities": [(21, 24, "Body"), (34, 51, "VIN")]}),
        ("Do you have an SUV with off-road capabilities, a roof rack, and skid plates?", {"entities": [(13, 16, "Body"), (22, 43, "OPTIONS"), (47, 56, "OPTIONS"), (62, 73, "OPTIONS")]}),
        ("Do you have an SUV with remote start, a heated steering wheel, and a power liftgate?", {"entities": [(13, 16, "Body"), (22, 34, "OPTIONS"), (38, 60, "OPTIONS"), (66, 81, "OPTIONS")]}),
        ("I'm looking for an SUV with third-row seating.", {"entities": [(18, 21, "Body"), (27, 42, "OPTIONS")]}),
        ("Do you have a hybrid SUV?", {"entities": [(13, 19, "FUEL_TYPE"), (20, 23, "Body")]}),
        ("I currently drive a 2018 Toyota Camry. Do you have anything similar?", {"entities": [(19, 23, "YEAR"), (24, 30, "MAKE"), (31, 36, "MODEL")]}),
        ("I'm driving a 2018 Hyundai Tucson right now. Any similar SUVs in stock?", {"entities": [(15, 19, "YEAR"), (20, 27, "MAKE"), (28, 34, "MODEL"), (53, 57, "Body")]}),
        ("I want an electric car.", {"entities": [(9, 17, "FUEL_TYPE"), (18, 21, "Body")]}),
        ("I'm looking for a fun car to drive.", {"entities": [(18, 21, "Body")]}),
    ]

    # Add labels to the NER component
    for _, annotations in examples:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # Convert training examples to spaCy's Example objects
    training_data = []
    for text, annotations in examples:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        training_data.append(example)

    # Begin training
    nlp.begin_training()
    # You can set a seed for reproducibility
    random.seed(42)
    spacy.util.fix_random_seed(42)

    # Let's split the data into training and validation sets
    split = int(len(training_data) * 0.8)
    train_data = training_data[:split]
    valid_data = training_data[split:]

    # Tracking losses and validation scores
    train_losses = []
    valid_f_scores = []

    for epoch in range(50):
        random.shuffle(train_data)
        losses = {}
        batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.5))
        for batch in batches:
            nlp.update(
                batch,
                drop=0.35,
                losses=losses
            )
        train_losses.append(losses.get('ner', 0.0))
        
        # Evaluate on validation data
        examples = []
        for example in valid_data:
            pred_doc = nlp(example.reference.text)
            examples.append(Example(predicted=pred_doc, reference=example.reference))
        # Calculate F-score
        scorer = spacy.scorer.Scorer()
        scores = scorer.score(examples)
        valid_f_scores.append(scores['ents_f'])
        
        #print(f"Epoch {epoch + 1}, Loss: {train_losses[-1]:.4f}, Validation F-score: {valid_f_scores[-1]:.2f}")

    # Plot the training loss and validation F-score
    plt.figure(figsize=(10,5))
    plt.plot(train_losses, label='Training Loss')
    plt.plot(valid_f_scores, label='Validation F-score')
    plt.xlabel('Epoch')
    plt.ylabel('Value')
    plt.legend()
    plt.title('Training Loss and Validation F-score over Epochs')
    plt.show()

    # Save the model
    nlp.to_disk("custom_ner_model")



def passToNLP(text):
    print(f"in pass_to_nlp, text is : {text}")
    nlp = spacy.load("custom_ner_model")
    doc = nlp(text)
    print(f"Input text: {text}")
    print(f"Doc is: {doc}")
    
    # Extract and format criteria
    extracted_criteria = {}
    for ent in doc.ents:
        print(f"Doc entity text: {ent.text}")
        print(f"Doc entity label: {ent.label_}")

        # Map entity labels to the keys used in the criteria dictionary
        if ent.label_ == "Price_Range":
            extracted_criteria["Price_Range"] = ent.text
        elif ent.label_ == "Miles_Range":
            extracted_criteria["Miles_Range"] = ent.text
        elif ent.label_ == "Body":
            extracted_criteria["Body"] = ent.text
        elif ent.label_ == "MAKE":
            extracted_criteria["Make"] = ent.text
        elif ent.label_ == "Model":
            extracted_criteria["Model"] = ent.text
        elif ent.label_ == "COLOR":
            extracted_criteria["Ext_Color_Generic"] = ent.text

    # Print the formatted criteria
    print(f"Extracted criteria: {extracted_criteria}")

    # Return the formatted criteria
    return extracted_criteria

