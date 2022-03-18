#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <time.h>
#include <string.h>
#include "csv.h"

char presentCSV[20][50] = {
  "./data/2021_tor_data.csv",
  "./data/2021_van_data.csv",
  "./data/2021_mtl_data.csv",
  "./data/2021_cal_data.csv",
  "./data/2021_edm_data.csv",
  "./data/2021_ham_data.csv",
  "./data/2021_hfx_data.csv",
  "./data/2021_kel_data.csv",
  "./data/2021_kit_data.csv",
  "./data/2021_lon_data.csv",
  "./data/2021_osh_data.csv",
  "./data/2021_ott_data.csv",
  "./data/2021_peg_data.csv",
  "./data/2021_qbc_data.csv",
  "./data/2021_reg_data.csv",
  "./data/2021_sas_data.csv",
  "./data/2021_stcath_data.csv",
  "./data/2021_stjn_data.csv",
  "./data/2021_vic_data.csv",
  "./data/2021_win_data.csv"
};

char prevCSV[20][50] = {
  "./data/2020_tor_data.csv",
  "./data/2020_van_data.csv",
  "./data/2020_mtl_data.csv",
  "./data/2020_cal_data.csv",
  "./data/2020_edm_data.csv",
  "./data/2020_ham_data.csv",
  "./data/2020_hfx_data.csv",
  "./data/2020_kel_data.csv",
  "./data/2020_kit_data.csv",
  "./data/2020_lon_data.csv",
  "./data/2020_osh_data.csv",
  "./data/2020_ott_data.csv",
  "./data/2020_peg_data.csv",
  "./data/2020_qbc_data.csv",
  "./data/2020_reg_data.csv",
  "./data/2020_sas_data.csv",
  "./data/2020_stcath_data.csv",
  "./data/2020_stjn_data.csv",
  "./data/2020_vic_data.csv",
  "./data/2020_win_data.csv" 
};

// Calculate the euclidian distance of two arrays
double calcEuclidianDistance(
  double *presentMeans, 
  double *prevMeans, 
  int numPresentMeans
) {
  double euclidianDistance = 0;
  for (int i = 0; i < numPresentMeans; i++) {
    euclidianDistance += pow(presentMeans[i] - prevMeans[i], 2);
  }
  return sqrt(euclidianDistance);
}

// Determine the minimum value from an array
double min(double *arr, int len) {
  double minVal = DBL_MAX;
  for (int i = 0; i < len; i++)
    if (arr[i] < minVal)
      minVal = arr[i];
  return minVal;
}

