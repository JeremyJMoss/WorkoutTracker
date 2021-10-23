from datetime import datetime
import requests

NUTRIONIX_API_KEY = "your nutrionix api key00"
NUTRIONIX_APP_ID = "your Nutrionix app id"
EXERCISE_END_POINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_END_POINT = "your sheety endpoint"
GENDER = "your gender here"
SHEET_TOKEN = "your sheety token here"
EXERCISE_TEXT = input("Tell me what exercises you did: ")

exercise_params = {
    "query": EXERCISE_TEXT,
    "gender": GENDER,
    "weight_kg": 88.8,
    "height_cm": 180.1,
    "age": 27
}

headers = {
    "x-app-id": NUTRIONIX_APP_ID,
    "x-app-key": NUTRIONIX_API_KEY
}

response = requests.post(EXERCISE_END_POINT, json=exercise_params, headers=headers)
result = response.json()["exercises"]

exercise_list = {
    "name": [],
    "duration": [],
    "calories_burnt": []
}

for exercise in result:
    exercise_list["name"].append(exercise["name"])
    exercise_list["duration"].append(exercise["duration_min"])
    exercise_list["calories_burnt"].append(exercise["nf_calories"])

sheet_headers = {
    "authorization": f"Bearer {SHEET_TOKEN}"
}

for index in range(0, len(exercise_list["name"])):
    workout_row = {
        "workout": {
            "date": datetime.now().strftime("%d/%m/%Y"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "exercise": exercise_list["name"][index].title(),
            "duration": str(int(exercise_list["duration"][index])),
            "calories": exercise_list["calories_burnt"][index]
        }
    }

    sheet_response = requests.post(SHEETY_END_POINT, json=workout_row, headers=sheet_headers)
    print(sheet_response.text)
