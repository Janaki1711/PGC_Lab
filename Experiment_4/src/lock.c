/*
 * lock.c - OpenMP Lock Synchronization (omp_lock_t)
 * Course: Parallel and GPU Computing (26ECAC304) | Experiment 4
 *
 * Demonstrates mutual exclusion using OpenMP runtime lock primitives.
 *
 * Compilation: gcc -O2 lock.c -fopenmp -o lock
 * Usage: ./lock
 */

#include <stdio.h>
#include <omp.h>

#define ITERATIONS 100000

int main(void) {
    long counter = 0;
    omp_lock_t lock;
    omp_init_lock(&lock);

    #pragma omp parallel for
    for (int i = 0; i < ITERATIONS; i++) {
        omp_set_lock(&lock);
        counter++;
        omp_unset_lock(&lock);
    }

    omp_destroy_lock(&lock);
    printf("Final counter = %ld\n", counter);
    return 0;
}
