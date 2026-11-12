// barrier.c - Demonstrates #pragma omp barrier synchronization
#include <stdio.h>
#include <omp.h>

#define NUM_THREADS 12
#define NUM_INCREMENTS 10000000

int main() {
    long long counter = 0;

    #pragma omp parallel num_threads(NUM_THREADS)
    {
        int tid = omp_get_thread_num();

        // Phase 1
        printf("Thread %d before barrier\n", tid);

        #pragma omp barrier  // All threads wait here

        // Phase 2
        printf("Thread %d after barrier\n", tid);

        #pragma omp atomic
        counter++;
    }

    printf("Counter=%lld\n", counter);
    return 0;
}
