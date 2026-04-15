### Opportunity_Evaluation_Project


## Overview:

This project is a backend system that is designed to help businesses evaluate incoming opportunities and decide which ones are worth pursuing. The system processes submitted opportunities, calculates a score based on user-defined parameters, and identifies whether opportunites are worth pursuing, not worth pursuing, or need to be reviewed further by personnel. Once a user has entered all defining criteria for an opportunity, it can be automatically scored and sent to an email of the user's choosing.



## Main Project Features:

* Dynamic Evaluation Models
* Weighted scoring system 
* Derived fields using user-created formulas
* Automated evaluation with detailed scoring breakdown
* Email Notifications


## Tech Stack:

* Python
* Flask
* SQLite
* SendGrid (Email API)


## Setup Instructions (using Visual Studio Code):

# 1) Clone the github repository by entering the following into your terminal:
* git clone https://github.com/HectorAVJr/Opportunity_Evaluation_Project
* cd Opportunity_Evaluation_Project

# 2) Create virtual environment (if not already active) by entering the following into your terminal:
* python -m venv venv
* venv\Scripts\activate 
* (Restarting VS Code and the terminal is sometimes necessary after these steps)


# 3) Install dependencies located in 'requirements.txt' by entering this into your terminal:
* pip install -r requirements.txt

# 4) Configure environment variable (SendGrid API key):
* setx SENDGRID_API_KEY "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"
* Restart VS Code after the terminal says "SUCCESS: Specified value was saved."

# 5) Running the backend system by entering the following into your terminal:
* python app.py (Server will be running at http://127.0.0.1:5000)

# 6) Instructions for using the API:
* Go to the 'requests.http' file to view a step by step guide on how to create a model with user-determined criteria and how to submit an opportunity with user-specified values. 
* This is an example of what the inputted format should look like:


### Example Model

"### Example Model

send request

POST http://127.0.0.1:5000/model

Content-Type: application/json

{

  "name": "Multi Factor Model",
  
  "criteria": [
  
    {
    
    "field_name": "profit_margin",
    
    "weight": 0.5,
    
    "min": 0,
    
      "max": 1
      
       },
       
    {
    
    "field_name": "risk_score",
    
      "weight": 0.25,
      
      "min": 0,
      
      "max": 10
      
      },
      
    {
        "field_name": "customer_satisfaction",
        "weight": 0.25,
        "min": 1,
        "max": 5
    }
    
  ],
  
  "derived_fields": [
  
    {
      "name": "profit_margin",
      "formula": "(revenue - cost) / revenue"
    },
    {
        "name": "risk_score",
        "formula": "10 - risk"
    },
    {
        "name": "customer_satisfaction",
        "formula": "rating / 5"
    }
  ]
}"



* Once Model has been written, the database will save an ID number to the Model along with all associated criteria and derived fields when the user clicks the 'request' button above the POST address at the top of the Model.
* After the Model has been created and given an ID, an opportunity can be written by the user. 



"### Example Model Test

POST http://127.0.0.1:5000/opportunity

Content-Type: application/json

{

  "model_id": 1,
  
  "email": "email@example.com",
  
  "data": {
  
    "revenue": 40000,
    
    "cost": 5000,
    
    "risk": 2,
    
    "rating": 5
    
  }
  
}"



* When the user has written an opportunity with all required information then the user must click 'request' above the POST address to submit the opportunity for evaluation.
* When the opportunity evaluation is complete, the scoring and recommended decision regarding the submitted opportunity will be displayed to the user and an email will be sent to the email that the user entered in the "email" field. 



Evaluation Logic:
* The criteria is normalized using its min value and max value range
* The scoring is weighted based on user-defined importance
* Final evaluation score determines the recommended decision:
- "Pursue" recommendation is given when a score is 0.7 to 1.0
- "Reject" recommendation is given when a score is 0.0 to 0.39..
- "Review" recommendation is given when a score is 0.4 to 0.69..



Email Notifications:
After an opportunity is evaluated, the system sends an email with the following:
* Opportunity ID
* Evaluation score
* Recommended decision
* Breakdown of the criteria
* Evaluated data



Design Decisions:
* Configurable Models: Allows users from different industries to define their own evaluation logic.
* Weighted Scoring: Gives users flexibility and the ability to prioritize certain factors over others
* Derived Fields: Enables users to define their own formulas to further allow flexibility
* Email Notifications: The API-based emailing uses SendGrid for free and reliable delivery



References:
* SendGrid online set up and implementing guide: https://app.sendgrid.com/guide , https://www.youtube.com/watch?v=QHxhNu-T9mE 
* Debugging assistance: ChatGPT (OpenAI)
* Flask set up and guide: https://www.geeksforgeeks.org/python/flask-creating-first-simple-application/ , https://www.youtube.com/watch?v=IfWZHjsPeHg&t=1181s




Contact:

Developer: Hector Velazquez Jr. (HectorAVJr)

Project: https://github.com/HectorAVJr/Opportunity_Evaluation_Project
