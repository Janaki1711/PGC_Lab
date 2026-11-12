#!/usr/bin/env python3
"""
generate_charts.py - Generates publication-grade performance charts for Experiment 4
Course: Parallel and GPU Computing (26ECAC304) | Experiment 4

Uses empirical benchmark data measured directly during the laboratory execution.
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
c_red = '#D63031'       # Crimson (False Sharing)
c_green = '#00B894'     # Mint Teal (Padded / Optimal)
c_purple = '#6C5CE7'    # Royal Violet
c_orange = '#E17055'    # Coral Orange
c_dark = '#2D3436'      # Charcoal
c_gray = '#636E72'      # Slate

# =========================================================================
# 1. Cache Coherence Protocol Bus Transactions & Memory Traffic Chart
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
rects3 = ax2.bar(x - width/2, writebacks, width, label='Forced DRAM Writebacks', color=c_orange, alpha=0.9, edgecolor=c_dark)
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
# 2. Empirical False Sharing Execution Time & Speedup Scaling Chart
# =========================================================================
threads = [1, 2, 4]
adj_time = [0.0351, 0.4215, 1.4088]
pad_time = [0.0399, 0.0293, 0.0119]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), facecolor='#FAFAFA')

# Panel 1: Execution Time
ax1.plot(threads, adj_time, marker='o', markersize=9, color=c_red, lw=2.8, label='Adjacent Layout (Severe False Sharing)')
ax1.plot(threads, pad_time, marker='s', markersize=9, color=c_green, lw=2.8, linestyle='--', label='Padded Layout (64B Aligned)')

for t, at, pt in zip(threads, adj_time, pad_time):
    ax1.annotate(f'{at:.4f}s', (t, at), xytext=(-10, 8), textcoords='offset points', fontsize=9, fontweight='bold', color=c_red)
    ax1.annotate(f'{pt:.4f}s', (t, pt), xytext=(-10, -15), textcoords='offset points', fontsize=9, fontweight='bold', color=c_green)

ax1.set_title('Empirical Execution Time: 100M Increments', fontsize=12, fontweight='bold', color=c_dark, pad=12)
ax1.set_xlabel('Active Threads', fontsize=11, fontweight='bold', color=c_gray)
ax1.set_ylabel('Execution Time in Seconds (Lower is Better)', fontsize=11, fontweight='bold', color=c_gray)
ax1.set_xticks(threads)
ax1.set_facecolor('#FFFFFF')
ax1.grid(True, linestyle=':', color='#DFE6E9', alpha=0.9)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(frameon=True, facecolor='#F1F2F6', edgecolor='#B2BEC3')

# Panel 2: Speedup Advantage of Padded Layout over Adjacent Layout
speedup_advantage = [at / pt for at, pt in zip(adj_time, pad_time)]
x_pos = np.arange(len(threads))

bars = ax2.bar(x_pos, speedup_advantage, width=0.45, color=[c_orange, c_purple, c_green], edgecolor=c_dark, alpha=0.9)
for b, val in zip(bars, speedup_advantage):
    ax2.annotate(f'{val:.2f}x\nFaster', xy=(b.get_x() + b.get_width()/2, val),
                 xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=c_dark)

ax2.set_title('Padded Layout Performance Gain over Adjacent', fontsize=12, fontweight='bold', color=c_dark, pad=12)
ax2.set_xlabel('Thread Count', fontsize=11, fontweight='bold', color=c_gray)
ax2.set_ylabel('Speedup Factor (Padded vs Adjacent)', fontsize=11, fontweight='bold', color=c_gray)
ax2.set_xticks(x_pos)
ax2.set_xticklabels([f'{t} Thread{"s" if t > 1 else ""}' for t in threads], fontweight='bold')
ax2.set_ylim(0, 140)
ax2.set_facecolor('#FFFFFF')
ax2.grid(True, linestyle=':', color='#DFE6E9', alpha=0.9)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.suptitle('Empirical False Sharing Benchmark Results (10^8 Increments in Lab Environment)',
             fontsize=14, fontweight='bold', color=c_dark, y=1.01)
plt.tight_layout()
plt.savefig('images/false_sharing_scaling.png', dpi=300, bbox_inches='tight')
plt.close()

# =========================================================================
# 3. NUMA Memory Sweep Throughput & Policy Comparison Chart
# =========================================================================
# 512 MB buffer sweep (4 passes = 2 GB read)
labels = ['1 Thread (Default)', '1 Thread (Node 0)', '2 Threads (Default)', '2 Threads (Node 0)']
sweep_times = [0.1192, 0.1043, 0.0873, 0.0842]
total_gb = (512 * 4) / 1024.0  # 2.0 GB
sweep_bw = [total_gb / t for t in sweep_times]

fig, ax1 = plt.subplots(figsize=(9.5, 5.5), facecolor='#FAFAFA')

colors = [c_blue, '#0984E3', c_purple, '#6C5CE7']
bars = ax1.bar(labels, sweep_bw, color=colors, width=0.5, edgecolor=c_dark, alpha=0.9)

for b, t_val, bw_val in zip(bars, sweep_times, sweep_bw):
    ax1.annotate(f'{bw_val:.2f} GB/s\n({t_val:.4f}s)', xy=(b.get_x() + b.get_width()/2, bw_val),
                 xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=c_dark)

ax1.set_title('NUMA 512 MB Memory Sweep: Throughput & Latency (Default vs Local Node 0)',
              fontsize=13, fontweight='bold', color=c_dark, pad=15)
ax1.set_ylabel('Effective Memory Bandwidth (GB/s)', fontsize=11, fontweight='bold', color=c_gray)
ax1.set_ylim(0, 30)
ax1.grid(True, linestyle=':', color='#DFE6E9', alpha=0.9)
ax1.set_facecolor('#FFFFFF')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

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

# Dashboard Panel 2: False Sharing Execution Time Degradation
d2.plot(threads, adj_time, marker='o', color=c_red, lw=2.8, label='Adjacent (False Sharing)')
d2.plot(threads, pad_time, marker='s', color=c_green, lw=2.8, linestyle='--', label='Padded (No False Sharing)')
d2.set_title('(B) False Sharing Penalty: 100M Increments', fontsize=11, fontweight='bold', color=c_dark)
d2.set_xticks(threads)
d2.set_xlabel('Threads', fontsize=10, fontweight='bold', color=c_gray)
d2.set_ylabel('Execution Time (s)', fontsize=10, fontweight='bold', color=c_gray)
d2.grid(True, linestyle=':', color='#DFE6E9', alpha=0.8)
d2.set_facecolor('#FFFFFF')
d2.legend(frameon=True, facecolor='#F1F2F6')

# Dashboard Panel 3: Padded Speedup Multiplier
d3.bar(['1 Thread', '2 Threads', '4 Threads'], speedup_advantage, color=[c_orange, c_purple, c_green], width=0.45, edgecolor=c_dark)
for i, val in enumerate(speedup_advantage):
    d3.annotate(f'{val:.2f}x Faster', xy=(i, val), xytext=(0, 4), textcoords="offset points", ha='center', fontsize=9.5, fontweight='bold')
d3.set_title('(C) Speedup Factor: Padded vs Adjacent Layout', fontsize=11, fontweight='bold', color=c_dark)
d3.set_ylabel('Speedup Factor', fontsize=10, fontweight='bold', color=c_gray)
d3.set_ylim(0, 140)
d3.grid(True, linestyle=':', color='#DFE6E9', alpha=0.8)
d3.set_facecolor('#FFFFFF')

# Dashboard Panel 4: Memory Bandwidth Scaling (NUMA Sweep)
d4.bar(labels, sweep_bw, color=colors, width=0.5, edgecolor=c_dark, alpha=0.9)
for i, bw in enumerate(sweep_bw):
    d4.annotate(f'{bw:.1f} GB/s', xy=(i, bw), xytext=(0, 4), textcoords="offset points", ha='center', fontsize=9.5, fontweight='bold')
d4.set_title('(D) Memory Bandwidth: 512 MB Sweep (4 Passes)', fontsize=11, fontweight='bold', color=c_dark)
d4.set_ylabel('Throughput (GB/s)', fontsize=10, fontweight='bold', color=c_gray)
d4.set_ylim(0, 30)
d4.tick_params(axis='x', rotation=15)
d4.grid(True, linestyle=':', color='#DFE6E9', alpha=0.8)
d4.set_facecolor('#FFFFFF')

plt.suptitle('Experiment 4: Cache Coherence (MSI/MESI/MOESI) & NUMA Performance Dashboard',
             fontsize=15, fontweight='bold', color=c_dark, y=0.99)
plt.tight_layout()
plt.savefig('images/performance_comparison_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

print("[+] Successfully generated all publication-grade benchmark charts in images/")
