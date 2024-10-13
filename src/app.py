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
            st.Page(market_benchmark, title="Benchmark Portfolio"),
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

            Portfolio.read()

            st.rerun()
        else:
            st.warning("API Keys can not be left empty!")

def dashboard():
    """Basic Overview of Portfolio"""
    st.title("Dashboard")
    st.divider()

    # Basic Information Display
    portfolio_value_display, dividend_display = st.columns(2)

    with portfolio_value_display:
        st.metric(
            label="Portfolio Value",
            value="{}{:.2f}".format(Portfolio.Cash.currency_symbol, Portfolio.Cash.total),
            delta="{}{:.2f} ({:.2f}%)".format(Portfolio.Cash.currency_symbol, Portfolio.Cash.ppl, Portfolio.Cash.ppl_pc),
            )
        st.caption("Initial Investment: {}{:.2f}".format(Portfolio.Cash.currency_symbol, Portfolio.Cash.invested))
    
    with dividend_display:
        st.metric(
            label="Total Dividends",
            value="{}{:.2f}".format(Portfolio.Cash.currency_symbol, Portfolio.Cash.dividend_total), 
            delta="{}{:.2f}".format(Portfolio.Cash.currency_symbol, Portfolio.Cash.last_dividend) ,
            delta_color="off"
            )
        st.caption("Realized Gains: {}{:.2f}".format(Portfolio.Cash.currency_symbol, Portfolio.Cash.result))

    st.divider()

    # Asset Allocation
    st.progress(70, text="Cash")
    st.progress(20, text="Stocks")
    st.progress(10, text="Crypto")

def market_benchmark():
    st.title("Benchmark Portfolio")
    st.divider()

if __name__ == "__main__":
    main()