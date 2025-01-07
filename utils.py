import pandas as pd

def load_ev_sales_data():
    df = pd.read_csv("https://api.iea.org/evs?parameters=EV%20sales&category=Historical&mode=Cars&csv=true")
    ev_sales_df = df[df["parameter"]=="EV sales"]
    return ev_sales_df

def load_ev_charging_points_data():
    ev_charging_points_df = pd.read_csv("https://api.iea.org/evs?parameters=EV%20charging%20points&category=Historical&mode=EV&csv=true")
    return ev_charging_points_df
