// semaphore.c - Simulates semaphore-like behavior using omp_lock_t
#include <stdio.h>
#include <omp.h>

#define NUM_THREADS 4
#define NUM_INCREMENTS 10000000

int main() {
    long long counter = 0;
    omp_lock_t lock;
    omp_init_lock(&lock);

    #pragma omp parallel num_threads(NUM_THREADS)
    {
        for (int i = 0; i < NUM_INCREMENTS / NUM_THREADS; i++) {
            omp_set_lock(&lock);
            counter++;
            omp_unset_lock(&lock);
        }
    }

    omp_destroy_lock(&lock);
    printf("Counter=%lld\n", counter);
    return 0;
}
