// atomic.c - Uses #pragma omp atomic for lightweight hardware-level sync
#include <stdio.h>
#include <omp.h>

#define NUM_THREADS 4
#define NUM_INCREMENTS 10000000

int main() {
    long long counter = 0;

    #pragma omp parallel num_threads(NUM_THREADS)
    {
        for (int i = 0; i < NUM_INCREMENTS / NUM_THREADS; i++) {
            #pragma omp atomic
            counter++;
        }
    }

    printf("Counter=%lld\n", counter);
    return 0;
}
