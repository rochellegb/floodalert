import pandas as pd
from datetime import datetime

engine = 'sqlite:///data.db'

flood_data = pd.read_sql("SELECT * FROM Announcements", con=engine)
flood_data.head()


def separate_database_datetime():
    # splits data from time
    time = flood_data["time_posted"].str.split(" ", n=1, expand=True)
    flood_data["time"] = time[1]
    flood_data["date"] = time[0]

    # splits date(d,m,y)
    sep_date = flood_data["date"].str.split("/", n=2, expand=True)
    flood_data["month"] = sep_date[0]
    flood_data["day"] = sep_date[1]
    flood_data["year"] = sep_date[2]

    # splits hour from minutes
    sep_hour = flood_data["time"].str.split(":", n=1, expand=True)
    flood_data["hour"] = sep_hour[0]
    flood_data["minutes"] = sep_hour[1]


def plot_daily(month, day, year):
    separate_database_datetime()
    daily = flood_data[(flood_data['day'] == day) & (flood_data['month'] == month) & (flood_data['year'] == year)]
    daily_data = daily.groupby("hour", as_index=False).mean()
    data = daily_data.to_dict('records')
    return data


def plot_monthly(month, year):
    separate_database_datetime()
    monthly = flood_data[(flood_data['month'] == month) & (flood_data['year'] == year)]
    monthly_data = monthly.groupby("day", as_index=False).mean()
    data = monthly_data.to_dict('records')
    return data


def plot_yearly(year):
    separate_database_datetime()
    yearly = flood_data[(flood_data['year'] == year)]
    yearly_data = yearly.groupby("month", as_index=False).mean()
    data = yearly_data.to_dict('records')
    return data










