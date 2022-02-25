from operator import indexOf
import pandas as pd
import math
from pprint import pprint
import time
import matplotlib.pyplot as plt
import numpy as np
data_20 = pd.read_csv("2020_data.csv")
data_21 = pd.read_csv("2021_data.csv")
# def init_data():
#     global data_20, data_21
#     data_20 = pd.read_csv("2020_data.csv")
#     data_21 = pd.read_csv("2021_data.csv")
    

# #Predicting 2021 June 15th
def forecast_day(day):
    if day < 15 or day > 360:
        return None, None

    present_days = data_21.loc[day-7:day-1]
    present_days = present_days[[
        "Max Temp (°C)",
        "Min Temp (°C)",
        "Mean Temp (°C)",
        "Heat Deg Days (°C)",
        "Cool Deg Days (°C)",
        "Total Rain (mm)",
        "Total Snow (cm)",
        "Total Precip (mm)",
        "Snow on Grnd (cm)",
        # "Dir of Max Gust (10s deg)",
        # "Spd of Max Gust (km/h)"
        ]]
    present_days = present_days.fillna(0)
    CD = present_days.to_numpy()
    
    prev_days = data_20.loc[day-7:day+6]
    prev_days = prev_days[[
    "Max Temp (°C)",
    "Min Temp (°C)",
    "Mean Temp (°C)",
    "Heat Deg Days (°C)",
    "Cool Deg Days (°C)",
    "Total Rain (mm)",
    "Total Snow (cm)",
    "Total Precip (mm)",
    "Snow on Grnd (cm)",
    # "Dir of Max Gust (10s deg)",
    # "Spd of Max Gust (km/h)"
    ]]
    prev_days = prev_days.fillna(0)
    PD = prev_days.to_numpy()
    # t0 = time.time()
    w_dct = {}

    # pprint(CD)
    # pprint(PD)
    for index in range(8):
        w_dct[f"W{index+1}"] = PD[index: index+7]
 
    ed_list = []
    # calculating means for present year 7 days
    present_max = 0
    present_min = 0
    present_mean = 0
    present_head_days = 0
    present_cool_days = 0
    present_rain = 0
    present_snow = 0
    present_precip = 0
    present_snow_grnd = 0

    for line in CD:
        present_max += line[0] if not math.isnan(line[0]) else 0
        present_min += line[1] if not math.isnan(line[1]) else 0
        present_mean += line[2] if not math.isnan(line[2]) else 0
        present_head_days += line[3] if not math.isnan(line[3]) else 0
        present_cool_days += line[4] if not math.isnan(line[4]) else 0
        present_rain += line[5] if not math.isnan(line[5]) else 0
        present_snow += line[6] if not math.isnan(line[6]) else 0
        present_precip += line[7] if not math.isnan(line[7]) else 0
        present_snow_grnd += line[8] if not math.isnan(line[8]) else 0



    present_max = present_max / 7
    present_min = present_min / 7
    present_mean = present_mean / 7
    present_head_days = present_head_days / 7
    present_cool_days = present_cool_days / 7
    present_rain = present_rain / 7
    present_snow = present_snow / 7
    present_precip = present_precip / 7
    present_snow_grnd = present_snow_grnd / 7



    # mean of parameters for each window
    for line in w_dct:
        prev_max = 0
        prev_min = 0
        prev_mean = 0
        prev_head_days = 0
        prev_cool_days = 0
        prev_rain = 0
        prev_snow = 0
        prev_precip = 0
        prev_snow_grnd = 0
        for values in w_dct[line]:
            prev_max += values[0]
            prev_min += values[1]
            prev_mean += values[2]
            prev_head_days += values[3]
            prev_cool_days += values[4]
            prev_rain += values[5]
            prev_snow += values[6]
            prev_precip += values[7]
            prev_snow_grnd += values[8]

        prev_max = prev_max / 7
        prev_min = prev_min / 7
        prev_mean = prev_mean / 7
        prev_head_days = prev_head_days / 7
        prev_cool_days = prev_cool_days / 7
        prev_rain = prev_rain / 7
        prev_snow = prev_snow / 7
        prev_precip = prev_precip / 7
        prev_snow_grnd = prev_snow_grnd / 7

        euclid_distance = math.sqrt(
            (present_max - prev_max)**2 +
            (present_min - prev_min)**2 +
            (present_mean - prev_mean)**2 +
            (present_head_days - prev_head_days)**2 +
            (present_cool_days - prev_cool_days)**2 +
            (present_rain - prev_rain)**2 +
            (present_snow - prev_snow)**2 +
            (present_precip - prev_precip)**2 +
            (present_snow_grnd - prev_snow_grnd)**2
            )

        ed_list.append(euclid_distance)
    min_ed = min(ed_list)
    index_min_ed = indexOf(ed_list, min_ed)
    selected_prev_window = w_dct.get(f"W{index_min_ed+1}")

    sel_max = 0
    sel_min = 0
    sel_mean = 0
    sel_head_days = 0
    sel_cool_days = 0
    sel_rain = 0
    sel_snow = 0
    sel_precip = 0
    sel_snow_grnd = 0

    for line in selected_prev_window:
        sel_max += line[0]
        sel_min += line[1]
        sel_mean += line[2]
        sel_head_days += line[3]
        sel_cool_days += line[4]
        sel_rain += line[5]
        sel_snow += line[6]
        sel_precip += line[7]
        sel_snow_grnd += line[8]
        
    sel_max = sel_max / 7
    sel_min = sel_min / 7
    sel_mean = sel_mean / 7
    sel_head_days = sel_head_days / 7
    sel_cool_days = sel_cool_days / 7
    sel_rain = sel_rain / 7
    sel_snow = sel_snow / 7
    sel_precip = sel_precip / 7
    sel_snow_grnd = sel_snow_grnd / 7

    pred_max = (present_max + sel_max) / 2
    pred_min = (present_min + sel_min) / 2
    pred_mean = (present_mean + sel_mean) / 2
    pred_head_days = (present_head_days + sel_head_days) / 2
    pred_cool_days = (present_cool_days + sel_cool_days) / 2
    pred_rain = (present_rain + sel_rain) / 2
    pred_snow = (present_snow + sel_snow) / 2
    pred_precip = (present_precip + sel_precip) / 2
    pred_snow_grnd = (present_snow_grnd + sel_snow_grnd) / 2

    actual_data = data_21.loc[day]
    # actual_data = data_21[(data_21["Month"] == 6) & (data_21["Day"] == 15)]
    actual_data = actual_data.fillna(0)
    actual_values = actual_data[[
        "Max Temp (°C)",
        "Min Temp (°C)",
        "Mean Temp (°C)",
        "Heat Deg Days (°C)",
        "Cool Deg Days (°C)",
        "Total Rain (mm)",
        "Total Snow (cm)",
        "Total Precip (mm)",
        "Snow on Grnd (cm)",
        ]].to_numpy().flatten()

    # print("Prediction for June 15th, 2021 \n-----------------------------")

    title_arr = ["Max Temp (°C)",
        "Min Temp (°C)",
        "Mean Temp (°C)",
        "Heat Deg Days (°C)",
        "Cool Deg Days (°C)",
        "Total Rain (mm)",
        "Total Snow (cm)",
        "Total Precip (mm)",
        "Snow on Grnd (cm)"]
    pred_arr = [
        pred_max,
        pred_min,
        pred_mean,
        pred_head_days,
        pred_cool_days,
        pred_rain,
        pred_snow,
        pred_precip,
        pred_snow_grnd
    ]
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


