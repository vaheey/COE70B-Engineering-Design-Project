#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Reads a weather CSV file and returns an array of strings
// containing the values in the CSV file
void readCSV(
  char result[][50][50], 
  char * filename
) {
  char line[1024];
  char *linePtr;
  int i = 0;
  int j = 0;
  FILE *file = fopen(filename, "r");

  // Read row by row
  int lineNumber = 0;
  while (fgets(line, sizeof(line), file)) {
    // Skip the first column
    if (lineNumber == 0) {
      lineNumber++;
      continue;
    }

    // Read column by column
    char *token;
    linePtr = line;
    while ((token = strsep(&linePtr, ","))) {
      // Copy cell from CSV to array
      strcpy(result[i][j], token);
      // Increment Columns
      j++;
    }
    
    // Increment Rows
    i++;
    // Reset to first column
    j = 0;
  }

  fclose(file);
}