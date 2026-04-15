import json
from models import get_db_connection

def normalize(value, min_val, max_val):
    if max_val == min_val:
        return 0.0
    return (value - min_val) / (max_val - min_val)

def evaluate_opportunity(model_id, data):

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch criteria for the model
    cursor.execute("""
        SELECT field_name, weight, min, max 
        FROM criteria 
        WHERE model_id = ?
    """, (model_id,))
    criteria = cursor.fetchall()

    # fetch derived fields for the model
    cursor.execute("""
        SELECT name, formula 
        FROM derived_fields 
        WHERE model_id = ?
    """, (model_id,))
    derived_fields = cursor.fetchall()

    # copy original data to be evaluated
    evaluated_data = data.copy()

    # calculate derived fields
    for name, formula in derived_fields:
        try:
            evaluated_data[name] = eval(formula, {}, evaluated_data)
        except Exception as e:
            evaluated_data[name] = 0

    # calculate total score
    total_score = 0
    breakdown = {}

    for field_name, weight, min_val, max_val in criteria:

        value = evaluated_data.get(field_name, 0)
        normalized_value = normalize(value, min_val, max_val)

        contribution = normalized_value * weight
        total_score += contribution

        breakdown[field_name] = round(contribution, 3)
        
    conn.close()

    # decision logic
    if total_score >= 0.7:
        decision = "Pursue"
    elif total_score >= 0.4:
        decision = "Review"
    else:
        decision = "Reject"


    return {
        "score": round(total_score, 3),
        "decision": decision,
        "evaluated_data": evaluated_data,
        "breakdown": breakdown
        }