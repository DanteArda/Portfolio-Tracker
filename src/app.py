import file_handler
import os
from portfolio_generator import Portfolio
import api_interface
import api_server

# init
Config_ini = file_handler.Config.Ini()
Config_json = file_handler.Config.Json()

if Config_ini.has_platform("Trading212"):
    print("Got API key from .ini file")
    api_key = Config_ini.get("Trading212")

else:
    while True:
        api_key = input("Please enter your API key:\n")
        Config_ini.set("Trading212", api_key)
        Config_ini.save()
        break

print("Writing to local Portfolio")
Trading212_Portfolio = Portfolio()

if Config_json.has_platform("Trading212") and Config_json.is_outdated("Trading212"):
    Portfolio.write(Trading212_Portfolio.Cash, Config_json.get("Trading212"))

else:
    Trading212 = api_server.Trading212(api_key)

    Hook = api_interface.Hook(Trading212, Trading212_Portfolio)
    Hook.write_cash()

    Config_json.save(Portfolio.filter_attributes(Trading212_Portfolio.Cash), "Trading212")

def dashboard():
    Cash = Trading212_Portfolio.Cash
    print(f"""
    Free Funds: {Cash.free}
    Invested: {Cash.invested}
    Profit and Loss: {Cash.profit_and_loss}
    Realized Gains: {Cash.realized}
    Total Value: {Cash.total}
    """)

def main():
    dashboard()

main()


