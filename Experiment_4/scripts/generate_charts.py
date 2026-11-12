#!/usr/bin/env python3
"""
generate_charts.py - Generates publication-grade performance charts for Experiment 4
Course: Parallel and GPU Computing (26ECAC304) | Experiment 4
"""

import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs('images', exist_ok=True)

# Custom typography & theme settings
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Segoe UI', 'Arial']

# Color palette
c_blue = '#0984E3'      # Intel Blue
c_red = '#D63031'       # Crimson Alert
c_green = '#00B894'     # Mint Teal
c_purple = '#6C5CE7'    # Royal Violet
c_orange = '#E17055'    # Coral Orange
c_yellow = '#FDCB6E'    # Amber
c_dark = '#2D3436'      # Charcoal
c_gray = '#636E72'      # Slate

# =========================================================================
# 1. Cache Coherence Protocol Bus Transactions Chart
# =========================================================================
protocols = ['MSI', 'MESI', 'MOESI']
adjacent_bus_tx = [4000, 3999, 3999]
padded_bus_tx = [4, 2, 2]
writebacks = [1999, 1999, 0]
c2c_transfers = [0, 0, 1999]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), facecolor='#FAFAFA')

# Panel 1: Bus Transactions
x = np.arange(len(protocols))
width = 0.35

rects1 = ax1.bar(x - width/2, adjacent_bus_tx, width, label='Adjacent (False Sharing)', color=c_red, alpha=0.9, edgecolor=c_dark)
rects2 = ax1.bar(x + width/2, padded_bus_tx, width, label='Padded (Cache Aligned)', color=c_green, alpha=0.9, edgecolor=c_dark)

ax1.set_title('Bus Transactions: False Sharing vs Padded', fontsize=12, fontweight='bold', color=c_dark, pad=12)
ax1.set_xlabel('Coherence Protocol', fontsize=11, fontweight='bold', color=c_gray)
ax1.set_ylabel('Total Bus Transactions (Lower is Better)', fontsize=11, fontweight='bold', color=c_gray)
ax1.set_xticks(x)
ax1.set_xticklabels(protocols, fontweight='bold')
ax1.set_facecolor('#FFFFFF')
ax1.grid(True, linestyle=':', color='#DFE6E9', alpha=0.9)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(frameon=True, facecolor='#F1F2F6', edgecolor='#B2BEC3')

for r in rects1:
    h = r.get_height()
    ax1.annotate(f'{h}', xy=(r.get_x() + r.get_width()/2, h),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color=c_red)

for r in rects2:
    h = r.get_height()
    ax1.annotate(f'{h}', xy=(r.get_x() + r.get_width()/2, h),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color=c_green)

# Panel 2: Memory Traffic - Writeback vs Cache-to-Cache Transfer
rects3 = ax2.bar(x - width/2, writebacks, width, label='Forced Memory Writebacks', color=c_orange, alpha=0.9, edgecolor=c_dark)
rects4 = ax2.bar(x + width/2, c2c_transfers, width, label='Cache-to-Cache Transfers (Owned)', color=c_blue, alpha=0.9, edgecolor=c_dark)

ax2.set_title('DRAM Traffic vs Cache-to-Cache Servicing (Adjacent)', fontsize=12, fontweight='bold', color=c_dark, pad=12)
ax2.set_xlabel('Coherence Protocol', fontsize=11, fontweight='bold', color=c_gray)
ax2.set_ylabel('Transaction Count', fontsize=11, fontweight='bold', color=c_gray)
ax2.set_xticks(x)
ax2.set_xticklabels(protocols, fontweight='bold')
ax2.set_facecolor('#FFFFFF')
ax2.grid(True, linestyle=':', color='#DFE6E9', alpha=0.9)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(frameon=True, facecolor='#F1F2F6', edgecolor='#B2BEC3')

for r in rects3:
    h = r.get_height()
    ax2.annotate(f'{h}', xy=(r.get_x() + r.get_width()/2, h),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color=c_orange)

