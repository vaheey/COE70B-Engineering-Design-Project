#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <time.h>

double calcEuclidianDistance(
  double presentMax, 
  double maxMean, 
  double presentMin, 
  double minMean, 
  double presentRain, 
  double rainMean
) {
  return sqrt(
    pow(presentMax - maxMean, 2) + 
    pow(presentMin - minMean, 2) + 
    pow(presentRain - rainMean, 2)
  );
}

double min(double *arr, int len) {
  double minVal = DBL_MAX;
  for (int i = 0; i < len; i++)
    if (arr[i] < minVal)
      minVal = arr[i];
  return minVal;
}

int main() {
  clock_t t;
  t = clock();

  double CD[7][3] = {
                    {26.5, 20.9, 10.2},
                    {29.4, 19.5,  0},
                    {25.3, 17.6,  0},
                    {25.3, 17.3,  0},
                    {25.4, 17.2,  0},
                    {29.1, 16.7,  0},
                    {25.0,  15.6,  2.8}
                  };

  double PD[14][3] = {
                  {23.7,  7.9,  0 },
                  {27.2, 12.9, 10.4},
                  {27.4, 13.4,  5.4},
                  {30.0,  15.6,  0 },
                  {28.3, 17.0,   2.6},
                  {26.1, 13.9,  0 },
                  {20.9, 11.1,  0 },
                  {22.8, 10.0,   0 },
                  {31.6, 15.6,  0 },
                  {32.1, 16.9, 24.4},
                  {24.3, 15.4,  0 },
                  {17.9,  9.2,  0 },
                  {18.7,  8.0,   0 },
                  {17.6,  8.2,  0 }
  };

  double windows[8][7][3];
  
  for (int i = 0; i < 8; i++)
    for (int j = 0; j < i + 7; j++)
      for (int k = 0; k < 3; k++)
        windows[i][j][k] = PD[j+i][k];

  double presentMax, presentMin, presentRain;

  for (int i = 0; i < 7; i++) {
    presentMax += CD[i][0];
    presentMin += CD[i][1];
    presentRain += CD[i][2];
  }

  presentMax /= 7;
  presentMin /= 7;
  presentRain /= 7;

  double edList[8];

  // mean of parameters for each window
  for (int i = 0; i < 8; i++) {
    double maxSum = 0; 
    double minSum = 0;
    double rainSum = 0;

    for (int j = 0; j < 7; j++) {
      maxSum += windows[i][j][0];
      minSum += windows[i][j][1];
      rainSum += windows[i][j][2];
    }

    double maxMean = maxSum / 7;
    double minMean = minSum / 7;
    double rainMean = rainSum / 7;

    double euclidDistance = calcEuclidianDistance
    (
      presentMax, 
      maxMean, 
      presentMin, 
      minMean, 
      presentRain, 
      rainMean
    );

    edList[i] = euclidDistance;
  }

  double minEd = min(edList, sizeof(edList) / sizeof(edList[0]));

  int indexMinEd;
  for (int i = 0; i < 8; i++) {
    if (edList[i] == minEd) {
      indexMinEd = i;
      break;
    }
  }

  double selectedPrevWindow[7][3];

  for (int i = 0; i < 7; i++) {
    for (int j = 0; j < 3; j++) {
      selectedPrevWindow[i][j] = windows[indexMinEd][i][j];
    }
  }

  double selMaxSum, selMinSum, selRainSum;

  for (int i = 0; i < 7; i++) {
    selMaxSum += selectedPrevWindow[i][0];
    selMinSum += selectedPrevWindow[i][1];
    selRainSum += selectedPrevWindow[i][2];
  }

  double selMaxMean = selMaxSum / 7;
  double selMinMean = selMinSum / 7;
  double selRainMean = selRainSum / 7;

  double predMax = (presentMax + selMaxMean) / 2;
  double predMin = (presentMin + selMinMean) / 2;
  double predRain = (presentRain + selRainMean) / 2;

  printf("Prediction for June 15th 2021\n");
  printf("\tMax Temp | Min Temp | Rainfall\n");
  printf("Actual:   22.5   |   12.9   |   0.0\n");
  printf("Predicted: %.2lf |   %.2lf  |   %.2lf\n", predMax, predMin, predRain);
  
  t = clock() - t;
  double timeTaken = ((double)t)/CLOCKS_PER_SEC;
  printf("Time taken: %f seconds\n", timeTaken);
  return 1;
}
