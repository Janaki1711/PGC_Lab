// compare_sync.c - Full benchmark comparing all synchronization mechanisms
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define NUM_INCREMENTS 10000000

typedef struct {
    const char *name;
    int threads;
    long long final_count;
    double time_sec;
    int correct;
} Result;

long long run_none(int nthreads) {
    long long counter = 0;
    #pragma omp parallel num_threads(nthreads)
    {
        for (int i = 0; i < NUM_INCREMENTS / nthreads; i++)
            counter++;
    }
    return counter;
}

long long run_critical(int nthreads) {
    long long counter = 0;
    #pragma omp parallel num_threads(nthreads)
    {
        for (int i = 0; i < NUM_INCREMENTS / nthreads; i++) {
            #pragma omp critical
            counter++;
        }
    }
    return counter;
}

long long run_atomic(int nthreads) {
    long long counter = 0;
    #pragma omp parallel num_threads(nthreads)
    {
        for (int i = 0; i < NUM_INCREMENTS / nthreads; i++) {
            #pragma omp atomic
            counter++;
        }
    }
    return counter;
}

long long run_lock(int nthreads) {
    long long counter = 0;
    omp_lock_t lock;
    omp_init_lock(&lock);
    #pragma omp parallel num_threads(nthreads)
    {
        for (int i = 0; i < NUM_INCREMENTS / nthreads; i++) {
            omp_set_lock(&lock);
            counter++;
            omp_unset_lock(&lock);
        }
    }
    omp_destroy_lock(&lock);
    return counter;
}

void benchmark(const char *name, long long (*fn)(int), int nthreads, Result *r) {
    double start = omp_get_wtime();
    long long count = fn(nthreads);
    double end = omp_get_wtime();

    r->name       = name;
    r->threads    = nthreads;
    r->final_count = count;
    r->time_sec   = end - start;
    r->correct    = (count == NUM_INCREMENTS);
}

int main() {
    int thread_counts[] = {1, 2, 4, 8};
    int n = sizeof(thread_counts) / sizeof(thread_counts[0]);

    printf("Comparing synchronization mechanisms for %d shared increments\n\n", NUM_INCREMENTS);
    printf("%-12s | %-7s | %-12s | %-11s | %s\n",
           "Mechanism", "Threads", "Final Count", "Correctness", "Time (s)");
    printf("%-s\n", "----------------------------------------------------------------------");

    for (int i = 0; i < n; i++) {
        int t = thread_counts[i];
        Result results[4];

        benchmark("None",     run_none,     t, &results[0]);
        benchmark("Critical", run_critical, t, &results[1]);
        benchmark("Atomic",   run_atomic,   t, &results[2]);
        benchmark("Lock",     run_lock,     t, &results[3]);

        for (int j = 0; j < 4; j++) {
            printf("%-12s | %-7d | %-12lld | %-11s | %.4f\n",
                   results[j].name,
                   results[j].threads,
                   results[j].final_count,
                   results[j].correct ? "Correct" : "INCORRECT",
                   results[j].time_sec);
        }
        printf("\n");
    }

    printf("\nExpected correct final count = %d\n", NUM_INCREMENTS);
    printf("Observation: 'None' is fastest but incorrect (race condition).\n");
    printf("'Critical' is correct but slowest (coarse-grained locking).\n");
    printf("'Atomic' and 'Lock' are correct; 'Atomic' scales better since it\n");
    printf("uses lightweight hardware instructions instead of OS-level locks.\n");

    return 0;
}
