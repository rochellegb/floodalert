import pandas as pd

data = pd.read_csv('flood data.csv')
engine = 'sqlite:///data.db'
data.to_sql('Announcements', con=engine, if_exists='append', index=False)