for r in rects4:
    h = r.get_height()
    ax2.annotate(f'{h}', xy=(r.get_x() + r.get_width()/2, h),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color=c_blue)

plt.suptitle('Cache Coherence Protocol Microarchitectural Impact (1000 Iterations / 4000 Ops)',
             fontsize=14, fontweight='bold', color=c_dark, y=1.01)
plt.tight_layout()
plt.savefig('images/cache_coherence_bus_traffic.png', dpi=300, bbox_inches='tight')
plt.close()

# =========================================================================
# 2. False Sharing Execution Time Scaling Chart
# =========================================================================
threads = [1, 2, 4, 8]
adj_time = [0.0213, 0.0132, 0.0179, 0.0306]
pad_time = [0.0208, 0.0109, 0.0060, 0.0068]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), facecolor='#FAFAFA')

# Panel 1: Execution Time
ax1.plot(threads, adj_time, marker='o', markersize=8, color=c_red, lw=2.5, label='Adjacent Layout (False Sharing)')
ax1.plot(threads, pad_time, marker='s', markersize=8, color=c_green, lw=2.5, linestyle='--', label='Padded Layout (64B Aligned)')

for t, at, pt in zip(threads, adj_time, pad_time):
    ax1.annotate(f'{at:.4f}s', (t, at), xytext=(-10, 8), textcoords='offset points', fontsize=8.5, fontweight='bold', color=c_red)
    ax1.annotate(f'{pt:.4f}s', (t, pt), xytext=(-10, -14), textcoords='offset points', fontsize=8.5, fontweight='bold', color=c_green)

ax1.set_title('Execution Time vs Threads (10^8 Increments)', fontsize=12, fontweight='bold', color=c_dark, pad=12)
ax1.set_xlabel('Number of Threads', fontsize=11, fontweight='bold', color=c_gray)
ax1.set_ylabel('Execution Time in Seconds (Lower is Better)', fontsize=11, fontweight='bold', color=c_gray)
ax1.set_xticks(threads)
ax1.set_facecolor('#FFFFFF')
ax1.grid(True, linestyle=':', color='#DFE6E9', alpha=0.9)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(frameon=True, facecolor='#F1F2F6', edgecolor='#B2BEC3')

# Panel 2: Speedup vs Baseline (Single Thread Padded = 0.0208s)
base = pad_time[0]
adj_speedup = [base / t for t in adj_time]
pad_speedup = [base / t for t in pad_time]
ideal_speedup = [1, 2, 4, 8]

ax2.plot(threads, adj_speedup, marker='o', markersize=8, color=c_red, lw=2.5, label='Adjacent Layout (False Sharing)')
ax2.plot(threads, pad_speedup, marker='s', markersize=8, color=c_green, lw=2.5, linestyle='--', label='Padded Layout (Aligned)')
ax2.plot(threads, ideal_speedup, color=c_gray, lw=1.5, linestyle=':', label='Ideal Linear Scaling')

for t, asp, psp in zip(threads, adj_speedup, pad_speedup):
    ax2.annotate(f'{asp:.2f}x', (t, asp), xytext=(-10, 8), textcoords='offset points', fontsize=8.5, fontweight='bold', color=c_red)
    ax2.annotate(f'{psp:.2f}x', (t, psp), xytext=(-10, -14), textcoords='offset points', fontsize=8.5, fontweight='bold', color=c_green)

ax2.set_title('Effective Speedup Factor vs Scaling', fontsize=12, fontweight='bold', color=c_dark, pad=12)
ax2.set_xlabel('Number of Threads', fontsize=11, fontweight='bold', color=c_gray)
ax2.set_ylabel('Speedup Factor (Higher is Better)', fontsize=11, fontweight='bold', color=c_gray)
ax2.set_xticks(threads)
ax2.set_facecolor('#FFFFFF')
ax2.grid(True, linestyle=':', color='#DFE6E9', alpha=0.9)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(frameon=True, facecolor='#F1F2F6', edgecolor='#B2BEC3')

