# Multithreaded Programming Using Pthreads and OpenMP

[![Course](https://img.shields.io/badge/Course-Parallel%20%26%20GPU%20Computing-blue.svg)](#)
[![Workload](https://img.shields.io/badge/Workload-10%5E9%20Numerical%20Iterations-orange.svg)](#)
[![Libraries](https://img.shields.io/badge/Libraries-POSIX%20Threads%20%7C%20OpenMP-green.svg)](#)
[![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)](#)

---

## Executive Summary

This repository contains the empirical performance analysis, parallel execution models, and benchmark results for **Multithreaded Programming Using POSIX Threads (Pthreads) and OpenMP**, evaluating thread creation, work distribution, concurrency hazards, synchronization primitives, and numerical scalability over **$1,000,000,000$ iterations ($10^9$)**.

```mermaid
flowchart LR
    subgraph Input ["1. Workload Input"]
        IN["Numerical Summation Workload<br/>N = 1,000,000,000 (10^9 iterations)<br/>Target Sum = 499999999500.00"]
    end

    subgraph Models ["2. Multithreaded Scaling Evaluation"]
        direction TB
        M1["Sequential CPU Baseline — 1.418s (1.00x)"]
        M2["Pthreads (1 to 16 Threads) — Up to 10.40x Speedup"]
        M3["OpenMP (1 to 16 Threads) — Up to 10.41x Speedup"]
    end

    subgraph Output ["3. Deterministic Output"]
        OUT["Validated Numerical Correctness<br/>Near-Linear Scaling up to 6 Threads<br/>Peak Speedup ~10.4x at 16 Threads"]
    end

    Input --> Models --> Output
```

### Key Finding

> **Both Pthreads and OpenMP achieved near-linear speedup up to 6 threads (~5.90× speedup, ~98.4% parallel efficiency) and delivered a peak speedup of ~10.4× on 16 threads (reducing execution time from 1.418s down to 0.136s). OpenMP delivered identical runtime performance to manual low-level Pthreads while eliminating over 85% of thread management boilerplate code.**

---

## Table of Contents

1. [Repository Structure](#repository-structure)
2. [Experiment Objectives](#1-experiment-objectives)
3. [Theoretical & Architectural Comparison](#2-theoretical--architectural-comparison)
4. [Workload Specification](#3-workload-specification)
5. [Source Code References](#4-source-code-references)
6. [Empirical Results & Screenshots](#5-empirical-results--screenshots)
7. [Performance Comparison & Visualizations](#6-performance-comparison--visualizations)
8. [Technical Analysis & Discussion](#7-technical-analysis--discussion)
9. [Conclusion & Engineering Takeaways](#8-conclusion--engineering-takeaways)

---

## Repository Structure

```
Experiment_2/
├── README.md                                           # Master Lab Documentation & Benchmark Report
├── .gitignore                                          # Git ignore rules for build artifacts & binaries
├── src/                                                # Source Code Implementations
│   ├── pthreads/                                       # POSIX Threads Programs
│   │   ├── thread1.c                                   # Single Thread Creation & Joining
│   │   ├── thread2.c                                   # Multi-Thread Spawning with Thread IDs
│   │   ├── thread_sum.c                                # Array Chunking & Partial Summation
│   │   ├── race.c                                      # Unsynchronized Race Condition Demo
│   │   ├── mutex.c                                     # Mutex Synchronization (pthread_mutex_t)
│   │   └── pthread_perf.c                              # Scalability Benchmark (1, 2, 4, 6, 16 Threads)
│   ├── openmp/                                         # OpenMP Programs
│   │   ├── omp1.c                                      # Parallel Region & Thread Identification
│   │   ├── omp_sum.c                                   # Work-Sharing Loop & Reduction Clause
│   │   ├── omp_race.c                                  # OpenMP Data Race Condition
│   │   ├── omp_critical.c                              # Critical Section Synchronization
│   │   ├── omp_barrier.c                               # Phased Barrier Synchronization
│   │   └── omp_perf.c                                  # Scalability Benchmark (1, 2, 4, 6, 16 Threads)
│   └── sequential/                                     # Baseline Reference
│       └── sequential.c                                # Single-Threaded Sequential Program
├── images/                                             # Screenshots & Performance Charts
│   ├── performance_comparison_charts.png               # Combined 3-Panel Benchmark Chart
│   ├── execution_time_vs_threads.png                   # Execution Time Scaling Curve
│   ├── speedup_vs_threads.png                          # Speedup Factor vs. Ideal Curve
│   ├── efficiency_vs_threads.png                       # Parallel Efficiency Percentage Curve
│   └── *.jpeg                                          # Terminal Execution Output Screenshots
└── scripts/
    └── generate_charts.py                              # Python Script to regenerate performance charts
```

---

## 1. Experiment Objectives

1. **Thread Lifecycle Management**: Explore explicit thread creation, parameter passing, and synchronization using `pthread_create()` and `pthread_join()` versus automated compiler-managed thread pools in OpenMP.
2. **Work Partitioning**: Divide continuous data structures into non-overlapping index chunks across concurrent worker threads.
3. **Concurrency Hazards**: Identify and reproduce race conditions arising from unsynchronized simultaneous read-modify-write operations on shared variables.
4. **Synchronization Primitives**: Implement deterministic synchronization using mutual exclusion locks (`pthread_mutex_t`) and directive-based critical sections (`#pragma omp critical`).
5. **Thread Coordination**: Enforce phased stage synchronization across teams of threads using barriers (`#pragma omp barrier`).
6. **Empirical Scalability Benchmarking**: Measure execution times, speedup factors, and parallel efficiency across $1, 2, 4, 6,$ and $16$ threads for a massive numerical workload of $10^9$ iterations.

---

## 2. Theoretical & Architectural Comparison

```mermaid
flowchart TD
    subgraph Workload ["Shared Workload (1,000,000,000 Iterations)"]
    end

    Workload --> Seq["Sequential CPU<br/>(1 Worker, Monolithic Loop)"]
    Workload --> Pth["POSIX Threads (Pthreads)<br/>(Explicit Library API, Manual Chunks)"]
    Workload --> Omp["OpenMP Directives<br/>(Compiler Managed, Directive-Based)"]

    Seq --> R1["Execution Time: 1.418s<br/>Speedup: 1.00x"]
    Pth --> R2["Execution Time: 0.136s (16 Thr)<br/>Speedup: 10.40x"]
    Omp --> R3["Execution Time: 0.136s (16 Thr)<br/>Speedup: 10.41x"]
```

### Architectural Breakdown

#### 1. Sequential Execution (Single Worker)
In a sequential architecture, a single CPU core processes loop iterations monotonically from start to finish without concurrency.

```
Sequential Execution (1 Core):
Main Thread ─── Chunk 1 ─── Chunk 2 ─── Chunk 3 ─── Chunk 4 ─── Finish
```

#### 2. POSIX Threads (Pthreads)
Pthreads provides an explicit, low-level C library interface (`<pthread.h>`). The programmer manually defines worker thread functions, manages thread handles (`pthread_t`), computes partition boundaries, and explicitly synchronizes memory using mutexes (`pthread_mutex_t`).

```
Pthreads Explicit Architecture:
                ┌─── Worker Thread 1 ─── Chunk 1 ───┐
                ├─── Worker Thread 2 ─── Chunk 2 ───┤
Master Spawn ───┼─── Worker Thread 3 ─── Chunk 3 ───┼─── pthread_join() ─── Aggregated Result
                └─── Worker Thread 4 ─── Chunk 4 ───┘
```

#### 3. OpenMP (Compiler Directives)
OpenMP provides high-level compiler pragmas (`#pragma omp`). The compiler and runtime handle thread pool initialization, chunk allocation (`schedule`), reduction accumulation (`reduction(+:sum)`), and implicit join barriers at block exits.

```
+-----------------------------------------------------------------------------+
|                           PTHREADS VS. OPENMP COMPARISON                    |
+--------------------------+----------------------------+---------------------+
| Feature                  | POSIX Threads (Pthreads)   | OpenMP              |
+--------------------------+----------------------------+---------------------+
| Paradigm                 | Explicit low-level C API   | Declarative pragmas |
| Thread Spawning          | Manual `pthread_create()`  | `#pragma omp parallel` |
| Thread Joining           | Manual `pthread_join()`    | Automatic barrier   |
| Work Distribution        | Manual index arithmetic    | Automatic loop work-sharing |
| Synchronization          | `pthread_mutex_lock/unlock`| `#pragma omp critical` |
| Reduction                | Manual per-thread arrays   | `reduction(+:var)`  |
| Boilerplate Overhead     | High (~60-90 lines)        | Minimal (~5-10 lines) |
+--------------------------+----------------------------+---------------------+
```

---

## 3. Workload Specification

- **Problem Size ($N$)**: $1,000,000,000$ iterations ($10^9$)
- **Per-Iteration Computation**: $i \times 10^{-6}$
- **Mathematical Invariant & Target Result**:
  $$\text{Target Sum} = \sum_{i=0}^{10^9 - 1} (i \times 10^{-6}) = \mathbf{499999999500.00}$$
- **Hardware Platform**: Multi-core processor with 32 logical threads on WSL2 Ubuntu.

---

## 4. Source Code References

All complete source code implementations are organized inside the [`src/`](src/) directory:

| Section | Paradigm / Concept | Source File Link | Key API / Pragma Highlights |
| :--- | :--- | :--- | :--- |
| **Pthreads** | Single Thread Creation | [`src/pthreads/thread1.c`](src/pthreads/thread1.c) | `pthread_create()`, `pthread_join()` |
| **Pthreads** | Multiple Thread Spawning | [`src/pthreads/thread2.c`](src/pthreads/thread2.c) | Thread ID parameter passing via structs |
| **Pthreads** | Work Distribution & Chunking | [`src/pthreads/thread_sum.c`](src/pthreads/thread_sum.c) | Range chunking & per-thread partial sums |
| **Pthreads** | Race Condition Demonstration | [`src/pthreads/race.c`](src/pthreads/race.c) | Unsynchronized concurrent counter access |
| **Pthreads** | Mutex Mutual Exclusion | [`src/pthreads/mutex.c`](src/pthreads/mutex.c) | `pthread_mutex_lock()`, `pthread_mutex_unlock()` |
| **Pthreads** | Scalability Performance Test | [`src/pthreads/pthread_perf.c`](src/pthreads/pthread_perf.c) | Numerical summation across 1, 2, 4, 6, 16 threads |
| **OpenMP** | Parallel Region & Thread IDs | [`src/openmp/omp1.c`](src/openmp/omp1.c) | `#pragma omp parallel`, `omp_get_thread_num()` |
| **OpenMP** | Work Sharing & Reduction | [`src/openmp/omp_sum.c`](src/openmp/omp_sum.c) | `#pragma omp parallel for reduction(+:sum)` |
| **OpenMP** | Race Condition Hazard | [`src/openmp/omp_race.c`](src/openmp/omp_race.c) | Unprotected shared variable accumulation |
| **OpenMP** | Critical Section Lock | [`src/openmp/omp_critical.c`](src/openmp/omp_critical.c) | `#pragma omp critical` synchronization |
| **OpenMP** | Phased Barrier Coordination | [`src/openmp/omp_barrier.c`](src/openmp/omp_barrier.c) | `#pragma omp barrier` synchronization point |
| **OpenMP** | Scalability Performance Test | [`src/openmp/omp_perf.c`](src/openmp/omp_perf.c) | Numerical summation across 1, 2, 4, 6, 16 threads |
| **Baseline** | Single-Threaded Sequential | [`src/sequential/sequential.c`](src/sequential/sequential.c) | Unthreaded baseline reference implementation |

---

## 5. Empirical Results & Screenshots

### 5.1 Environment Setup & Verification
System verification showing GCC 15.2.0 and active WSL2 Linux environment.

![WSL Environment and GCC Verification](images/00_wsl_gcc_environment.jpeg)

---

### 5.2 Part A — POSIX Threads (Pthreads)

#### Single Thread & Multi-Thread Execution
Creation and joining of single and multiple worker threads with deterministic ID tracking.

| Single Thread Creation (`thread1.c`) | Multiple Thread Spawning (`thread2.c`) |
| :---: | :---: |
| ![Single Thread Execution](images/01_pthread_single_thread.jpeg) | ![Multiple Threads Execution](images/02_pthread_multiple_threads.jpeg) |

#### Work Distribution & Array Chunking (`thread_sum.c`)
Partitioning array indices into uniform chunks and accumulating partial sums.

![Pthread Work Distribution](images/03_pthread_work_distribution_sum.jpeg)

#### Concurrency Hazards & Mutex Fix
Demonstration of data corruption from a race condition versus deterministic correctness restored using `pthread_mutex_t`.

| Race Condition Hazard (`race.c`) | Mutex Synchronization Fix (`mutex.c`) |
| :---: | :---: |
| ![Pthread Race Condition](images/04_pthread_race_condition.jpeg) | ![Pthread Mutex Fixed](images/05_pthread_mutex_fixed.jpeg) |

---

### 5.3 Part B — OpenMP Directives

#### Parallel Region & Thread Teams (`omp1.c`)
Fork-join thread execution across available logical cores.

![OpenMP Parallel Hello](images/06_omp_parallel_hello_32threads.jpeg)

#### Work-Sharing Loops & Reduction (`omp_sum.c`)
Automatic chunk distribution and reduction clause accumulating numerical results.

![OpenMP Sum Reduction](images/07_omp_sum_reduction.jpeg)

#### Data Hazards & Critical Section Synchronization
Data race corruption versus synchronized execution using `#pragma omp critical`.

| OpenMP Race Condition (`omp_race.c`) | OpenMP Critical Section (`omp_critical.c`) |
| :---: | :---: |
| ![OpenMP Race Condition](images/08_omp_race_condition.jpeg) | ![OpenMP Critical Section](images/09_omp_critical_section.jpeg) |

#### Phased Barrier Coordination (`omp_barrier.c`)
Guaranteed phase synchronization where all threads halt until every team member reaches the barrier.

![OpenMP Barrier Synchronization](images/10_omp_barrier_synchronization.jpeg)

---

### 5.4 Part C — Scalability Benchmarks

#### Sequential Baseline Runtime
Single-threaded baseline reference runtime: **`1.418018 seconds`**.

![Sequential Baseline Execution](images/11_sequential_baseline.jpeg)

#### Pthreads Scalability Benchmarks (`pthread_perf.c`)
Execution across 1, 2, 4, 6, and 16 threads showing runtime reduction down to **`0.136414 seconds`**.

![Pthreads Performance Benchmarks](images/12_pthread_perf_all_threads.jpeg)

#### OpenMP Scalability Benchmarks (`omp_perf.c`)
Execution across 1, 2, 4, 6, and 16 threads showing runtime reduction down to **`0.136195 seconds`**.

![OpenMP Performance Benchmarks](images/13_omp_perf_all_threads.jpeg)

---

## 6. Performance Comparison & Visualizations

### 6.1 Measured Execution Time & Scalability Table

| Thread Count ($P$) | Sequential Baseline | Pthreads Time | OpenMP Time | Pthreads Speedup | OpenMP Speedup | Pthreads Efficiency | OpenMP Efficiency |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1 Thread** | 1.418018 s | **1.405171 s** | **1.393317 s** | **1.009×** | **1.018×** | **100.91%** | **101.77%** |
| **2 Threads** | — | **0.718377 s** | **0.717785 s** | **1.974×** | **1.976×** | **98.70%** | **98.78%** |
| **4 Threads** | — | **0.358913 s** | **0.359875 s** | **3.951×** | **3.940×** | **98.77%** | **98.51%** |
| **6 Threads** | — | **0.240157 s** | **0.240754 s** | **5.905×** | **5.890×** | **98.41%** | **98.16%** |
| **16 Threads** | — | **0.136414 s** | **0.136195 s** | **10.395×** | **10.412×** | **64.97%** | **65.07%** |

$$\text{Speedup } (S) = \frac{T_{\text{sequential}}}{T_{\text{parallel}}}, \quad \text{Efficiency } (E) = \frac{S}{P} \times 100\%$$

---

### 6.2 Empirical Performance Charts

#### Comprehensive 3-Panel Benchmark Overview
Comparison of Execution Time, Speedup, and Parallel Efficiency across Pthreads, OpenMP, and the Sequential baseline.

![Performance Comparison Charts](images/performance_comparison_charts.png)

#### Standalone Scaling Curves
| Execution Time Scaling | Speedup vs. Ideal Scaling | Parallel Efficiency (%) |
| :---: | :---: | :---: |
| ![Execution Time vs Threads](images/execution_time_vs_threads.png) | ![Speedup vs Threads](images/speedup_vs_threads.png) | ![Efficiency vs Threads](images/efficiency_vs_threads.png) |

---

## 7. Technical Analysis & Discussion

1. **Near-Linear Physical Core Scaling (1 to 6 Threads)**:
   Between 1 and 6 threads, both Pthreads and OpenMP achieve nearly ideal linear speedup ($1.97\times$ on 2 threads, $3.95\times$ on 4 threads, and $5.90\times$ on 6 threads), maintaining over **$98.4\%$ parallel efficiency**. Because memory access is chunked sequentially per thread, CPU cache lines remain valid with minimal cache coherence overhead.
2. **Parity Between Pthreads and OpenMP**:
   Across all thread counts, OpenMP runtime performance matches Pthreads within a fraction of a millisecond ($0.136195\text{s}$ vs. $0.136414\text{s}$ at 16 threads). This proves that OpenMP's compiler runtime achieves optimal scheduling without runtime abstraction penalties.
3. **Hyper-Threading & Bandwidth Bottleneck (16 Threads)**:
   At 16 threads, speedup reaches **$10.41\times$** rather than theoretical $16\times$, dropping efficiency to **$65.07\%$**. This reflects physical hardware limitations:
   - **Simultaneous Multithreading (SMT)**: Logical hyper-threads share the same physical execution pipeline (ALUs/FPUs), providing 20–35% additional throughput rather than full doubling.
   - **Memory Bus Saturation**: Streaming $10^9$ additions across 16 threads exhausts shared L3 cache lines and saturates memory bus bandwidth.
   - **Amdahl's Law**: Thread spawning, barrier coordination, and final reduction introduce non-parallelizable serial overhead.

---

## 8. Conclusion & Engineering Takeaways

1. **Scalability Ceiling**: Multithreading delivers extraordinary speedups for compute-intensive numerical loops up to the physical core count, after which SMT and memory bandwidth dictate scaling efficiency.
2. **Safety of Synchronization**: Shared memory architectures require rigorous mutual exclusion. Unsynchronized concurrent writes guarantee data race hazards, which can be safely resolved using mutexes or compiler critical sections.
3. **Productivity vs. Control**: OpenMP provides identical execution performance to Pthreads while drastically reducing code complexity and potential human error, making it the preferred choice for loop-level shared-memory parallelism.
