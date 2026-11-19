// critical.c - Uses #pragma omp critical for mutual exclusion
#include <stdio.h>
#include <omp.h>

#define NUM_THREADS 4
#define NUM_INCREMENTS 10000000

int main() {
    long long counter = 0;

    #pragma omp parallel num_threads(NUM_THREADS)
    {
        for (int i = 0; i < NUM_INCREMENTS / NUM_THREADS; i++) {
            #pragma omp critical
            {
                counter++;
            }
        }
    }

    printf("Counter=%lld\n", counter);
    return 0;
}
