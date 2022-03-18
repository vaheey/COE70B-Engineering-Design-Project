from operator import indexOf
import pandas as pd
import math
from pprint import pprint
import time
import matplotlib.pyplot as plt
import numpy as np

toronto_data_20 = pd.read_csv("data/2020_data.csv")
van_data_20 = pd.read_csv("data/2020_van_data.csv")
mtl_data_20 = pd.read_csv("data/2020_mtl_data.csv")
cal_data_20 = pd.read_csv("data/2020_cal_data.csv")
edm_data_20 = pd.read_csv("data/2020_edm_data.csv")
ham_data_20 = pd.read_csv("data/2020_ham_data.csv")
hfx_data_20 = pd.read_csv("data/2020_hfx_data.csv")
kel_data_20 = pd.read_csv("data/2020_kel_data.csv")
kit_data_20 = pd.read_csv("data/2020_kit_data.csv")
lon_data_20 = pd.read_csv("data/2020_lon_data.csv")
osh_data_20 = pd.read_csv("data/2020_osh_data.csv")
ott_data_20 = pd.read_csv("data/2020_ott_data.csv")
peg_data_20 = pd.read_csv("data/2020_peg_data.csv")
qbc_data_20 = pd.read_csv("data/2020_qbc_data.csv")
reg_data_20 = pd.read_csv("data/2020_reg_data.csv")
sas_data_20 = pd.read_csv("data/2020_sas_data.csv")
stc_data_20 = pd.read_csv("data/2020_stcath_data.csv")
stj_data_20 = pd.read_csv("data/2020_stjn_data.csv")
vic_data_20 = pd.read_csv("data/2020_vic_data.csv")
win_data_20 = pd.read_csv("data/2020_win_data.csv")
toronto_data_21 = pd.read_csv("data/2021_data.csv")
van_data_21 = pd.read_csv("data/2021_van_data.csv")
mtl_data_21 = pd.read_csv("data/2021_mtl_data.csv")
cal_data_21 = pd.read_csv("data/2021_cal_data.csv")
edm_data_21 = pd.read_csv("data/2021_edm_data.csv")
ham_data_21 = pd.read_csv("data/2021_ham_data.csv")
hfx_data_21 = pd.read_csv("data/2021_hfx_data.csv")
kel_data_21 = pd.read_csv("data/2021_kel_data.csv")
kit_data_21 = pd.read_csv("data/2021_kit_data.csv")
lon_data_21 = pd.read_csv("data/2021_lon_data.csv")
osh_data_21 = pd.read_csv("data/2021_osh_data.csv")
ott_data_21 = pd.read_csv("data/2021_ott_data.csv")
peg_data_21 = pd.read_csv("data/2021_peg_data.csv")
qbc_data_21 = pd.read_csv("data/2021_qbc_data.csv")
reg_data_21 = pd.read_csv("data/2021_reg_data.csv")
sas_data_21 = pd.read_csv("data/2021_sas_data.csv")
stc_data_21 = pd.read_csv("data/2021_stcath_data.csv")
stj_data_21 = pd.read_csv("data/2021_stjn_data.csv")
vic_data_21 = pd.read_csv("data/2021_vic_data.csv")
win_data_21 = pd.read_csv("data/2021_win_data.csv")

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
    
    actual_data = data_21.loc[day]
    actual_data = actual_data.fillna(0)
    actual_values = actual_data[PARAMS].to_numpy().flatten()

    return actual_values, pred_arr

