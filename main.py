import os


import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
user_name = os.environ['USERNAME']
password = os.environ['PASSWORD']


basic = HTTPBasicAuth(user_name, password)
# requests.get('https://httpbin.org/basic-auth/user/pass', auth=basic)

NUTRITION_KEY = os.environ['NUTRITION_PASSWORD']
NUTRITION_API_KEY = os.environ['NUTRITION_API']


# for parameters
GENDER = "MALE"
WEIGHT = 60
HEIGHT = 182
AGE = 30
EXERCISE_QUESTION = input("What did you do?: \n").title()

NUTRITION_ID = NUTRITION_KEY

NLN_ENDPOINT = 'https://trackapi.nutritionix.com/v2/natural/exercise'

headers = {
    'Content-Type': 'application/json',
    'x-app-id': NUTRITION_ID,
    'x-app-key':NUTRITION_API_KEY
  }

NUTRITION_DATA = {
    "query": EXERCISE_QUESTION,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,}


nln_endpoint = requests.post(url=NLN_ENDPOINT,json=NUTRITION_DATA,headers=headers)
nln_endpoint.raise_for_status()
result = nln_endpoint.json()
print(result)


# to create row using sheety
sheet_endpoint = os.environ["SHEET_ENDPOINT"]
#
today_date = datetime.now().strftime("%d/%m/%Y")
time_now = datetime.now().strftime("%X")


print(today_date)
print(time_now)
#introduce authentication

for exercise in result['exercises']:

    sheet_inputs = {
      "workout": {
        "date": today_date,
        "time": time_now,
        "duration": exercise['duration_min'],
        "exercise": exercise["name"].title(),
        "calories": exercise['nf_calories'],
        "description": exercise['description']


      }
    }

    response = requests.post(sheet_endpoint,json= sheet_inputs, auth=basic)
    print(response.text)


