// race.c - Demonstrates a race condition (no synchronization)
#include <stdio.h>
#include <omp.h>

#define NUM_THREADS 4
#define NUM_INCREMENTS 10000000

int main() {
    long long counter = 0;

    #pragma omp parallel num_threads(NUM_THREADS)
    {
        for (int i = 0; i < NUM_INCREMENTS / NUM_THREADS; i++) {
            counter++;  // No sync → race condition
        }
    }

    printf("Counter=%lld\n", counter);
    printf("Expected=%d\n", NUM_INCREMENTS);
    return 0;
}
