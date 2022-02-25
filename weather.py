from operator import indexOf
import pandas as pd
import math
from pprint import pprint
import time
import matplotlib.pyplot as plt
import numpy as np

data_20 = pd.read_csv("2020_data.csv")
data_21 = pd.read_csv("2021_data.csv")

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
    return [arr[i] / 7 for i in range(len(arr))]

# Predicting any day in 2021
def forecast_day(day):
    if day < 15 or day > 360:
        return None, None

    present_days = data_21.loc[day-7:day-1]
    present_days = present_days[PARAMS]
    present_days = present_days.fillna(0)
    CD = present_days.to_numpy()
    
    prev_days = data_20.loc[day-7:day+6]
    prev_days = prev_days[PARAMS]
    prev_days = prev_days.fillna(0)
    PD = prev_days.to_numpy()
    w_dct = {}

    for index in range(8):
        w_dct[f"W{index+1}"] = PD[index: index+7]
 
    ed_list = []
    # calculating means for present year 7 days
    present_means = [0] * NUM_OF_PARAMS

    for line in CD:
        for i in range(len(line)):
            present_means[i] += line[i] if not math.isnan(line[i]) else 0

    present_means = get_mean(present_means)

    # mean of parameters for each window
    for line in w_dct:
        prev_means = [0] * NUM_OF_PARAMS
        for values in w_dct[line]:
            for i in range(len(prev_means)):
                prev_means += values[i]

        prev_means = get_mean(prev_means)

        euclid_distance = sum([(present_means[i] - prev_means[i]) ** 2 for i in range(len(present_means))])        
        ed_list.append(euclid_distance)

    min_ed = min(ed_list)
    index_min_ed = indexOf(ed_list, min_ed)
    selected_prev_window = w_dct.get(f"W{index_min_ed+1}")

    sel_means = [0] * NUM_OF_PARAMS

    for line in selected_prev_window:
        for i in range(len(line)):
            sel_means[i] += line[i]

    sel_means = get_mean(sel_means) 
    
    pred_arr = [(present_means[i] + sel_means[i]) / 2 for i in range(len(sel_means))]

    actual_data = data_21.loc[day]
    # actual_data = data_21[(data_21["Month"] == 6) & (data_21["Day"] == 15)]
    actual_data = actual_data.fillna(0)
    actual_values = actual_data[PARAMS].to_numpy().flatten()

    # print("Prediction for June 15th, 2021 \n-----------------------------")

    # print(" \t\t\t\t Actual | Predicted")
    # for i in range(len(title_arr)):
    #     print(f"{title_arr[i]}           \t|  {actual_values[i]} | {round(pred_arr[i], 2)}")
    # print(f"Actual:   {actual_values[0]}   |   {actual_values[1]}   |   {actual_values[2]}")
    # print(f"Predicted: {round(pred_max, 2)} |   {round(pred_min,2)}  |   {round(pred_rain, 2)}")

    # print(f"\nTotal time: {time.time() - t0}")
    return actual_values, pred_arr


if __name__ == "__main__":
    t0 = time.time()
    x = np.arange(0, 365)
    actual_list = []
    pred_list = []
    for val in x:
        temp_actual, temp_pred = forecast_day(val+1)
        if not temp_pred == None:
            actual_list.append(list(temp_actual))
            pred_list.append(temp_pred)
        else:
            actual_list.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
            pred_list.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
    print(f"\nTotal time: {time.time() - t0}")

    actual_max_lst = []
    pred_max_lst = []
    min
    for line in actual_list:
        actual_max_lst.append(line[0])
    for line in pred_list:
        pred_max_lst.append(line[0])
    plt.plot(x, actual_max_lst, label='Actual', color = "red")
    plt.plot(x, pred_max_lst, label='Prediction', color = "blue")
    plt.show()
    # # pprint(pred_list)
    # # pprint(data_20.loc[0,"Total Rain (mm)"])
    
    # # forecast_day(168)