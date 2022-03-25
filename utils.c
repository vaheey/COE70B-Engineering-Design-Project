#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <float.h>
#include <math.h>

// Accepts a matrix and filters it to a specified range of 
// rows and columns
void filterMatrix(
  char matrix[][50][50],
  char result[][50][50],
  int startRow, 
  int endRow, 
  int *colsToFilter,
  int numColsToFilter
) {
  int i = 0;
  int j = 0;
  
  // For any weather data matrix
  int numRows = 400;
  int numCols = 50;

   // Read row by row
  int lineNumber = 0;
  for (int row = 0; row < numRows; row++) {
    // Constrain lines to row range
    if (lineNumber < startRow) {
      lineNumber++;
      continue;
    }
    // Stop reading once specified rows are read
    else if (lineNumber > endRow) {
      break;
    }

    // Read column by column
    int columnNumber = 0;
    int columnsRead = 0;
    for (int col = 0; col < numCols; col++) {
      // Constrain columns to the ones specified
      int shouldReadColumn = 0;
      for (int k = 0; k < numColsToFilter; k++) {
        if (columnNumber == colsToFilter[k]) {
          shouldReadColumn = 1;
          break;
        }
      }

      if (!shouldReadColumn) {
        // Stop reading once specified columns are read
        if (columnsRead == numColsToFilter) {
          break;
        }
        columnNumber++;
        continue;
      }

      // Copy cell from CSV to array
      strcpy(result[i][j], matrix[row][col]);

      // Increment Columns
      j++;
      columnNumber++;
      columnsRead++;
    }

    // Increment Rows
    i++;
    lineNumber++;

    // Reset to first column
    j = 0;
  }
}

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