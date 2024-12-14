import streamlit
import file_handler
import portfolio_generator
import api_interface

if "logged_in" not in streamlit.session_state:
    streamlit.session_state.logged_in = False

def login():
    streamlit.title("API Key Input")
    api_input = streamlit.text_input("Trading212 API Key Input")
    if streamlit.button("Confirm"):
        if api_input:
            streamlit.session_state.logged_in = True
    
        else:
            streamlit.warning("No API Key")

def dashboard():
    streamlit.title("Dashboard")

login_page = streamlit.Page(login)
dashboard_page = streamlit.Page(dashboard)

if streamlit.session_state.logged_in:
    pg = streamlit.navigation(
        {
            "Your Portfolio": [dashboard_page]
        }
    )

else:
    pg = streamlit.navigation([login_page])

pg.run()