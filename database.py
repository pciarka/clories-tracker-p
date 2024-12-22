import mysql.connector
from mysql.connector import Error
from dotenv import dotenv_values
from typing import Any
import streamlit as st
import streamlit.components.v1 as components

#establish connection, if None is returned, connection failed
@st.cache_resource
def connect_to_db():
    #env = dotenv_values(".env")
    try:
        connection = mysql.connector.connect(
        host=st.secrets['DB_HOST'],        
        user=st.secrets['DB_USER'],        
        password=st.secrets['DB_PASS'],        
        database=st.secrets['DB_NAME'],
        port=st.secrets['DB_PORT'],      
        auth_plugin=st.secrets['DB_AUTH_PLUGIN']
    )
        
        if connection.is_connected():
            return connection
        
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def return_reqest(connection: Any,query: str):
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


def db_login(connection: Any, username: str, password: str):
    results=return_reqest(connection, f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    if results:
        return True
    else:
        return False

def db_login_email(connection: Any, email: str):
    results=return_reqest(connection, f"SELECT * FROM users WHERE email = '{email}'")
    if results:
        usr_id=return_reqest(connection, f"SELECT id FROM users WHERE email = '{st.session_state.email}'")[0][0]
        st.session_state.usr_id = usr_id
        return st.session_state.usr_id
    else:
        if st.session_state.email != '' and st.session_state.usr_id is None:
            st.markdown(f'email {st.session_state.email}')
            st.markdown(f'usr_id {st.session_state.usr_id}')
            
            collect_user_data_gmail()
         
    
    
def collect_user_data_gmail():
    st.header("Write some data please") 
    with st.form("user_data_form"):
    
        goal = st.selectbox("Goal", ["lose", "gain"])
        weight = st.number_input("Weight", min_value=0)
        body_fat = st.number_input("Body fat", min_value=0)
        daily_calories = st.number_input("Daily calories", min_value=0)
        daily_protein = st.number_input("Daily protein", min_value=0)
        daily_carbs = st.number_input("Daily carbs", min_value=0)
        daily_fats = st.number_input("Daily fats", min_value=0)
        daily_fiber = st.number_input("Daily fiber", min_value=0)
  
        submitted = st.form_submit_button("Save data ")

            
        
        # Validation and save
        if submitted:
            # Podstawowa walidacja
            if not goal or not weight or not body_fat or not daily_calories or not daily_protein or not daily_carbs:
                st.error("Fill all data")
                return None
            
            else:
                add_usr(connect_to_db(), st.session_state.email, st.session_state.email, goal, weight, body_fat, daily_calories, daily_protein, daily_carbs, daily_fats, daily_fiber )
                st.success("Success, we are starting! ✅")
                st.rerun()


def add_meal(connection: Any, usr_id: int, meal_name: str, calories: int, protein: int, carbs: int, fats: int, fiber: int):
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO food_intake (user_id, meal_name, calories, protein, carbs, fats, fiber,day) VALUES ({usr_id}, '{meal_name}', {calories}, {protein}, {carbs}, {fats}, {fiber}, CURDATE())")
    connection.commit()
    cursor.close()

def add_usr(connection: Any, email: str, username: str, goal: str, weight: int, body_fat: int, daily_calories: int, daily_protein: int, daily_carbs: int, daily_fats: int, daily_fiber: int):
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO users (email, username, goal, bodyfat, weight, daily_calories, daily_protein, daily_carbs, daily_fats, daily_fiber) VALUES ('{email}', '{username}', '{goal}', '{body_fat}', '{weight}', '{daily_calories}', '{daily_protein}', '{daily_carbs}', '{daily_fats}', '{daily_fiber}')")
    connection.commit()
    cursor.close()
    
    
#void disconnect 
def disconnect(connection:any):
    connection.close()
   
def create_user(connection: Any, username: str, password: str, daily_calories: int, daily_protein: int, daily_carbs: int, daily_fats: int, daily_fiber: int):
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO users (username, password, daily_calories, daily_protein, daily_carbs, daily_fats, daily_fiber) VALUES ('{username}', '{password}', {daily_calories}, {daily_protein}, {daily_carbs}, {daily_fats}, {daily_fiber})")
    connection.commit()
    cursor.close()
    
def db_user_goal(connection: Any, usr_id: int):
    goal_string = return_reqest(connection, f"SELECT goal FROM users WHERE id = {usr_id}")
    return goal_string[0][0]

def user_exists_check_by_email(email):
    db_login_email()

