/*
 * performance.c - Micro-Benchmark: OpenMP Critical Section vs Hardware Atomic
 * Course: Parallel and GPU Computing (26ECAC304) | Experiment 4
 *
 * Compares fine-grained hardware atomic instructions (LOCK XADD)
 * against coarse-grained compiler/runtime critical section locks.
 *
 * Compilation: gcc -O2 performance.c -fopenmp -o performance
 * Usage: ./performance
 */

#include <stdio.h>
#include <omp.h>

#define PERF_ITERS 1000000

int main(void) {
    long crit_counter = 0;
    double t0 = omp_get_wtime();
    #pragma omp parallel for
    for (int i = 0; i < PERF_ITERS; i++) {
        #pragma omp critical
        crit_counter++;
    }
    double t_crit = omp_get_wtime() - t0;
    printf("Critical counter = %ld\n", crit_counter);
    printf("Critical time = %.6f seconds\n", t_crit);

    long atom_counter = 0;
    double t1 = omp_get_wtime();
    #pragma omp parallel for
    for (int i = 0; i < PERF_ITERS; i++) {
        #pragma omp atomic
        atom_counter++;
    }
    double t_atom = omp_get_wtime() - t1;
    printf("Atomic counter = %ld\n", atom_counter);
    printf("Atomic time = %.6f seconds\n", t_atom);

    return 0;
}
