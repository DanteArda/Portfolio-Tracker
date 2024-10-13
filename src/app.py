import streamlit as st
import portfolio

if "Portfolio" not in st.session_state:
    st.session_state.Portfolio = portfolio.Portfolio()
Portfolio = st.session_state.Portfolio

if "Buffer" not in st.session_state:
    st.session_state.Buffer = {}
buffer_api_key_map = st.session_state.Buffer

def _import():
    """Import api_key_map and a Portfolio schema via Cache.py"""
    # TODO

def main():
    """Main"""
    if Portfolio.api_key_map:
        pg = st.navigation([
            st.Page(dashboard, title="Dashboard"),
            st.Page(connect, title="Connect to Broker"),
        ])
    else:
        pg = st.navigation([st.Page(connect, title="Connect to Broker")])

    pg.run()

def connect():
    """Page to connect to retrieve API keys from user"""
    def change_api_key(broker : str):
        api_key = st.text_input("Enter API Key", value=Portfolio.api_key_map[broker]["api_key"] if broker in Portfolio.api_key_map else None)
        
        if st.button("Apply"):
            if api_key:
                with st.spinner("Checking Key"):
                    changed = False

                    if Portfolio.auth_api(broker, api_key):
                        changed = True
                        buffer_api_key_map.update({"Trading212": {"api_key": api_key}})
                
                if changed: st.success("Successfully changed API Key")
                else: st.warning("Warning: API Key was invalid")    

    st.title("Connect to Brokers")
    st.divider()

    # Brokers
    with st.popover("Trading212"):
        change_api_key("Trading212")

    # Write to Portfolio.api_key_map
    if st.button("Apply Changes"):
        if buffer_api_key_map or Portfolio.api_key_map:
            Portfolio.api_key_map = buffer_api_key_map

            st.rerun()
        else:
            st.warning("API Keys can not be left empty!")

def dashboard():
    """Basic Overview of Portfolio"""
    st.title("Dashboard")

if __name__ == "__main__":
    main()