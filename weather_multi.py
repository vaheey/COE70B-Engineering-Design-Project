from operator import indexOf
import pandas as pd
import math
from pprint import pprint
import time
import matplotlib.pyplot as plt
import numpy as np
import datetime

data_files_2020 = [
    pd.read_csv("data/2020_tor_data.csv"),
    pd.read_csv("data/2020_van_data.csv"),
    pd.read_csv("data/2020_mtl_data.csv"),
    pd.read_csv("data/2020_cal_data.csv"),
    pd.read_csv("data/2020_edm_data.csv"),
    pd.read_csv("data/2020_ham_data.csv"),
    pd.read_csv("data/2020_hfx_data.csv"),
    pd.read_csv("data/2020_kel_data.csv"),
    pd.read_csv("data/2020_kit_data.csv"),
    pd.read_csv("data/2020_lon_data.csv"),
    pd.read_csv("data/2020_osh_data.csv"),
    pd.read_csv("data/2020_ott_data.csv"),
    pd.read_csv("data/2020_peg_data.csv"),
    pd.read_csv("data/2020_qbc_data.csv"),
    pd.read_csv("data/2020_reg_data.csv"),
    pd.read_csv("data/2020_sas_data.csv"),
    pd.read_csv("data/2020_stcath_data.csv"),
    pd.read_csv("data/2020_stjn_data.csv"),
    pd.read_csv("data/2020_vic_data.csv"),
    pd.read_csv("data/2020_win_data.csv"),
    ]

data_files_2021 = [
    pd.read_csv("data/2021_tor_data.csv"),
    pd.read_csv("data/2021_van_data.csv"),
    pd.read_csv("data/2021_mtl_data.csv"),
    pd.read_csv("data/2021_cal_data.csv"),
    pd.read_csv("data/2021_edm_data.csv"),
    pd.read_csv("data/2021_ham_data.csv"),
    pd.read_csv("data/2021_hfx_data.csv"),
    pd.read_csv("data/2021_kel_data.csv"),
    pd.read_csv("data/2021_kit_data.csv"),
    pd.read_csv("data/2021_lon_data.csv"),
    pd.read_csv("data/2021_osh_data.csv"),
    pd.read_csv("data/2021_ott_data.csv"),
    pd.read_csv("data/2021_peg_data.csv"),
    pd.read_csv("data/2021_qbc_data.csv"),
    pd.read_csv("data/2021_reg_data.csv"),
    pd.read_csv("data/2021_sas_data.csv"),
    pd.read_csv("data/2021_stcath_data.csv"),
    pd.read_csv("data/2021_stjn_data.csv"),
    pd.read_csv("data/2021_vic_data.csv"),
    pd.read_csv("data/2021_win_data.csv")
]



PARAMS = [
    "Max Temp (°C)",
    "Min Temp (°C)",
    "Mean Temp (°C)",
    "Heat Deg Days (°C)",
    "Cool Deg Days (°C)",
    "Total Rain (mm)",
    "Total Snow (cm)",
    "Total Precip (mm)",
    "Snow on Grnd (cm)",
]

PARAMS_DATE = [
    "Date/Time",
    "Max Temp (°C)",
    "Min Temp (°C)",
    "Mean Temp (°C)",
    "Heat Deg Days (°C)",
    "Cool Deg Days (°C)",
    "Total Rain (mm)",
    "Total Snow (cm)",
    "Total Precip (mm)",
    "Snow on Grnd (cm)",
]

DATE_ENUM = "Date/Time"

pred_tor_2020 = pd.read_csv("temp_data/2020_tor_data.csv")[PARAMS_DATE]
pred_tor_2021 = pd.read_csv("temp_data/2021_tor_data.csv")[PARAMS_DATE]
pred_tor_2022 = pd.read_csv("temp_data/2022_tor_data.csv")[PARAMS_DATE]
temp_tor_2022 = pd.read_csv("temp_data/2022_tor_data.csv")[PARAMS_DATE]

NUM_OF_PARAMS = len(PARAMS)

def get_mean(arr):
    return [val / 7 for val in arr]

