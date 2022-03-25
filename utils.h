#ifndef UTILS_DOT_H
#define UTILS_DOT_H

void filterMatrix(
  char matrix[][50][50],
  char result[][50][50],
  int startRow, 
  int endRow, 
  int *colsToFilter,
  int numColsToFilter
);

double calcEuclidianDistance(
  double *presentMeans, 
  double *prevMeans, 
  int numPresentMeans
);

double min(double *arr, int len);

#endif