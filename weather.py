from operator import indexOf
import pandas as pd
import math
from pprint import pprint
import time
import matplotlib.pyplot as plt
import numpy as np

data_files_2020 = [
    pd.read_csv("data/2020_data.csv"),
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
    pd.read_csv("data/2021_data.csv"),
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

NUM_OF_PARAMS = len(PARAMS)

def get_mean(arr):
    return [val / 7 for val in arr]

# Predicting any day in 2021
def forecast_day(day,data_21,data_20):
    if day < 7 or day > 360:
        return None, None

    present_days = data_21.loc[day-7:day-1]
    present_days = present_days[PARAMS]
    present_days = present_days.fillna(0)
    CD = present_days.to_numpy()

    prev_days = data_20.loc[day-7:day+6]
    prev_days = prev_days[PARAMS]

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

    actual_data = data_21.loc[day]
    actual_data = actual_data.fillna(0)
    actual_values = actual_data[PARAMS].to_numpy().flatten()

    return actual_values, pred_arr

if __name__ == "__main__":
    t0 = time.time()
    day_range = np.arange(0, 365)
    actual_list = [[] for i in range(20)]
    pred_list = [[] for i in range(20)]


    for day in day_range:
        for i in range(len(pred_list)):
            temp_actual, temp_pred = forecast_day(day,data_files_2021[i],data_files_2020[i])

            if temp_pred:
                actual_list[i].append(list(temp_actual))
                pred_list[i].append(list(temp_pred))

            else:
                actual_list[i].append([0] * NUM_OF_PARAMS)
                pred_list[i].append([0] * NUM_OF_PARAMS)

    print(f"\nTotal time: {time.time() - t0}")

    toronto_actual_data = np.transpose(actual_list[0])
    toronto_pred_data = np.transpose(pred_list[0])


    plt.figure()
    plt.subplot(1, 3, 1)
    plt.gcf().set_size_inches(20,12)

    index = 0
    for param in PARAMS:
        plt.subplot(2, 5, index+1)
        plt.plot(day_range, toronto_actual_data[index], label='Toronto Actual', color = "red")
        plt.plot(day_range, toronto_pred_data[index], label='Toronto Prediction', color = "blue")
        plt.ylim(-20, 40)
        plt.title(f"{param}")
        plt.legend(['Toronto Actual', 'Toronto Prediction'])
        index += 1
    plt.show()
