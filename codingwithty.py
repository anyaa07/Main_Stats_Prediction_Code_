# figure out how to incorporate team record
import pandas as pd
from sklearn.linear_model import LinearRegression

pd.set_option('display.max_columns', None)
# load data & Read the CSV file into a DataFrame


def load_data(url_1, url_2, url_3):
    QB20 = pd.read_csv(url_1)
    QB21 = pd.read_csv(url_2)
    QB22 = pd.read_csv(url_3)
    dataframes = [QB20, QB21, QB22]
    return dataframes


def main():
    url = "https://raw.githubusercontent.com/anyaa07/QBs/main/QB20.csv"
    url2 = "https://raw.githubusercontent.com/anyaa07/QBs/main/QB21.csv"
    url3 = "https://raw.githubusercontent.com/anyaa07/QBs/main/QB22.csv"
    data_frames = load_data(url, url2, url3)
    # merge data
    QB21 = data_frames[1].rename(
        columns={'Pass': 'Pass Yds', 'TD2': 'TD', 'INT2': 'INT', 'Att2': 'Att',
                 'Comp2': 'Comp', 'Year2': 'Year'})
    QB20 = data_frames[0].rename(columns={'TDs': 'TD', 'INTs': 'INT',
                                          'Year3': 'Year'})
    merged = pd.concat([QB20, QB21], axis=0, ignore_index=True)
    merged2 = pd.concat([QB21, data_frames[2]], axis=0, ignore_index=True)
    data = pd.merge(QB20, QB21, on=['Player', 'Team'])
    data1 = pd.merge(data, data_frames[2], on=['Player', 'Team'])
    mergedDF = [merged, merged2, data1, data]
    return mergedDF

    # create linear regression model


def modeldefined(mergedDF, dataframes):
    model = LinearRegression()
    # loop through each player
    for player in mergedDF[3]['Player'].unique():
        # fit model to player data, merge 20 and 21 for x, 21 and 22 for y
        X = mergedDF[0][['Pass Yds', 'TD', 'INT', 'Comp', 'Att']]
        y = mergedDF[1][['Pass Yds', 'TD', 'INT', 'Comp', 'Att']]
        model.fit(X, y)

        # predict 2023-24 season stats
        predicted_stats = model.predict(
            dataframes[2][['Pass Yds', 'TD', 'INT', 'Comp', 'Att']])
        defined_models = [predicted_stats]
        return defined_models

    # assign predicted statistics to the corresponding columns -- (wont change)
    # mask --> selects only the rows of data that correspond to the current
    # player that is being looped through enumerate --> gets the index of each
    # of the selected rows where the players name matches the player variable,
    # and assigns predicted stats only to the correct rows


def columns(defined_models, mergedDF):
    pass_yd_pts = 0.04
    pass_td_pts = 4
    int_pts = -2
    for index, player in enumerate(defined_models[0]['Player'].unique()):
        mask = (mergedDF[2]['Player'] == player)
        mergedDF[2].loc[mask, 'Pass Yds_2023_24'] = defined_models[0][index][0]
        mergedDF[2].loc[mask, 'TD_2023_24'] = defined_models[0][index][1]
        mergedDF[2].loc[mask, 'INT_2023_24'] = defined_models[0][index][2]
        mergedDF[2].loc[mask, 'Comp_2023_24'] = defined_models[0][index][3]
        mergedDF[2].loc[mask, 'Att_2023_24'] = defined_models[0][index][4]
            # may change
        fantasy_points = mergedDF[2]['Pass Yds_2023_24'] * pass_yd_pts + mergedDF[2][
            'TD_2023_24'] * pass_td_pts + mergedDF[2][
                                'INT_2023_24'] * int_pts
        mergedDF[2].loc[mask, 'Fantasy_Points'] = defined_models[0][index][4]
        # QBR Calculation (wont change)

    mergedDF[2]['QBR'] = ((mergedDF[2]['Comp_2023_24'] - 30) / 20 + (
            (mergedDF[2]['Pass Yds_2023_24'] / mergedDF[2]['Att_2023_24']) - 3) * 0.25 + (
                                mergedDF[2]['TD_2023_24']) * 0.2 + 2.375 - (
                                    mergedDF[2]['INT_2023_24'] * 0.25)) * 100 / 6 / 3
    selected_columns = mergedDF[2][
        ['Team', 'Player', 'Pass Yds_2023_24', 'TD_2023_24', 'INT_2023_24',
            'Comp_2023_24', 'Att_2023_24', 'QBR',
            'Fantasy_Points']]
        # print the modified data frame
    print(selected_columns)


if __name__ == '__main__':
    main()
