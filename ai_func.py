
from openai import OpenAI
import base64
import instructor
from pydantic import BaseModel
from dotenv import dotenv_values
import streamlit as st


class Meal(BaseModel):
    name: str
    calories: int
    protein: int
    carbs: int
    fats: int
    fiber: int

@st.cache_resource
def get_openai_client():
    env = dotenv_values(".env")
    key=st.session_state.get("openai_api_key")
    return OpenAI(api_key=key)

def openAI_response(image):
    

    openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    instructor_openai_client = instructor.from_openai(openai_client)
    
    meal = instructor_openai_client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=Meal,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Wypełnij makroskładniki i kalorie posiłku oraz podaj jego nazwę.", 
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": prepare_image_for_open_ai(image),
                            "detail": "high"
                        },
                    },
                ],
            },
        ],
    )
    return meal

def prepare_image_for_open_ai(image_path):
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    return f"data:image/png;base64,{image_data}"


def fill_meal(image, weight_goal, connection):
    response=[]
    for i in range(4):
        response.append(openAI_response(image))
    #if goal is to lose weigh remove highest calorie response
    if weight_goal == "lose":
        response = sorted(response, key=lambda x: x.calories)
        response.pop()
    #if goal is to gain weight remove lowest calorie response
    elif weight_goal == "gain":
        response = sorted(response, key=lambda x: x.calories, reverse=True)
        response.pop()
    #if goal is to maintain weight remove highest and lowest calorie response
    else:
        response = sorted(response, key=lambda x: x.calories)
        response.pop()
        response.pop()
    #return mean of remaining responses
    return Meal(
        name=response[0].name,
        calories=sum([meal.calories for meal in response]) // len(response),
        protein=sum([meal.protein for meal in response]) // len(response),
        carbs=sum([meal.carbs for meal in response]) // len(response),
        fats=sum([meal.fats for meal in response]) // len(response),
        fiber=sum([meal.fiber for meal in response]) // len(response),
    )
    
