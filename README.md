# COE70B-Engineering-Design-Project

[Sliding Window Algorithm](https://www.hindawi.com/journals/isrn/2013/156540/)

## How to Run the Sequential C Program
Run the following command to compile and run the C program:

`gcc -Wall -c csv.c && gcc -Wall -c utils.c && gcc -Wall -c weather.c && gcc -o weather csv.o utils.o weather.o && ./weather`

## How to Run the Parallel C Program
Run the following command to compile and run the C program with MPI:

`mpicc -Wall -c csv.c && mpicc -Wall -c utils.c && mpicc -Wall -c weather_mpi.c && mpicc -o weather_mpi csv.o utils.o weather_mpi.o && mpirun -np <NUM_PROCESSES> weather_mpi`
