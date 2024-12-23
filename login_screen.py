from database import connect_to_db, db_login, return_reqest, db_login_email
import streamlit as st
from st_paywall import add_auth  # type: ignore


def login():
    login_screen_g()
    # login_screen()
    return st.session_state.usr_id

def login_screen():
    with st.sidebar: 
        st.markdown('### or please login by username')
        username = st.text_input('Username')
        password = st.text_input('Password', type='password')
        if st.button('Login'):
            connection = connect_to_db()
        
            if db_login(connect_to_db(), username, password):
                st.success('Login successful')
                st.session_state.usr_id = return_reqest(connect_to_db(), f"SELECT id FROM users WHERE username = '{username}' AND password = '{password}'")[0][0]
            else:
                st.error('Incorrect password or username')

        return st.session_state.usr_id
       
def login_screen_g():
    
        try:
            add_auth(
            required=False,
            login_sidebar=True,
            login_button_text="Log by Google",
            

            )
      
        
        except KeyError:
            pass

        
        if st.session_state.get('email'):
            # st.markdown(f"You logged by: {st.session_state['email']}")
            
            if db_login_email(connect_to_db(), st.session_state.email): 
            # st.success("User exist!") 
                st.query_params.update(logged_in=True)

        
        return st.session_state.usr_id

    