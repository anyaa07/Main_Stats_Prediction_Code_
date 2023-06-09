# figure out how to incorporate team record
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# !pip install -q streamlit
# load data
url = "https://raw.githubusercontent.com/anyaa07/QBs/main/QB20.csv"
url2 = "https://raw.githubusercontent.com/anyaa07/QBs/main/QB21.csv"
url3 = "https://raw.githubusercontent.com/anyaa07/QBs/main/QB22.csv"

# Read the CSV file into a DataFrame
QB20 = pd.read_csv(url)
QB21 = pd.read_csv(url2)
QB22 = pd.read_csv(url3)

# merge data
QB21_2 = QB21.rename(
    columns={'Pass': 'Pass Yds', 'TD2': 'TD', 'INT2': 'INT', 'Att2': 'Att', 'Comp2': 'Comp', 'Year2': 'Year'})
QB20_2 = QB20.rename(columns={'TDs': 'TD', 'INTs': 'INT', 'Year3': 'Year'})
merged = pd.concat([QB20_2, QB21_2], axis=0, ignore_index=True)
merged2 = pd.concat([QB21_2, QB22], axis=0, ignore_index=True)
data = pd.merge(QB20, QB21, on=['Player', 'Team'])
data1 = pd.merge(data, QB22, on=['Player', 'Team'])

# data2 = pd.merge(data, Records, on='Team')

# create linear regression model
model = LinearRegression()
# loop through each player
for player in data1['Player'].unique():
    # fit model to player data, merge 20 and 21 for x, 21 and 22 for y
    X = merged[['Pass Yds', 'TD', 'INT', 'Comp', 'Att']]
    y = merged2[['Pass Yds', 'TD', 'INT', 'Comp', 'Att']]
    model.fit(X, y)

# predict 2023-24 season stats
predicted_stats = model.predict(QB22[['Pass Yds', 'TD', 'INT', 'Comp', 'Att']])

# assign predicted statistics to the corresponding columns -- (wont change)
# mask --> selects only the rows of data that correspond to the current player that is being looped through
# enumerate --> gets the index of each of the selected rows where the players name matches the player variable, and assigns predicted stats only to the correct rows
pass_yd_pts = 0.04
pass_td_pts = 4
int_pts = -2
for index, player in enumerate(data1['Player'].unique()):
    mask = (data1['Player'] == player)
    data1.loc[mask, 'Pass Yds_2023_24'] = predicted_stats[index][0]
    data1.loc[mask, 'TD_2023_24'] = predicted_stats[index][1]
    data1.loc[mask, 'INT_2023_24'] = predicted_stats[index][2]
    data1.loc[mask, 'Comp_2023_24'] = predicted_stats[index][3]
    data1.loc[mask, 'Att_2023_24'] = predicted_stats[index][4]
    # may change
    fantasy_points = data1['Pass Yds_2023_24'] * pass_yd_pts + data1['TD_2023_24'] * pass_td_pts + data1[
        'INT_2023_24'] * int_pts
    data1.loc[mask, 'Fantasy_Points'] = predicted_stats[index][4]
# QBR Calculation (wont change)
cp = (data1['Comp_2023_24'] / data1['Att_2023_24'] - 0.3) * 0.05
ypa = (data1['Pass Yds_2023_24'] / data1['Att_2023_24'] - 3) * 0.25
tdp = (data1['TD_2023_24'] / data1['Att_2023_24']) * 0.2
intp = (data1['INT_2023_24'] / data1['Att_2023_24']) * 0.25

data1['QBR'] = ((data1['Comp_2023_24'] - 30) / 20 + ((data1['Pass Yds_2023_24'] / data1['Att_2023_24']) - 3) * 0.25 + (
data1['TD_2023_24']) * 0.2 + 2.375 - (data1['INT_2023_24'] * 0.25)) * 100 / 6 / 3
selected_columns = data1[
    ['Team', 'Player', 'Pass Yds_2023_24', 'TD_2023_24', 'INT_2023_24', 'Comp_2023_24', 'Att_2023_24', 'QBR',
     'Fantasy_Points']]
# print the modified data frame
print(selected_columns)
# mean_absolute_error(y, predicted_stats)
# mean_squared_error(y, predicted_stats)