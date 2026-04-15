from flask import Flask, request, jsonify
import json
import math
from models import init_db, get_db_connection
from evaluator import evaluate_opportunity
from email_service import send_email

app = Flask(__name__)


# guide
@app.route('/guide', methods=['GET'])
def get_guide():
    return jsonify({
        "1:Instructions": "Create a model with criteria and optional derived fields. To avoid syntax errors, make sure to end each consecutive line with a comma except for the last line in each section. (The steps are numbered for clarity and are not meant to be included in the actual model.)",
        "2:Rules": [
            "Weights must sum to 1.0",
            "Use min/max to normalize values",
            "Derived fields use formulas (e.g., profit = revenue - costs)"
        ],
        "3: Enter this (3a-3c) to start the model creation process": [
            "3a: POST http://127.0.0.1:5000/model",
            "3b: Content-Type: application/json",
            "3c: {"
        ],
        "4: example_model format": {
            "4a: name": "Example Model",
            "4b: criteria": [
                {
                    "1: field_name": "profit_margin",
                    "2: weight": 0.5,
                    "3: min": 0,
                    "4: max": 1
                },
                {
                    "1: field_name": "customer_satisfaction",
                    "2: weight": 0.5,
                    "3: min": 1,
                    "4: max": 5
                }
            ],
            "4c: derived_fields": [
                {
                    "1: name": "profit_margin",
                    "2: formula": "(revenue - costs) / revenue"
                },
                {
                    "1: name": "customer_satisfaction",
                    "2: formula": "(customer_rating / 5)"
                }
            ]
        },
        "5": "end with another '}' to close",

        "6: Once model is created, enter the following stepts to submit an opportunity for evaluation": [
            "6a: POST http://127.0.0.1:5000/opportunity",
            "6b: Content-Type: application/json",
            "6c: {",
        ],

        "7": "model_id : 1,",

        "8: data": [
            "8a: revenue: 40000",
            "8b: cost: 10000,",
            "8c: customer_rating: 4"
        ],
    })

# create model
@app.route('/model', methods=['POST'])
def create_model():

    data = request.json
    model_name = data.get('name')
    criteria = data.get('criteria', [])
    derived_fields = data.get('derived_fields', [])

    total_weight = sum(crit['weight'] for crit in criteria)
    if total_weight < 1.0:
        return jsonify({"error": "Total weight of criteria is less than 1.0"}), 400
    if total_weight > 1.0:
        return jsonify({"error": "Total weight of criteria is greater than 1.0"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert model and get its ID
    cursor.execute('INSERT INTO models (name) VALUES (?)', (model_name,))
    model_id = cursor.lastrowid

    # Insert criteria for the model
    for crit in criteria:
        cursor.execute('''
            INSERT INTO criteria (model_id, field_name, weight, min, max)
            VALUES (?, ?, ?, ?, ?)
        ''', (model_id, crit['field_name'], crit['weight'], crit['min'], crit['max']))

    for df in derived_fields:
        cursor.execute('''
        INSERT INTO derived_fields (model_id, name, formula)
        VALUES (?, ?, ?)
        ''', (model_id, df['name'], df['formula']))


    conn.commit()
    conn.close()

    return jsonify({
        'message': 'Model created successfully',
        'model_id': model_id
        }), 201

# submit opportunity
@app.route('/opportunity', methods=['POST'])
def create_opportunity():
    data = request.json
    model_id = data.get('model_id')
    opportunity_data = data.get('data')

    result = evaluate_opportunity(model_id, opportunity_data)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert opportunity and get its ID
    cursor.execute('''
        INSERT INTO opportunities (model_id, data, score, decision)
        VALUES (?, ?, ?, ?)
    ''', (model_id, json.dumps(opportunity_data), result['score'], result['decision']))
    
    opportunity_id = cursor.lastrowid

    conn.commit()
    conn.close()

    if result['decision'] == "Pursue":
        # Placeholder for pursuing logic (e.g., create tasks, assign team, etc.)
        print(f"Opportunity ID: {opportunity_id} marked for Pursuit")
        # Send email notification
        send_email(opportunity_id, result['score'])

    if result['decision'] == "Review":
        # Placeholder for review logic (e.g., flag for manual review, etc.)
        print(f"Opportunity ID: {opportunity_id} marked for Review")
        # Send email notification
        send_email(opportunity_id, result['score'])


    return jsonify(result), 201

@app.route('/opportunities', methods=['GET'])
def get_opportunities():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM opportunities')
    rows = cursor.fetchall()

    conn.close()

    return jsonify(rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)