// Predicts the weather of a particular day of a year
void predictWeatherForGivenDay(
  double *prediction, 
  double *actual,
  char *presentCSV,
  char *prevCSV, 
  int day, 
  int *cols, 
  int numParams
) {
  // Get current data for the past 7 days
  char CD[7][50][50];
  readCSV(CD, presentCSV, day - 7, day - 1, cols, numParams);

  // Get previous data (1 year old) for a 14 day period
  char PD[14][50][50];
  readCSV(PD, prevCSV, day - 7, day + 6, cols, numParams);

  // 8 sliding windows based on previous data, 7 days per window
  double windows[8][7][numParams];
  memset(windows, 0, 8*7*numParams*sizeof(double));
  for (int i = 0; i < 8; i++) {
    for (int j = 0; j < 7; j++) {
      for (int k = 0; k < numParams; k++) {
        windows[i][j][k] = atof(PD[j+i][k]);
      }
    }
  }

  // Sum the present values 
  double presentSums[numParams];
  memset(presentSums, 0, numParams*sizeof(double));
  for (int i = 0; i < 7; i++)
    for (int j = 0; j < numParams; j++)
      presentSums[j] += atof(CD[i][j]);

  // Using the present sums, determine the means
  double presentMeans[numParams];
  memset(presentMeans, 0, numParams*sizeof(double));
  for (int i = 0; i < numParams; i++)
    presentMeans[i] = presentSums[i] / 7;

  // Determine the means of the previous values based on the
  // sliding windows and calculate the Euclidian Distances
  double edList[8];
  memset(edList, 0, 8*sizeof(double));
  for (int i = 0; i < 8; i++) {
    double prevSums[numParams];
    memset(prevSums, 0, numParams*sizeof(double));
    for (int j = 0; j < 7; j++)
      for (int k = 0; k < numParams; k++)
        prevSums[k] += windows[i][j][k];

    double prevMeans[numParams];
    memset(prevMeans, 0, numParams*sizeof(double));
    for (int j = 0; j < numParams; j++)
      prevMeans[j] = prevSums[j] / 7;

    int numPresentMeans = sizeof(presentMeans) / sizeof(presentMeans[0]);
    double euclidDistance = calcEuclidianDistance
    (
      presentMeans,
      prevMeans,
      numPresentMeans
    );

    edList[i] = euclidDistance;
  }

  // Determine the minimum Euclidian Distance and find its index
  double minEd = min(edList, sizeof(edList) / sizeof(edList[0]));
  int indexMinEd = 0;
  for (int i = 0; i < 8; i++) {
    if (edList[i] == minEd) {
      indexMinEd = i;
      break;
    }
  }

  // Isolate the window with the minimum Euclidian Distance
  double selectedPrevWindow[7][numParams];
  memset(selectedPrevWindow, 0, 7*numParams*sizeof(double));
  for (int i = 0; i < 7; i++)
    for (int j = 0; j < numParams; j++)
      selectedPrevWindow[i][j] = windows[indexMinEd][i][j];

  // Find variation vector based on present data
  double presentVariationVector[numParams][6];
  memset(presentVariationVector, 0, numParams*6*sizeof(double));
  for (int i = 0; i < numParams; i++)
    for (int j = 0; j < 6; j++)
      presentVariationVector[i][j] = atof(CD[j+1][i]) - atof(CD[j][i]);

  // Find variation vector based on previous data
  double prevVariationVector[numParams][6];
  memset(prevVariationVector, 0, numParams*6*sizeof(double));
  for (int i = 0; i < numParams; i++)
    for (int j = 0; j < 6; j++)
      prevVariationVector[i][j] = selectedPrevWindow[j+1][i] - selectedPrevWindow[j][i];

  // Determine the mean of the present variation vector
  double meanPresentVar[numParams];
  memset(meanPresentVar, 0, numParams*sizeof(double));
  for (int i = 0; i < numParams; i++) {
    double presentVarSum = 0;
    for (int j = 0; j < 6; j++)
      presentVarSum += presentVariationVector[i][j];
    meanPresentVar[i] = presentVarSum / 6;
  }

  // Determine the mean of the previous variation vector
  double meanPrevVar[numParams];
  memset(meanPrevVar, 0, numParams*sizeof(double));
  for (int i = 0; i < numParams; i++) {
    double prevVarSum = 0;
    for (int j = 0; j < 6; j++)
      prevVarSum += prevVariationVector[i][j];
    meanPrevVar[i] = prevVarSum / 6;
  }

  // Determine the mean of both present and previous mean variation vectors
  double meanVariationVector[numParams];
  memset(meanVariationVector, 0, numParams*sizeof(double));
  for (int i = 0; i < numParams; i++)
    meanVariationVector[i] = (meanPresentVar[i] + meanPrevVar[i]) / 2;

  // Retrieve values from the day previous to the day being predicted
  double previousDay[numParams];
  memset(previousDay, 0, numParams*sizeof(double));
  for (int i = 0; i < numParams; i++)
    previousDay[i] = atof(CD[6][i]);

  // Add mean variation vector values to the previous day to get final prediction
  for (int i = 0; i < numParams; i++)
    previousDay[i] += meanVariationVector[i];

  // Assign the final prediction values
  for (int i = 0; i < numParams; i++)
    prediction[i] = previousDay[i];

  // Retrive the actual values for comparision purposes
  char actualValues[1][50][50];
  readCSV(actualValues, presentCSV, day, day, cols, numParams);
  for (int i = 0; i < numParams; i++)
    actual[i] = atof(actualValues[0][i]);
}

int main() {
  clock_t t;
  t = clock();

  // 9 - Max Temp (°C)
  // 11 - Min Temp (°C)
  // 13 - Mean Temp (°C)
  // 15 - Heat Deg Days (°C)
  // 17 - Cool Deg Days (°C)
  // 19 - Total Rain (mm)
  // 21 - Total Snow (cm)
  // 23 - Total Precip (mm)
  // 25 - Snow on Grnd (cm)
  int cols[] = {9, 11, 13, 15, 17, 19, 21, 23, 25};
  int numParams = sizeof(cols) / sizeof(cols[0]);
  int numLocations = sizeof(presentCSV) / sizeof(presentCSV[0]);

  for (int location = 0; location < numLocations; location++) {
    for (int i = 8; i <= 359; i++) {
      double prediction[numParams];
      double actual[numParams];
      predictWeatherForGivenDay(
        prediction, 
        actual, 
        presentCSV[location], 
        prevCSV[location], 
        i,
        cols, 
        numParams
      );
      
      // Comment out these print statements for a more accurate time measurement
      // printf("\nDay %d\nActual: ", i);
      // for (int j = 0; j < numParams; j++) {
      //   printf("%.2lf ", actual[j]);
      // }
      // printf("\nPrediction: ");
      // for (int j = 0; j < numParams; j++) {
      //   printf("%.2lf ", prediction[j]);
      // }
      // printf("\n");
    }
  }
  
  t = clock() - t;
  double timeTaken = ((double)t)/CLOCKS_PER_SEC;
  printf("\nTime taken: %f seconds\n", timeTaken);

  return 0;
}
