# Experiment 4: Cache Coherence (MSI, MESI, MOESI), NUMA Memory Access & Multithreaded Synchronization Analysis

[![Course](https://img.shields.io/badge/Course-Parallel%20%26%20GPU%20Computing-blue.svg)](#)
[![Code](https://img.shields.io/badge/Code-26ECAC304-orange.svg)](#)
[![Protocols](https://img.shields.io/badge/Protocols-MSI%20%7C%20MESI%20%7C%20MOESI-green.svg)](#)
[![Architecture](https://img.shields.io/badge/Architecture-SMP%20%7C%20NUMA%20%7C%20Cache%20Hierarchy-purple.svg)](#)
[![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)](#)

---

## Executive Summary

This study presents an empirical and architectural investigation into **Cache Coherence Protocols (MSI, MESI, MOESI)**, **False Sharing Hazards**, **Non-Uniform Memory Access (NUMA) Latency**, and their direct relationship to **Multi-Threaded Synchronization Primitives** on shared-memory multi-core systems.

By modeling hardware snooping cache coherence through a cycle-accurate protocol simulator, evaluating false sharing on multi-threaded counter workloads across varying cache line strides, measuring NUMA memory sweep bandwidth over 512 MB buffers, and benchmarking concurrency synchronization primitives under high contention, this report uncovers the fundamental hardware mechanisms that govern parallel scalability.

```mermaid
flowchart LR
    subgraph PartA ["1. Cache Coherence Protocols"]
        direction TB
        P1["MSI: 4000 Bus Tx<br/>(1999 Writebacks)"]
        P2["MESI: 3999 Bus Tx<br/>(Silent E to M Upgrade)"]
        P3["MOESI: 3999 Bus Tx<br/>(0 Writebacks, 1999 C2C)"]
    end

    subgraph PartB ["2. False Sharing Evaluation"]
        direction TB
        FS1["Adjacent Layout (Stride = 1)<br/>0.0306s at 8 Threads<br/>Cache Ping-Pong Bottleneck"]
        FS2["Padded Layout (Stride = 8)<br/>0.0068s at 8 Threads<br/>4.50x Performance Gain"]
    end

    subgraph PartC ["3. NUMA & Synchronization"]
        direction TB
        NM["512 MB Memory Sweep<br/>Up to 18.14 GB/s Throughput"]
        SYNC["Hardware Atomics vs Locks<br/>Atomics 2.2x Faster than Locks"]
    end

    PartA --> PartB --> PartC
```

### Key Findings

> 1. **Coherence Protocol Optimization**: Under heavy cache line contention, the **MOESI protocol completely eliminates DRAM write-back traffic** (0 writebacks vs. 1,999 in MSI/MESI over 1,000 iterations) by enabling dirty cache-to-cache transfers via the **Owned ($O$)** state.
> 2. **False Sharing Degradation**: When independent thread counters share a single 64-byte cache line (*adjacent layout*), execution time degrades by **2.32×** as thread count increases from 2 to 8 threads (increasing from 0.0132s to 0.0306s). Aligning data with 64-byte padding (*padded layout*) resolves the cache invalidation storm, reducing execution time to **0.0068s**—yielding a **4.50× speedup** over the adjacent layout.
> 3. **Hardware Atomics vs. Coarse Mutexes**: Fine-grained hardware atomic instructions (`#pragma omp atomic`, compiling to `LOCK XADD`) scale significantly better than OS-level mutexes (`omp_lock_t`), achieving up to **2.21× higher throughput** under severe multi-threaded contention by leveraging hardware-level cache line ownership without thread descheduling overhead.

---

## Table of Contents

1. [Experiment Objectives](#1-experiment-objectives)
2. [Microarchitectural & Theoretical Foundations](#2-microarchitectural--theoretical-foundations)
   - [2.1 The Cache Coherence Problem](#21-the-cache-coherence-problem)
   - [2.2 Protocol State Comparison: MSI, MESI, and MOESI](#22-protocol-state-comparison-msi-mesi-and-moesi)
   - [2.3 Cache Line Granularity & False Sharing](#23-cache-line-granularity--false-sharing)
   - [2.4 NUMA Architecture & First-Touch Memory Policy](#24-numa-architecture--first-touch-memory-policy)
   - [2.5 Synchronization Primitives Under Cache Contention](#25-synchronization-primitives-under-cache-contention)
3. [System Environment & Workload Specifications](#3-system-environment--workload-specifications)
4. [Source Code Structure](#4-source-code-structure)
5. [Empirical Results & Verification Screenshots](#5-empirical-results--verification-screenshots)
   - [5.1 Cache Coherence Protocol Simulation (Part A)](#51-cache-coherence-protocol-simulation-part-a)
   - [5.2 Empirical False Sharing Benchmark (Part B)](#52-empirical-false-sharing-benchmark-part-b)
   - [5.3 NUMA Memory Sweep Throughput (Part C)](#53-numa-memory-sweep-throughput-part-c)
   - [5.4 Empirical Synchronization Benchmark (Part D)](#54-empirical-synchronization-benchmark-part-d)
6. [Performance Visualizations & Benchmark Dashboards](#6-performance-visualizations--benchmark-dashboards)
7. [In-Depth Technical Analysis & Discussion](#7-in-depth-technical-analysis--discussion)
8. [How to Build and Run](#8-how-to-build-and-run)
9. [Conclusion & Engineering Takeaways](#9-conclusion--engineering-takeaways)

---

## 1. Experiment Objectives

- **Protocol Verification**: Implement and simulate the state transitions of **MSI**, **MESI**, and **MOESI** snooping cache coherence protocols, tracking bus read (`BusRd`), read-for-ownership (`BusRdX`), bus upgrade (`BusUpgr`), invalidations, memory write-backs, and cache-to-cache transfers.
- **Quantifying False Sharing**: Expose the hidden performance penalty of false sharing in multi-threaded programs where independent variables reside on the same 64-byte cache line, and validate mitigation via 64-byte memory padding.
- **NUMA Memory Profiling**: Measure memory read bandwidth across a 512 MB memory buffer using OpenMP reduction, evaluating the impact of the Linux first-touch page placement policy.
- **Microarchitectural Concurrency Analysis**: Correlate hardware cache line invalidation traffic with software synchronization primitives (Locks, Semaphores, Barriers, Critical Sections, and Hardware Atomics).

---

## 2. Microarchitectural & Theoretical Foundations

### 2.1 The Cache Coherence Problem

In modern symmetric multiprocessing (SMP) and multi-core architectures, each processing core has private L1 and L2 caches to reduce memory access latency. When multiple cores load the same physical memory address, identical copies reside in multiple private caches. 

If Core 0 modifies its cached copy while Core 1 continues reading its local copy, Core 1 observes stale data. A **Cache Coherence Protocol** enforces a uniform view of memory across all cores via snooping on the shared interconnect or bus.

```mermaid
flowchart TD
    subgraph MultiCore ["Multi-Core Processor"]
        subgraph C0 ["Core 0"]
            L1_0["L1 / L2 Cache (Private)"]
        end
        subgraph C1 ["Core 1"]
            L1_1["L1 / L2 Cache (Private)"]
        end
        subgraph C2 ["Core 2"]
            L1_2["L1 / L2 Cache (Private)"]
        end
        subgraph C3 ["Core 3"]
            L1_3["L1 / L2 Cache (Private)"]
        end
    end

    Interconnect[["Shared System Interconnect / Snooping Bus"]]
    L3["Shared L3 Cache (Last Level Cache)"]
    RAM["Main Memory (DRAM)"]

    L1_0 <--> Interconnect
    L1_1 <--> Interconnect
    L1_2 <--> Interconnect
    L1_3 <--> Interconnect
    Interconnect <--> L3 <--> RAM
```

### 2.2 Protocol State Comparison: MSI, MESI, and MOESI

| State | Protocol | Description | Memory Clean? | Multiple Copies Permitted? |
| :--- | :--- | :--- | :---: | :---: |
| **M** (Modified) | MSI, MESI, MOESI | Cache holds the sole valid copy; dirty relative to DRAM. | No (Dirty) | No |
| **O** (Owned) | MOESI only | Cache holds dirty data and acts as owner; supplies data to other caches directly without writing back to DRAM. | No (Dirty) | Yes (as Shared) |
| **E** (Exclusive) | MESI, MOESI | Cache holds the sole copy; clean relative to DRAM. Can transition to $M$ silently with zero bus traffic. | Yes (Clean) | No |
| **S** (Shared) | MSI, MESI, MOESI | One of several valid copies; clean or owned by an $O$-state cache. Read-only. | Yes (or owned) | Yes |
| **I** (Invalid) | MSI, MESI, MOESI | Block contains invalid or stale data; any read requires a bus request. | N/A | N/A |

#### Key Protocol Distinctions:
1. **MSI**: Baseline 3-state protocol. Even if data is private to a core, the core must issue a `BusUpgr` on its first write, generating bus contention.
2. **MESI (Intel MESIF variant)**: Introduces the **Exclusive ($E$)** state. A private clean cache line can be upgraded to **Modified ($M$)** *silently* without broadcasting to the bus (`silent E->M`), significantly accelerating private data updates.
3. **MOESI (AMD variant)**: Introduces the **Owned ($O$)** state. When Core 1 reads data held dirty in Core 0's cache, Core 0 transitions to $O$ and directly serves the cache line to Core 1 via a cache-to-cache transfer ($C2C$), deferring DRAM write-back until eviction.

---

### 2.3 Cache Line Granularity & False Sharing

Cache coherence is tracked at the granularity of a **Cache Line** (standard 64 bytes on x86-64), not individual primitive variables.

```
+---------------------------------------------------------------+
|                      64-Byte Cache Line                       |
+---------------+---------------+---------------+---------------+
|  Counter 0    |  Counter 1    |  Counter 2    |  Counter 3    |
|   (Thread 0)  |   (Thread 1)  |   (Thread 2)  |   (Thread 3)  |
|    8 Bytes    |    8 Bytes    |    8 Bytes    |    8 Bytes    |
+---------------+---------------+---------------+---------------+
|<----------------------- SHARED LINE ------------------------->|
```

- **Adjacent Layout (False Sharing)**: Thread 0 writes to `cnt[0]` and Thread 1 writes to `cnt[1]`. Although logically independent, both variables share the identical 64-byte cache line. Every write by Thread 0 invalidates Thread 1's entire cache line, forcing Thread 1 into a cache miss and bus read. The cache line bounces between cores (*cache ping-pong*), severely degrading throughput.
- **Padded Layout (Mitigation)**: Inserting 64-byte padding (`stride = 8` for 64-bit `long` integers) ensures each thread's variable occupies an independent cache line. Cores write to their private lines concurrently without triggering invalidations.

---

### 2.4 NUMA Architecture & First-Touch Memory Policy

In a **Non-Uniform Memory Access (NUMA)** system, physical RAM is segmented into distinct nodes associated with specific processor sockets.
- **Local Access**: A core accessing memory attached to its local node achieves minimal latency and maximum bus bandwidth.
- **Remote Access**: Accessing memory attached to another node requires crossing an inter-socket interconnect (e.g., Intel UPI or AMD Infinity Fabric), introducing latency and memory bus contention.
- **First-Touch Policy**: Linux allocates physical pages to the NUMA node of the thread that first writes to the page (`memset` or first store), rather than the thread that allocated it with `malloc()`.

---

### 2.5 Synchronization Primitives Under Cache Contention

Software synchronization mechanisms interact directly with hardware cache coherence:
- **Critical Section (`#pragma omp critical`)**: Enforces coarse-grained compiler/runtime mutual exclusion. Threads serialize execution, causing substantial context switching and cache line invalidation overhead.
- **OpenMP Lock (`omp_lock_t`)**: Implements OS/runtime mutex locks. Under high contention, threads repeatedly poll or sleep, triggering lock bouncing across caches.
- **Hardware Atomic (`#pragma omp atomic`)**: Emits single indivisible machine instructions (e.g., `LOCK XADD` on x86-64). The CPU asserts a cache lock on the specific cache line, performing the read-modify-write entirely within L1 cache in Modified state without releasing lock ownership to the OS.

---

## 3. System Environment & Workload Specifications

### Hardware Environment

| Component | Specification |
| :--- | :--- |
| **Processor** | 13th Gen Intel(R) Core(TM) i5-13420H |
| **Microarchitecture** | Raptor Lake (Intel 7 Process) |
| **Total Cores / Threads** | 8 Physical Cores (4 P-cores + 4 E-cores) / 12 Hardware Threads |
| **L1 Data Cache** | 288 KiB (6 instances × 48 KB) |
| **L1 Instruction Cache** | 192 KiB (6 instances × 32 KB) |
| **L2 Cache** | 7.5 MiB (6 instances) |
| **L3 Cache (Shared LLC)** | 12.0 MiB Unified Smart Cache |
| **Host Operating System** | Ubuntu 22.04 LTS (WSL2 / VMware Virtualized Kernel 5.15) |
| **Compiler Toolchain** | GCC 15.2.0 (with OpenMP 4.5 / libgomp support) |

### Benchmark Workloads

1. **Protocol Simulation Workload**: 1,000 trace iterations ($4,000$ memory operations) between Core 0 and Core 1 alternating reads and writes on counters $X$ and $Y$.
2. **False Sharing Benchmark Workload**: $100,000,000$ ($10^8$) cumulative counter increments across 1, 2, 4, and 8 threads under adjacent (`stride = 1`) and padded (`stride = 8`) layouts.
3. **NUMA Memory Sweep Workload**: 512 MB contiguous buffer read sequentially across 4 complete traversal passes (reading 1 byte per 64-byte cache line).
4. **Synchronization Contention Workload**: $10,000,000$ ($10^7$) shared increments evaluated across None, Critical, Atomic, and Lock mechanisms for 1, 2, 4, and 8 threads.

---

## 4. Source Code Structure

All source implementations are maintained under the [`src/`](src/) directory:

```
Experiment_4/
├── README.md                                          # Master Experiment Report & Architectural Analysis
├── .gitignore                                         # Build artifact exclusions
├── docs/
│   └── Exp_4_Cache_Coherence_NUMA.pdf                 # Lab Experiment Specification & Syllabus Reference
├── images/
│   ├── 01_env_and_race_execution.jpeg                 # Lab VM execution log: environment & race condition
│   ├── 02_race_and_critical_execution.jpeg            # Lab VM execution log: critical section verification
│   ├── 03_synchronization_primitives_execution.jpeg   # Lab VM execution log: all primitives execution
│   ├── 04_sync_empirical_benchmark_table.jpeg         # Lab VM execution log: 10M empirical benchmark table
│   ├── cache_coherence_bus_traffic.png                # Visualization: protocol bus transactions & writebacks
│   ├── false_sharing_scaling.png                      # Visualization: false sharing degradation vs padded scaling
│   ├── numa_sweep_latency.png                         # Visualization: memory sweep throughput & latency
│   └── performance_comparison_dashboard.png           # Visualization: comprehensive 4-panel dashboard
├── scripts/
│   └── generate_charts.py                             # Automated chart generation script (Matplotlib)
└── src/
    ├── Makefile                                       # Automated compilation rules
    ├── coherence_sim.py                               # 2-core snooping cache protocol simulator (MSI, MESI, MOESI)
    ├── false_sharing.c                                # False sharing benchmark: adjacent vs padded layouts
    ├── numa_sweep.c                                   # 512 MB memory sweep bandwidth benchmark
    ├── compare_numa.c                                 # Master False Sharing & NUMA evaluation program
    ├── lock.c                                         # OpenMP runtime mutex implementation (omp_lock_t)
    └── performance.c                                  # Micro-benchmark: Critical section vs Hardware Atomic
```

---

## 5. Empirical Results & Verification Screenshots

### 5.1 Cache Coherence Protocol Simulation (Part A)

#### State Transition Trace (First 2 Iterations, Adjacent Layout)

```
======================================================================
CACHE COHERENCE PROTOCOL SIMULATOR (MSI vs MESI vs MOESI)
======================================================================

Protocol: MSI
  Core 0 Reads  line A -> State: [C0=S, C1=I]
  Core 0 Writes line A -> State: [C0=M, C1=I]
  Core 1 Reads  line A -> State: [C0=S, C1=S]
  Core 1 Writes line A -> State: [C0=I, C1=M]
  Core 0 Reads  line A -> State: [C0=S, C1=S]
  Core 0 Writes line A -> State: [C0=M, C1=I]
  Core 1 Reads  line A -> State: [C0=S, C1=S]
  Core 1 Writes line A -> State: [C0=I, C1=M]

Protocol: MESI
  Core 0 Reads  line A -> State: [C0=E, C1=I]
  Core 0 Writes line A -> State: [C0=M, C1=I]
  Core 1 Reads  line A -> State: [C0=S, C1=S]
  Core 1 Writes line A -> State: [C0=I, C1=M]
  Core 0 Reads  line A -> State: [C0=S, C1=S]
  Core 0 Writes line A -> State: [C0=M, C1=I]
  Core 1 Reads  line A -> State: [C0=S, C1=S]
  Core 1 Writes line A -> State: [C0=I, C1=M]

Protocol: MOESI
  Core 0 Reads  line A -> State: [C0=E, C1=I]
  Core 0 Writes line A -> State: [C0=M, C1=I]
  Core 1 Reads  line A -> State: [C0=O, C1=S]
  Core 1 Writes line A -> State: [C0=I, C1=M]
  Core 0 Reads  line A -> State: [C0=S, C1=O]
  Core 0 Writes line A -> State: [C0=M, C1=I]
  Core 1 Reads  line A -> State: [C0=O, C1=S]
  Core 1 Writes line A -> State: [C0=I, C1=M]
```

#### Protocol Transaction Totals (1,000 Iterations / 4,000 Operations)

| Layout | Protocol | Bus Transactions | BusRd | BusRdX | BusUpgr | Invalidations | Memory Writebacks | Cache-to-Cache ($C2C$) | Silent $E \to M$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Adjacent** | **MSI** | `4000` | `2000` | `0` | `2000` | `1999` | `1999` | `0` | `0` |
| **Adjacent** | **MESI** | `3999` | `2000` | `0` | `1999` | `1999` | `1999` | `0` | `1` |
| **Adjacent** | **MOESI** | `3999` | `2000` | `0` | `1999` | `1999` | **`0`** | **`1999`** | `1` |
| **Padded** | **MSI** | `4` | `2` | `0` | `2` | `0` | `0` | `0` | `0` |
| **Padded** | **MESI** | `2` | `2` | `0` | `0` | `0` | `0` | `0` | `2` |
| **Padded** | **MOESI** | `2` | `2` | `0` | `0` | `0` | `0` | `0` | `2` |

---

### 5.2 Empirical False Sharing Benchmark (Part B)

Empirical execution of `compare_numa` on the 12-thread host machine for $100,000,000$ increments:

| Layout Configuration | Thread Count ($P$) | Final Verified Count | Deterministic Status | Execution Time (s) | Relative Speedup vs 1T |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Adjacent (False Sharing)** | 1 | `100000000` | Correct | `0.0213` | 0.98× |
| **Padded (Aligned)** | 1 | `100000000` | Correct | `0.0208` | 1.00× (Baseline) |
| **Adjacent (False Sharing)** | 2 | `100000000` | Correct | `0.0132` | 1.58× |
| **Padded (Aligned)** | 2 | `100000000` | Correct | `0.0109` | **1.91×** |
| **Adjacent (False Sharing)** | 4 | `100000000` | Correct | `0.0179` | 1.16× (Degrading) |
| **Padded (Aligned)** | 4 | `100000000` | Correct | `0.0060` | **3.47×** |
| **Adjacent (False Sharing)** | 8 | `100000000` | Correct | `0.0306` | **0.68× (Severe Penalty)** |
| **Padded (Aligned)** | 8 | `100000000` | Correct | `0.0068` | **3.06× (Optimal)** |

> **Key Observation**: At 8 threads, false sharing slows down execution to **0.0306 seconds**, which is slower than single-threaded execution (0.0208s). Padding the counters eliminates this line contention, completing in **0.0068 seconds** (**4.50× faster** than adjacent).

---

### 5.3 NUMA Memory Sweep Throughput (Part C)

512 MB memory buffer traversal across 4 passes ($2.0$ GB total memory read):

| Thread Count ($P$) | Execution Time (s) | Effective Memory Bandwidth (GB/s) | Scaling Factor |
| :---: | :---: | :---: | :---: |
| **1 Thread** | `0.1311` | `15.25 GB/s` | 1.00× |
| **2 Threads** | `0.1200` | `16.66 GB/s` | 1.09× |
| **4 Threads** | `0.1102` | `18.14 GB/s` | 1.19× |

---

### 5.4 Empirical Synchronization Benchmark (Part D)

Empirical data recorded during the laboratory session comparing synchronization models over $10,000,000$ shared updates:

| Mechanism | Threads ($P$) | Final Counter Value | Correctness Status | Execution Time (s) | Throughput (MOps/s) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **None (Unsynchronized)** | 1 | `10000000` | Correct | `0.0075` | 1333.3 |
| **Critical Section** | 1 | `10000000` | Correct | `0.1175` | 85.1 |
| **Hardware Atomic** | 1 | `10000000` | Correct | `0.0709` | 141.0 |
| **OpenMP Lock** | 1 | `10000000` | Correct | `0.1274` | 78.5 |
| **None (Unsynchronized)** | 2 | `6912581` | **INCORRECT (30.87% lost)** | `0.0084` | 1190.5 |
| **Critical Section** | 2 | `10000000` | Correct | `0.2617` | 38.2 |
| **Hardware Atomic** | 2 | `10000000` | Correct | `0.1587` | **63.0** |
| **OpenMP Lock** | 2 | `10000000` | Correct | `0.3117` | 32.1 |
| **None (Unsynchronized)** | 4 | `5043596` | **INCORRECT (49.56% lost)** | `0.0100` | 1000.0 |
| **Critical Section** | 4 | `10000000` | Correct | `0.2892` | 34.6 |
| **Hardware Atomic** | 4 | `10000000` | Correct | `0.1799` | **55.6** |
| **OpenMP Lock** | 4 | `10000000` | Correct | `0.3396` | 29.4 |
| **None (Unsynchronized)** | 8 | `8830290` | **INCORRECT (11.70% lost)** | `0.0156` | 641.0 |
| **Critical Section** | 8 | `10000000` | Correct | `0.2555` | 39.1 |
| **Hardware Atomic** | 8 | `10000000` | Correct | `0.1625` | **61.5** |
| **OpenMP Lock** | 8 | `10000000` | Correct | `0.3587` | 27.9 |

---

### Laboratory Execution Screenshots

#### Screenshot 1: Environment Setup & Race Condition Verification
Execution of `./race` in the laboratory virtual machine environment showing initial race hazards:

![Environment and Race Condition](images/01_env_and_race_execution.jpeg)

---

#### Screenshot 2: Critical Section Verification
Execution showing deterministic mutual exclusion via `./critical`:

![Race and Critical Section](images/02_race_and_critical_execution.jpeg)

---

#### Screenshot 3: Multi-Primitive Execution & Performance Micro-Benchmark
Execution verifying all synchronization primitives (`./race`, `./critical`, `./atomic`, `./barrier`, `./semaphore`, `./lock`, and `./performance`):
- `Critical time = 0.027345 seconds`
- `Atomic time = 0.008758 seconds` (Hardware Atomics run **3.12× faster** than Critical sections on 1M iterations)

![All Primitives Execution](images/03_synchronization_primitives_execution.jpeg)

---

#### Screenshot 4: Empirical Benchmark Table (`compare_sync_output.txt`)
Direct terminal output confirming synchronization times, lost update counts, and scaling characteristics:

![Empirical Benchmark Output](images/04_sync_empirical_benchmark_table.jpeg)

---

## 6. Performance Visualizations & Benchmark Dashboards

### 6.1 Cache Coherence Protocol Bus Transactions & Memory Traffic

Comparison of bus transactions and DRAM writebacks across MSI, MESI, and MOESI:

![Cache Coherence Bus Traffic](images/cache_coherence_bus_traffic.png)

---

### 6.2 False Sharing Degradation vs. Padded Scaling

Empirical scaling curves illustrating the severe penalty of adjacent cache line layout versus 64-byte padding:

![False Sharing Scaling](images/false_sharing_scaling.png)

---

### 6.3 NUMA Memory Sweep Throughput & Latency

Memory throughput (GB/s) scaling for the 512 MB buffer sweep:

![NUMA Memory Sweep](images/numa_sweep_latency.png)

---

### 6.4 Comprehensive 4-Panel Master Benchmark Dashboard

Integrated multi-panel dashboard covering protocols, false sharing, synchronization primitives, and memory bandwidth:

![Master Performance Dashboard](images/performance_comparison_dashboard.png)

---

## 7. In-Depth Technical Analysis & Discussion

### 7.1 Microarchitectural Comparison: MSI vs. MESI vs. MOESI

1. **Why MSI Incurs Extra Bus Overhead**:
   In MSI, a core that reads a line in state $I$ transitions to $S$. When it subsequently writes to that line, it must broadcast a `BusUpgr` to invalidate potential copies, even if no other core holds the line. In the benchmark, MSI required **2,000 BusUpgr transactions**.
2. **The Power of MESI's Exclusive ($E$) State**:
   MESI checks if any other cache holds the line during the initial read. If no other cache holds it, the line transitions directly to $E$ (Exclusive Clean). When the core subsequently writes to it, it transitions silently from $E \to M$ without placing any command on the shared bus (`silent E->M = 1` in our trace, and `2` for padded layout).
3. **MOESI's Owned ($O$) State Eliminates DRAM Write-Backs**:
   In MSI and MESI, when a dirty line in state $M$ is requested for reading by another core, the owner must flush the line back to main memory via a costly bus write-back (`1,999 writebacks` in MSI/MESI). 
   In MOESI, the owner transitions the line from $M \to O$ and satisfies the read request directly via an on-chip **Cache-to-Cache ($C2C$) transfer** (`1,999 C2C transfers`, **0 writebacks**). This drastically cuts memory bus traffic and prevents DRAM bandwidth saturation.

---

### 7.2 False Sharing: The Mechanics of Cache Line Ping-Pong

In the adjacent counter experiment (`stride = 1`), both `cnt[0]` and `cnt[1]` reside on the same 64-byte cache line:
$$\text{Address of } cnt[0] = 0\text{x}00, \quad \text{Address of } cnt[1] = 0\text{x}08$$

1. Core 0 writes `cnt[0]` $\implies$ Line transitions to Modified ($M$) in Core 0's L1 cache; Core 1's copy is marked Invalid ($I$).
2. Core 1 writes `cnt[1]` $\implies$ Core 1 suffers a cache write miss (BusRdX); Core 0 flushes or transfers line; Core 1 transitions line to $M$; Core 0's copy is marked $I$.
3. This cycle repeats $100,000,000$ times. The execution time rises from **0.0132s at 2 threads** to **0.0306s at 8 threads** due to severe interconnect saturation.
4. With **padded layout** (`stride = 8`), $\text{offset} = 8 \times 8 = 64\text{ bytes}$, placing each thread counter on a distinct cache line. Cores write exclusively to their private L1 lines, completing in **0.0068s** (**4.50× faster**).

---

### 7.3 Synchronization Under Contention: Hardware Atomics vs. Locks

Under high concurrency, software synchronization performance is dominated by cache line bouncing:
- **`#pragma omp critical` (0.2555s at 8T)**: Implements coarse locking through compiler-generated calls into the OpenMP runtime library (`libgomp`). Every thread acquiring the section incurs function call overhead and memory barriers.
- **`omp_lock_t` (0.3587s at 8T)**: Under heavy contention, multiple threads spin and poll the lock word, causing continuous invalidation of the lock cache line across all participating cores.
- **`#pragma omp atomic` (0.1625s at 8T)**: Hardware atomics translate directly into the x86 `LOCK XADD` instruction. Rather than stalling thread execution or descheduling threads, the hardware cache controller locks only the specific cache line for the few clock cycles needed to increment the register and store to L1. As a result, atomics deliver **2.21× higher throughput than locks** while ensuring absolute correctness.

---

## 8. How to Build and Run

### Prerequisites

Ensure GCC with OpenMP and Python 3 are installed on your Linux / WSL environment:

```bash
sudo apt update
sudo apt install build-essential numactl hwloc python3 python3-pip -y
pip install matplotlib numpy
```

### Build All Implementations

```bash
cd Experiment_4/src
make all
```

### Run Benchmarks

```bash
# 1. Run the Cache Coherence Protocol Simulator
python3 coherence_sim.py 1000

# 2. Run False Sharing Benchmark (Adjacent vs Padded)
OMP_NUM_THREADS=2 ./false_sharing adjacent
OMP_NUM_THREADS=2 ./false_sharing padded
OMP_NUM_THREADS=8 ./false_sharing adjacent
OMP_NUM_THREADS=8 ./false_sharing padded

# 3. Run NUMA Memory Sweep Benchmark
OMP_NUM_THREADS=4 ./numa_sweep 512

# 4. Run Master False Sharing & NUMA Evaluation Program
./compare_numa

# 5. Run Under numactl (if NUMA nodes are configured)
numactl --cpunodebind=0 --membind=0 ./compare_numa   # Local memory
numactl --cpunodebind=0 --membind=1 ./compare_numa   # Remote memory
```

### Generate Publication-Grade Visualizations

```bash
cd Experiment_4
python scripts/generate_charts.py
```

All generated `.png` figures are automatically saved to `Experiment_4/images/`.

---

## 9. Conclusion & Engineering Takeaways

1. **Protocol Selection Impact**:
   - For workloads with high read-after-write sharing across multiple cores, protocols featuring an **Owned state (MOESI)** dramatically decrease memory bus saturation by replacing DRAM write-backs with low-latency cache-to-cache interconnect transfers.
   - For private or read-mostly data, protocols with an **Exclusive state (MESI / MOESI)** completely eliminate bus upgrade broadcasts via silent state transitions.
2. **Cache-Conscious Data Structure Layout**:
   - False sharing is an invisible performance destroyer in multi-threaded code. Simply ensuring independent thread write targets are separated by at least **64 bytes** (e.g., using `alignas(64)` in C++ or padding arrays to cache-line multiples in C) recovers up to **4.50× performance**.
3. **Concurrency Primitive Selection**:
   - Avoid OS-level mutexes and critical sections for simple counter updates or reductions.
   - Prefer **Hardware Atomics (`#pragma omp atomic`)** or OpenMP **Reductions (`reduction(+:var)`)**, which utilize private accumulator registers and hardware cache locking to maximize throughput under extreme thread contention.
