import streamlit as st
from database import return_reqest, connect_to_db, add_meal , db_user_goal
from login_screen import login
from ai_func import fill_meal, Meal
import tempfile

st.set_page_config(initial_sidebar_state="expanded", page_title="Calories Tracker")

class CalorieAndMacroToday:
    calories: int
    protein: int
    carbs: int
    fats: int
    fiber: int
    
def empty_calories_today():
    temp=CalorieAndMacroToday()
    temp.calories=0
    temp.protein=0
    temp.carbs=0
    temp.fats=0
    temp.fiber=0
    return temp   



def custom_progress_bar(current, goal, label):
    goal = max(goal, 1)
    percentage = min(current / goal, 1)  # Cap percentage at 1 (100%)
    
    if percentage <1:
        st.progress(percentage)
        st.write(f"{label}")
    else:
        st.progress(0.999)
        st.markdown(f"<span style='color:red'>{label}</span>", unsafe_allow_html=True)


def fill_calories_today(connection, usr_id,class_calories):
    
    results = return_reqest(connection, f"SELECT * FROM food_intake WHERE user_id = {usr_id} and day = CURDATE()")
    
    for result in results:
        class_calories.calories+=result[2]
        class_calories.protein+=result[3]
        class_calories.carbs+=result[4]
        class_calories.fats+=result[5]
        class_calories.fiber+=result[6]
    return class_calories


def main():

    #general session state variables
    if 'usr_intake' not in st.session_state:
        st.session_state.usr_intake = empty_calories_today()
    
    if 'usr_id' not in st.session_state:
        st.session_state.usr_id = None

    if st.session_state.usr_id is None:
       st.session_state.usr_id = login()

    if st.session_state.usr_id is not None:
        connection=connect_to_db()
        
    if 'cur_meal' not in st.session_state:
        st.session_state.cur_meal = Meal(
            name="Add your meal",
            calories=0,
            protein=0,
            carbs=0,
            fats=0,
            fiber=0
        )



    # welcome to log user
    if st.session_state.usr_id is not None:
        connection=connect_to_db()  
        username = return_reqest(connection, f"SELECT username FROM users WHERE id = {st.session_state.usr_id}")
        st.markdown(f"### Welcome, {username[0][0]}")

        Meals, Today=st.tabs(["Add meal", "Today data"])
     
        with Today:
            # calories progress bars
            # if st.session_state.usr_id is not None:
            # username = return_reqest(connection, f"SELECT username FROM users WHERE id = {st.session_state.usr_id}")
            # st.markdown(f"### Welcome, {username[0][0]}")
            st.write("Here is your calories and macro for today")
        
            results = return_reqest(connection, f"SELECT daily_calories, daily_protein, daily_carbs, daily_fats, daily_fiber FROM users WHERE id = {st.session_state.usr_id}")
            daily_goals = results[0]
        
            st.session_state.usr_intake=empty_calories_today()
            st.session_state.usr_intake = fill_calories_today(connection, st.session_state.usr_id, st.session_state.usr_intake)  
        
        
            st.write("Calories Intake")
            custom_progress_bar(st.session_state.usr_intake.calories, daily_goals[0], 
                                f"{st.session_state.usr_intake.calories} / {int(daily_goals[0])} kcal")
            
            st.write("Protein Intake")
            custom_progress_bar(st.session_state.usr_intake.protein, daily_goals[1], 
                                f"{st.session_state.usr_intake.protein} / {int(daily_goals[1])} g")
            
            st.write("Carbs Intake")
            custom_progress_bar(st.session_state.usr_intake.carbs, daily_goals[2], 
                                f"{st.session_state.usr_intake.carbs} / {int(daily_goals[2])} g")
            
            st.write("Fats Intake")
            custom_progress_bar(st.session_state.usr_intake.fats, daily_goals[3], 
                                f"{st.session_state.usr_intake.fats} / {int(daily_goals[3])} g")
            
            st.write("Fiber Intake")
            custom_progress_bar(st.session_state.usr_intake.fiber, daily_goals[4], 
                                f"{st.session_state.usr_intake.fiber} / {int(daily_goals[4])} g")
       
        with Meals:
        # if st.session_state.usr_id is not None:
            # adding meals from photo
            option = st.selectbox("Choose an option", ("Take a picture from camera", "Upload a photo" ))
            image = None
            

            if option == "Take a picture from camera":
                image = st.camera_input("Take a picture")
            elif option == "Upload a photo":
                image = st.file_uploader("Upload a photo", type=["png", "jpg", "jpeg"])

            if image is not None:
                st.image(image, use_container_width=True)


            # Save the uploaded file to a temporary location
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(image.getbuffer())
                    tmp_file_path = tmp_file.name

            # Pass the file path to the fill_meal function
                st.session_state.cur_meal = fill_meal(tmp_file_path, db_user_goal(connection, st.session_state.usr_id), connection)
            
                
            #manually adding meals
            st.write("Add a meal")
            meal_name = st.text_input("Meal name", value=st.session_state.cur_meal.name) 
            calories = st.number_input("Calories", value=st.session_state.cur_meal.calories, min_value=0)
            protein = st.number_input("Protein", value=st.session_state.cur_meal.protein, min_value=0)
            carbs = st.number_input("Carbs", value=st.session_state.cur_meal.carbs, min_value=0)
            fats = st.number_input("Fats", value=st.session_state.cur_meal.fats, min_value=0)
            fiber = st.number_input("Fiber", value=st.session_state.cur_meal.fiber, min_value=0)
            
            
            if st.button("Add"):
                add_meal(connection, st.session_state.usr_id, meal_name, calories, 
                         protein, carbs, fats, fiber)
                st.session_state.usr_intake = empty_calories_today()
                st.session_state.usr_intake = fill_calories_today(connection, st.session_state.usr_id, 
                                                                  st.session_state.usr_intake)
                st.success("Meal added successfully")
                st.session_state.cur_meal = Meal(
                    name="Add your meal",
                    calories=0,
                    protein=0,
                    carbs=0,
                    fats=0,
                    fiber=0
                )
                image = None
                st.rerun()
                

            if image is not None:
                with open("captured_image.png", "wb") as f:
                    f.write(image.getbuffer())
            
            

if __name__ == "__main__":
    main()