plt.suptitle('Empirical False Sharing Benchmark (100M Increments on Intel Core i5-13420H)',
             fontsize=14, fontweight='bold', color=c_dark, y=1.01)
plt.tight_layout()
plt.savefig('images/false_sharing_scaling.png', dpi=300, bbox_inches='tight')
plt.close()

# =========================================================================
# 3. NUMA Memory Sweep Throughput & Latency Chart
# =========================================================================
numa_threads = [1, 2, 4]
numa_time = [0.1311, 0.1200, 0.1102]
numa_bw = [15.25, 16.66, 18.14]

fig, ax1 = plt.subplots(figsize=(8.5, 5.2), facecolor='#FAFAFA')

color = c_blue
ax1.set_xlabel('Active Threads', fontsize=11, fontweight='bold', color=c_gray)
ax1.set_ylabel('Sweep Execution Time (s)', color=color, fontsize=11, fontweight='bold')
line1 = ax1.plot(numa_threads, numa_time, marker='o', markersize=8, color=color, lw=2.5, label='Execution Time (s)')
ax1.tick_params(axis='y', labelcolor=color)
ax1.set_xticks(numa_threads)
ax1.set_facecolor('#FFFFFF')
ax1.grid(True, linestyle=':', color='#DFE6E9', alpha=0.9)
ax1.spines['top'].set_visible(False)

for t, tm in zip(numa_threads, numa_time):
    ax1.annotate(f'{tm:.4f}s', (t, tm), xytext=(-10, 8), textcoords='offset points', fontsize=9, fontweight='bold', color=color)

ax2 = ax1.twinx()
color = c_purple
ax2.set_ylabel('Effective Throughput (GB/s)', color=color, fontsize=11, fontweight='bold')
line2 = ax2.plot(numa_threads, numa_bw, marker='s', markersize=8, color=color, lw=2.5, linestyle='--', label='Throughput (GB/s)')
ax2.tick_params(axis='y', labelcolor=color)
ax2.spines['top'].set_visible(False)

for t, bw in zip(numa_threads, numa_bw):
    ax2.annotate(f'{bw:.2f} GB/s', (t, bw), xytext=(-10, -14), textcoords='offset points', fontsize=9, fontweight='bold', color=color)

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='center right', frameon=True, facecolor='#F1F2F6', edgecolor='#B2BEC3')

plt.title('NUMA 512 MB Memory Sweep: Throughput & Latency Scaling (4 Passes)',
          fontsize=13, fontweight='bold', color=c_dark, pad=15)
plt.tight_layout()
plt.savefig('images/numa_sweep_latency.png', dpi=300, bbox_inches='tight')
plt.close()

# =========================================================================
# 4. Master 4-Panel Performance Dashboard
# =========================================================================
fig, ((d1, d2), (d3, d4)) = plt.subplots(2, 2, figsize=(16, 12), facecolor='#FAFAFA')

# Dashboard Panel 1: Protocol Bus Transactions
d1.bar(x - width/2, adjacent_bus_tx, width, label='Adjacent (False Sharing)', color=c_red, alpha=0.9, edgecolor=c_dark)
d1.bar(x + width/2, padded_bus_tx, width, label='Padded (Cache Aligned)', color=c_green, alpha=0.9, edgecolor=c_dark)
d1.set_title('(A) Cache Coherence Bus Transactions (1000 Iters)', fontsize=11, fontweight='bold', color=c_dark)
d1.set_xticks(x)
d1.set_xticklabels(protocols, fontweight='bold')
d1.set_ylabel('Bus Transactions', fontsize=10, fontweight='bold', color=c_gray)
d1.grid(True, linestyle=':', color='#DFE6E9', alpha=0.8)
d1.set_facecolor('#FFFFFF')
d1.legend(frameon=True, facecolor='#F1F2F6')