if __name__ == "__main__":
    t0 = time.time()
    day_range = np.arange(0, 365)
    toronto_actual_list = []
    van_actual_list = []
    mtl_actual_list = []
    cal_actual_list = []
    edm_actual_list = []
    ham_actual_list = []
    hfx_actual_list = []
    kel_actual_list = []
    kit_actual_list = []
    lon_actual_list = []
    osh_actual_list = []
    ott_actual_list = []
    peg_actual_list = []
    qbc_actual_list = []
    reg_actual_list = []
    sas_actual_list = []
    stc_actual_list = []
    stj_actual_list = []
    vic_actual_list = []
    win_actual_list = []

    toronto_pred_list = []
    van_pred_list = []
    mtl_pred_list = []
    cal_pred_list = []
    edm_pred_list = []
    ham_pred_list = []
    hfx_pred_list = []
    kel_pred_list = []
    kit_pred_list = []
    lon_pred_list = []
    osh_pred_list = []
    ott_pred_list = []
    peg_pred_list = []
    qbc_pred_list = []
    reg_pred_list = []
    sas_pred_list = []
    stc_pred_list = []
    stj_pred_list = []
    vic_pred_list = []
    win_pred_list = []

    for day in day_range:
        toronto_temp_actual, toronto_temp_pred = forecast_day(day,toronto_data_21,toronto_data_20)
        mtl_temp_actual, mtl_temp_pred = forecast_day(day,mtl_data_21,mtl_data_20)
        cal_temp_actual, cal_temp_pred = forecast_day(day,cal_data_21,cal_data_20)
        edm_temp_actual, edm_temp_pred = forecast_day(day,edm_data_21,edm_data_20)
        ham_temp_actual, ham_temp_pred = forecast_day(day,ham_data_21,ham_data_20)
        hfx_temp_actual, hfx_temp_pred = forecast_day(day,hfx_data_21,hfx_data_20)
        kel_temp_actual, kel_temp_pred = forecast_day(day,kel_data_21,kel_data_20)
        kit_temp_actual, kit_temp_pred = forecast_day(day,kit_data_21,kit_data_20)
        lon_temp_actual, lon_temp_pred = forecast_day(day,lon_data_21,lon_data_20)
        osh_temp_actual, osh_temp_pred = forecast_day(day,osh_data_21,osh_data_20)
        ott_temp_actual, ott_temp_pred = forecast_day(day,ott_data_21,ott_data_20)
        peg_temp_actual, peg_temp_pred = forecast_day(day,peg_data_21,peg_data_20)
        qbc_temp_actual, qbc_temp_pred = forecast_day(day,qbc_data_21,qbc_data_20)
        reg_temp_actual, reg_temp_pred = forecast_day(day,reg_data_21,reg_data_20)
        sas_temp_actual, sas_temp_pred = forecast_day(day,sas_data_21,sas_data_20)
        stc_temp_actual, stc_temp_pred = forecast_day(day,stc_data_21,stc_data_20)
        stj_temp_actual, stj_temp_pred = forecast_day(day,stj_data_21,stj_data_20)
        vic_temp_actual, vic_temp_pred = forecast_day(day,vic_data_21,vic_data_20)
        win_temp_actual, win_temp_pred = forecast_day(day,win_data_21,win_data_20)
        van_temp_actual, van_temp_pred = forecast_day(day,van_data_21,van_data_20)

        if toronto_temp_pred:
            toronto_actual_list.append(list(toronto_temp_actual))
            mtl_actual_list.append(list(mtl_temp_actual))
            van_actual_list.append(list(van_temp_actual))
            cal_actual_list.append(list(cal_temp_actual))
            edm_actual_list.append(list(edm_temp_actual))
            ham_actual_list.append(list(ham_temp_actual))
            hfx_actual_list.append(list(hfx_temp_actual))
            kel_actual_list.append(list(kel_temp_actual))
            kit_actual_list.append(list(kit_temp_actual))
            lon_actual_list.append(list(lon_temp_actual))
            osh_actual_list.append(list(osh_temp_actual))
            ott_actual_list.append(list(ott_temp_actual))
            peg_actual_list.append(list(peg_temp_actual))
            qbc_actual_list.append(list(qbc_temp_actual))
            reg_actual_list.append(list(reg_temp_actual))
            sas_actual_list.append(list(sas_temp_actual))
            stc_actual_list.append(list(stc_temp_actual))
            stj_actual_list.append(list(stj_temp_actual))
            vic_actual_list.append(list(vic_temp_actual))
            win_actual_list.append(list(win_temp_actual))

            toronto_pred_list.append(toronto_temp_pred)
            mtl_pred_list.append(mtl_temp_pred)
            van_pred_list.append(van_temp_pred)
            cal_pred_list.append(list(cal_temp_pred))
            edm_pred_list.append(list(edm_temp_pred))
            ham_pred_list.append(list(ham_temp_pred))
            hfx_pred_list.append(list(hfx_temp_pred))
            kel_pred_list.append(list(kel_temp_pred))
            kit_pred_list.append(list(kit_temp_pred))
            lon_pred_list.append(list(lon_temp_pred))
            osh_pred_list.append(list(osh_temp_pred))
            ott_pred_list.append(list(ott_temp_pred))
            peg_pred_list.append(list(peg_temp_pred))
            qbc_pred_list.append(list(qbc_temp_pred))
            reg_pred_list.append(list(reg_temp_pred))
            sas_pred_list.append(list(sas_temp_pred))
            stc_pred_list.append(list(stc_temp_pred))
            stj_pred_list.append(list(stj_temp_pred))
            vic_pred_list.append(list(vic_temp_pred))
            win_pred_list.append(list(win_temp_pred))
        else:
            toronto_actual_list.append([0] * NUM_OF_PARAMS)
            mtl_actual_list.append([0] * NUM_OF_PARAMS)
            van_actual_list.append([0] * NUM_OF_PARAMS)
            cal_actual_list.append([0] * NUM_OF_PARAMS)
            edm_actual_list.append([0] * NUM_OF_PARAMS)
            ham_actual_list.append([0] * NUM_OF_PARAMS)
            hfx_actual_list.append([0] * NUM_OF_PARAMS)
            kel_actual_list.append([0] * NUM_OF_PARAMS)
            kit_actual_list.append([0] * NUM_OF_PARAMS)
            lon_actual_list.append([0] * NUM_OF_PARAMS)
            osh_actual_list.append([0] * NUM_OF_PARAMS)
            ott_actual_list.append([0] * NUM_OF_PARAMS)
            peg_actual_list.append([0] * NUM_OF_PARAMS)
            qbc_actual_list.append([0] * NUM_OF_PARAMS)
            reg_actual_list.append([0] * NUM_OF_PARAMS)
            sas_actual_list.append([0] * NUM_OF_PARAMS)
            stc_actual_list.append([0] * NUM_OF_PARAMS)
            stj_actual_list.append([0] * NUM_OF_PARAMS)
            vic_actual_list.append([0] * NUM_OF_PARAMS)
            win_actual_list.append([0] * NUM_OF_PARAMS)

            toronto_pred_list.append([0] * NUM_OF_PARAMS)
            mtl_pred_list.append([0] * NUM_OF_PARAMS)
            van_pred_list.append([0] * NUM_OF_PARAMS)
            cal_pred_list.append([0] * NUM_OF_PARAMS)
            edm_pred_list.append([0] * NUM_OF_PARAMS)
            ham_pred_list.append([0] * NUM_OF_PARAMS)
            hfx_pred_list.append([0] * NUM_OF_PARAMS)
            kel_pred_list.append([0] * NUM_OF_PARAMS)
            kit_pred_list.append([0] * NUM_OF_PARAMS)
            lon_pred_list.append([0] * NUM_OF_PARAMS)
            osh_pred_list.append([0] * NUM_OF_PARAMS)
            ott_pred_list.append([0] * NUM_OF_PARAMS)
            peg_pred_list.append([0] * NUM_OF_PARAMS)
            qbc_pred_list.append([0] * NUM_OF_PARAMS)
            reg_pred_list.append([0] * NUM_OF_PARAMS)
            sas_pred_list.append([0] * NUM_OF_PARAMS)
            stc_pred_list.append([0] * NUM_OF_PARAMS)
            stj_pred_list.append([0] * NUM_OF_PARAMS)
            vic_pred_list.append([0] * NUM_OF_PARAMS)
            win_pred_list.append([0] * NUM_OF_PARAMS)
    print(f"\nTotal time: {time.time() - t0}")

    toronto_actual_data = np.transpose(toronto_actual_list)
    mtl_actual_data = np.transpose(mtl_actual_list)
    van_actual_data = np.transpose(van_actual_list)
    toronto_pred_data = np.transpose(toronto_pred_list)
    mtl_pred_data = np.transpose(mtl_pred_list)
    van_pred_data = np.transpose(van_pred_list)

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
