#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include "mpi.h"
#include "csv.h"
#include "utils.h"

char presentCSV[][50] = {
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

char prevCSV[][50] = {
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

// Predicts the weather of a particular day of a year
void predictWeatherForGivenDay(
  double *prediction, 
  double *actual,
  char presentData[][50][50],
  char prevData[][50][50], 
  int day, 
  int *cols, 
  int numParams
) {
  // Get current data for the past 7 days
  char CD[7][50][50];
  filterMatrix(presentData, CD, day - 7, day - 1, cols, numParams);

  // Get previous data (1 year old) for a 14 day period
  char PD[14][50][50];
  filterMatrix(prevData, PD, day - 7, day + 6, cols, numParams);

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
  filterMatrix(presentData, actualValues, day, day, cols, numParams);
  for (int i = 0; i < numParams; i++)
    actual[i] = atof(actualValues[0][i]);
}

int main(int argc, char **argv) {
  int rank, numProcs;
  double startTime = 0.0;
  double endTime = 0.0;

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &numProcs);

  if (rank == 0)
    startTime = MPI_Wtime();

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
    char presentData[400][50][50];
    char prevData[400][50][50];
    if (rank == 0) {
      // Get data from CSV files
      readCSV(presentData, presentCSV[location]);
      readCSV(prevData, prevCSV[location]);
    }

    // Retrieve data from rank 0
    MPI_Bcast(&presentData, 400*50*50, MPI_CHAR, 0, MPI_COMM_WORLD);
    MPI_Bcast(&prevData, 400*50*50, MPI_CHAR, 0, MPI_COMM_WORLD);

    // Divide days evenly between processes
    int count = 344 / numProcs;
    int remainder = 344 % numProcs;
    int startDay, endDay;
    if (rank < remainder) {
        startDay = rank * (count + 1);
        endDay = startDay + count;
    } else {
        startDay = rank * count + remainder;
        endDay = startDay + (count - 1);
    }

    // Add 8 since first 7 days cannot be predicted
    // printf("Rank %d starting from %d and ending at %d\n", rank, startDay+8, endDay+8);
    for (int i = startDay+8; i < endDay+8; i++) {
      double prediction[numParams];
      double actual[numParams];
      predictWeatherForGivenDay(
        prediction, 
        actual, 
        presentData, 
        prevData, 
        i,
        cols, 
        numParams
      );
      // Comment out these print statements for a more accurate time measurement
      // printf("\nFROM PROCESS %d Day: %d\nActual: ", rank, i);
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

  MPI_Barrier(MPI_COMM_WORLD);

  if (rank == 0) {
    endTime = MPI_Wtime();
    double timeTaken = endTime - startTime;
    printf("\nTime taken: %f seconds\n", timeTaken);
  }

  MPI_Finalize();
  return 0;
}