# Dashboard Panel 2: False Sharing Degradation vs Padded Scaling
d2.plot(threads, adj_time, marker='o', color=c_red, lw=2.5, label='Adjacent (False Sharing)')
d2.plot(threads, pad_time, marker='s', color=c_green, lw=2.5, linestyle='--', label='Padded (No False Sharing)')
d2.set_title('(B) False Sharing Penalty: 100M Increments', fontsize=11, fontweight='bold', color=c_dark)
d2.set_xticks(threads)
d2.set_xlabel('Threads', fontsize=10, fontweight='bold', color=c_gray)
d2.set_ylabel('Execution Time (s)', fontsize=10, fontweight='bold', color=c_gray)
d2.grid(True, linestyle=':', color='#DFE6E9', alpha=0.8)
d2.set_facecolor('#FFFFFF')
d2.legend(frameon=True, facecolor='#F1F2F6')

# Dashboard Panel 3: Synchronization Primitives Under Contention (From Lab Benchmarks)
# From WhatsApp image empirical results: None, Critical, Atomic, Lock for 1, 2, 4, 8 threads
sync_threads = [1, 2, 4, 8]
time_none = [0.0075, 0.0084, 0.0100, 0.0156]
time_critical = [0.1175, 0.2617, 0.2892, 0.2555]
time_atomic = [0.0709, 0.1587, 0.1799, 0.1625]
time_lock = [0.1274, 0.3117, 0.3396, 0.3587]

d3.plot(sync_threads, time_none, marker='x', color='#74B9FF', lw=2, linestyle=':', label='None (Faulty Race)')
d3.plot(sync_threads, time_critical, marker='^', color=c_orange, lw=2.2, label='Critical Section')
d3.plot(sync_threads, time_atomic, marker='o', color=c_green, lw=2.5, label='Hardware Atomic')
d3.plot(sync_threads, time_lock, marker='s', color=c_purple, lw=2.2, label='OpenMP Lock (omp_lock_t)')
d3.set_title('(C) Synchronization Primitives Under Contention (10M Ops)', fontsize=11, fontweight='bold', color=c_dark)
d3.set_xticks(sync_threads)
d3.set_xlabel('Threads', fontsize=10, fontweight='bold', color=c_gray)
d3.set_ylabel('Execution Time (s)', fontsize=10, fontweight='bold', color=c_gray)
d3.grid(True, linestyle=':', color='#DFE6E9', alpha=0.8)
d3.set_facecolor('#FFFFFF')
d3.legend(frameon=True, facecolor='#F1F2F6')

# Dashboard Panel 4: Memory Bandwidth Scaling (NUMA Sweep)
d4.bar([str(t) + ' Thread' + ('s' if t > 1 else '') for t in numa_threads], numa_bw, color=[c_blue, '#0984E3', '#00CEC9'], width=0.5, edgecolor=c_dark)
for i, bw in enumerate(numa_bw):
    d4.annotate(f'{bw:.2f} GB/s', xy=(i, bw), xytext=(0, 4), textcoords="offset points", ha='center', fontsize=9.5, fontweight='bold')
d4.set_title('(D) Memory Bandwidth: 512 MB Sweep (4 Passes)', fontsize=11, fontweight='bold', color=c_dark)
d4.set_ylabel('Effective Bandwidth (GB/s)', fontsize=10, fontweight='bold', color=c_gray)
d4.set_ylim(0, 24)
d4.grid(True, linestyle=':', color='#DFE6E9', alpha=0.8)
d4.set_facecolor('#FFFFFF')

plt.suptitle('Experiment 4: Cache Coherence, Memory Access & Synchronization Performance Dashboard',
             fontsize=15, fontweight='bold', color=c_dark, y=0.99)
plt.tight_layout()
plt.savefig('images/performance_comparison_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

print("[+] Successfully generated all publication-grade benchmark charts in images/")
