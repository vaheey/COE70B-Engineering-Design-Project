#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Reads a CSV file and returns an array of strings
// containing the values in the specified rows and columns
void readCSV(
  char result[][50][50], 
  char * filename, 
  int startRow, 
  int endRow, 
  int *cols,
  int numCols
) {
  char line[1024];
  char *linePtr;
  int i = 0;
  int j = 0;
  FILE *file = fopen(filename, "r");

  // Read row by row
  int lineNumber = 0;
  while (fgets(line, sizeof(line), file)) {
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
    char *token;
    linePtr = line;
    int columnNumber = 0;
    int columnsRead = 0;
    while ((token = strsep(&linePtr, ","))) {
      // Constrain columns to the ones specified
      int shouldReadColumn = 0;
      for (int k = 0; k < numCols; k++) {
        if (columnNumber == cols[k]) {
          shouldReadColumn = 1;
          break;
        }
      }

      if (!shouldReadColumn) {
        // Stop reading once specified columns are read
        if (columnsRead == numCols) {
          break;
        }
        columnNumber++;
        continue;
      }

      // Copy cell from CSV to array
      strcpy(result[i][j], token);

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

  fclose(file);
}