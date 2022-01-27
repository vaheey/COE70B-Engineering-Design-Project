from operator import indexOf
from matplotlib.cbook import index_of
import numpy as np
import matplotlib.pyplot as plot
import pandas as pd
import seaborn as sns
import math
from pprint import pprint

data_20 = pd.read_csv("2020_data.csv")
data_21 = pd.read_csv("2021_data.csv")
data_21.head()

#Predicting 2021 June 15th

present_days = data_21[data_21["Month"] == 6]
present_days = present_days[(present_days["Day"] < 15) & (present_days["Day"] >= 8 )]
present_days = present_days[["Max Temp (°C)", "Min Temp (°C)", "Total Rain (mm)"]]
CD = present_days.to_numpy()
# CD = np.asmatrix(CD)

prev_days = data_20[data_20["Month"] == 6]
prev_days = prev_days[(prev_days["Day"] < 15) & (prev_days["Day"] >= 1)]
prev_days = prev_days[["Max Temp (°C)", "Min Temp (°C)", "Total Rain (mm)"]]
PD = prev_days.to_numpy()
# PD = np.asmatrix(PD)

w_dct = {}

for index in range(8):
    w_dct[f"W{index+1}"] = PD[index: index+7]



ed_list = []
# calculating means for present year 7 days
present_max = present_min = present_rain = 0

for line in CD:
    present_max += line[0]
    present_min += line[1]
    present_rain += line[2]

present_max = present_max / 7
present_min = present_min / 7
present_rain = present_rain / 7

# mean of parameters for each window
for line in w_dct:
    max_sum = min_sum = rain_sum = 0
    for values in w_dct[line]:
        max_sum += values[0]
        min_sum += values[1]
        rain_sum += values[2]
    max_mean = max_sum / 7
    min_mean = min_sum / 7
    rain_mean = rain_sum / 7
    euclid_distance = math.sqrt((present_max - max_mean)**2 + (present_min - min_mean)**2 + (present_rain - rain_mean) ** 2)
    ed_list.append(euclid_distance)

min_ed = min(ed_list)
index_min_ed = indexOf(ed_list, min_ed)

selected_prev_window = w_dct.get(f"W{index_min_ed}")

sel_max_sum = sel_min_sum = sel_rain_sum = 0

for line in selected_prev_window:
    sel_max_sum += line[0]
    sel_min_sum += line[1]
    sel_rain_sum += line[2]

sel_max_mean = sel_max_sum / 7
sel_min_mean = sel_min_sum / 7
sel_rain_mean = sel_rain_sum / 7

pred_max = (present_max + sel_max_mean) / 2
pred_min = (present_min + sel_min_mean) / 2
pred_rain = (present_rain + sel_rain_mean) / 2

actual_data = data_21[(data_21["Month"] == 6) & (data_21["Day"] == 15)]
actual_values = actual_data[["Max Temp (°C)", "Min Temp (°C)", "Total Rain (mm)"]].to_numpy().flatten()

print(actual_values)

print("Prediction for June 15th, 2021 \n-----------------------------")
print("\tMax Temp |", "Min Temp |", "Rainfall")
print(f"Actual:   {actual_values[0]}   |   {actual_values[1]}   |   {actual_values[2]}")
print(f"Predicted: {pred_max}   |   {pred_min}   |   {pred_rain}")