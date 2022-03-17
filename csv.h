#ifndef CSV_DOT_H
#define CSV_DOT_H

void readCSV(
  char result[][50][50], 
  char * filename, 
  int startRow, 
  int endRow, 
  int *cols,
  int numCols
);

#endif