# Predicting any day in 2021
def forecast_day(day,data_21,data_20):
    # if day < 7 or day > 359:
    #     return None, None

    # present_days = data_21.loc[day-7:day-1]
    present_days = data_21[PARAMS]
    present_days = present_days.fillna(0)
    CD = present_days.to_numpy()

    # prev_days = data_20.loc[day-7:day+6]
    prev_days = data_20[PARAMS]

    prev_days = prev_days.fillna(0)
    PD = prev_days.to_numpy()

    windows = []
    for i in range(len(PD) - 6):
        windows.append(PD[i: i+7])

    # calculating means for present year 7 days
    present_sums = [0] * NUM_OF_PARAMS
    for line in CD:
        for i in range(len(line)):
            if not math.isnan(line[i]): present_sums[i] += line[i] 
    present_means = get_mean(present_sums)

    # mean of parameters for each window
    ed_list = []
    for window in windows:
        prev_sums = [0] * NUM_OF_PARAMS
        for vals in window:
            for i in range(len(prev_sums)):
                prev_sums[i] += vals[i]
        prev_means = get_mean(prev_sums)

        euclid_distance = sum([(present_means[i] - prev_means[i]) ** 2 for i in range(len(present_means))])
        ed_list.append(euclid_distance)

    min_ed = min(ed_list)
    index_min_ed = indexOf(ed_list, min_ed)
    selected_prev_window = windows[index_min_ed]

    present_variation_vector = []
    for i in range(len(CD[0])):
        vector = []
        for j in range(len(CD)-1):
            vector.append(CD[j+1][i] - CD[j][i])
        present_variation_vector.append(vector)

    prev_variation_vector = []
    for i in range(len(selected_prev_window[0])):
            vector = []
            for j in range(len(selected_prev_window)-1):
                vector.append(selected_prev_window[j+1][i] - selected_prev_window[j][i])
            prev_variation_vector.append(vector)
    
    mean_present_var = []
    for i in range(len(present_variation_vector)):
        mean_present_var.append(sum(present_variation_vector[i]) / len(present_variation_vector[i]))

    mean_prev_var = []
    for i in range(len(prev_variation_vector)):
        mean_prev_var.append(sum(prev_variation_vector[i]) / len(prev_variation_vector[i]))

    mean_variation_vector = []
    for i in range(len(mean_present_var)):
        mean_variation_vector.append((mean_present_var[i] + mean_prev_var[i]) / 2)
    
    prev_day = CD[-1]
    for i in range(len(prev_day)):
        prev_day[i] += mean_variation_vector[i]
    pred_arr = prev_day.tolist()
    
    for i in range(len(pred_arr[5:])):
        if pred_arr[5+i] < 0:
            pred_arr[5+i] = 0

    # actual_data = data_21.loc[day]
    # actual_data = actual_data.fillna(0)
    # actual_values = actual_data[PARAMS].to_numpy().flatten()
    pred_arr.insert(0, day)

    return pred_arr

if __name__ == "__main__":
    t0 = time.time()

    pred_main = pd.concat([pred_tor_2020, pred_tor_2021], ignore_index=True)
    pred_main = pd.concat([pred_main, pred_tor_2022.loc[0:7]], ignore_index=True)

    curr_date = datetime.date(2022, 1, 9)

    for i in range(365):
        day_index = len(pred_main) - 1
        prev_index = day_index - 365
        seven_day_data = pred_main.loc[day_index-6:day_index]
        prev_day_data = pred_main.loc[prev_index-6:prev_index+7]

        # print()
        temp_pred = forecast_day(curr_date.isoformat(), seven_day_data, prev_day_data)
        temp_pred = np.array(temp_pred, dtype=object)
        temp_df = pd.DataFrame([temp_pred], columns=PARAMS_DATE)
        pred_main = pd.concat([pred_main, temp_df], ignore_index=True)

        curr_date += datetime.timedelta(days=1)

    print(f"\nTotal time: {time.time() - t0}")



    # Plotting
    temp_start_date = datetime.date(2022, 1, 1)
    temp_end_date = datetime.date(2022, 1, 31)

    temp_start_index = pred_main.index[pred_main[PARAMS_DATE[0]] == temp_start_date.isoformat()][0]
    temp_end_index = pred_main.index[pred_main[PARAMS_DATE[0]] == temp_end_date.isoformat()][0]

    temp_data = pred_main.loc[temp_start_index:temp_end_index]

    temp_actual_data = temp_tor_2022[PARAMS]
    temp_actual_data = temp_actual_data.loc[0:30]

    n = np.arange(0, len(temp_data))

    pprint(temp_actual_data[PARAMS[8]])

    temp_mean = np.transpose(temp_data[PARAMS[8]])
    temp_actual_mean = np.transpose(temp_actual_data[PARAMS[8]])

    plt.plot(n, temp_mean, color='blue')
    plt.plot(n, temp_actual_mean, color='red')

    plt.show()
