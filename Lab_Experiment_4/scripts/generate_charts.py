#!/usr/bin/env python3
import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs('images', exist_ok=True)

# Typography & theme settings
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Segoe UI', 'Arial']

# Muted, professional engineering palette
c_blue = '#2B5C8F'      # Deep Slate Blue
c_red = '#B85D43'       # Muted Terracotta (Adjacent / False Sharing)
c_green = '#387864'     # Muted Teal / Sage (Padded / Aligned)
c_slate = '#64748B'     # Slate
c_amber = '#C07D3E'     # Warm Amber
c_dark = '#1E293B'      # Dark Charcoal
c_gray = '#475569'      # Medium Slate

# =========================================================================
# 1. Cache Coherence Protocol Bus Transactions & Memory Traffic Chart
# =========================================================================
protocols = ['MSI', 'MESI', 'MOESI']
adjacent_bus_tx = [4000, 3999, 3999]
padded_bus_tx = [4, 2, 2]
writebacks = [1999, 1999, 0]
c2c_transfers = [0, 0, 1999]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 3.8), facecolor='#FAFBFC')

# Panel 1: Bus Transactions
x = np.arange(len(protocols))
width = 0.35

rects1 = ax1.bar(x - width/2, adjacent_bus_tx, width, label='Adjacent (False Sharing)', color=c_red, edgecolor='#334155', linewidth=0.8)
rects2 = ax1.bar(x + width/2, padded_bus_tx, width, label='Padded (Cache Aligned)', color=c_green, edgecolor='#334155', linewidth=0.8)

ax1.set_title('Bus Transactions: False Sharing vs Padded', fontsize=10.5, fontweight='bold', color=c_dark, pad=10)
ax1.set_xlabel('Coherence Protocol', fontsize=9, color=c_gray)
ax1.set_ylabel('Total Bus Transactions', fontsize=9, color=c_gray)
ax1.set_xticks(x)
ax1.set_xticklabels(protocols)
ax1.set_facecolor('#FFFFFF')
ax1.grid(True, linestyle=':', color='#E2E8F0', alpha=0.8)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=7.5)

for r in rects1:
    h = r.get_height()
    ax1.annotate(f'{h}', xy=(r.get_x() + r.get_width()/2, h),
                 xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=8, color=c_dark)

for r in rects2:
    h = r.get_height()
    ax1.annotate(f'{h}', xy=(r.get_x() + r.get_width()/2, h),
                 xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=8, color=c_dark)

# Panel 2: Memory Traffic - Writeback vs Cache-to-Cache Transfer
rects3 = ax2.bar(x - width/2, writebacks, width, label='DRAM Writebacks', color=c_amber, edgecolor='#334155', linewidth=0.8)
rects4 = ax2.bar(x + width/2, c2c_transfers, width, label='C2C Transfers (Owned)', color=c_blue, edgecolor='#334155', linewidth=0.8)

ax2.set_title('DRAM vs Cache-to-Cache Servicing', fontsize=10.5, fontweight='bold', color=c_dark, pad=10)
ax2.set_xlabel('Coherence Protocol', fontsize=9, color=c_gray)
ax2.set_ylabel('Transaction Count', fontsize=9, color=c_gray)
ax2.set_xticks(x)
ax2.set_xticklabels(protocols)
ax2.set_facecolor('#FFFFFF')
ax2.grid(True, linestyle=':', color='#E2E8F0', alpha=0.8)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=7.5)

for r in rects3:
    h = r.get_height()
    ax2.annotate(f'{h}', xy=(r.get_x() + r.get_width()/2, h),
                 xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=8, color=c_dark)

for r in rects4:
    h = r.get_height()
    ax2.annotate(f'{h}', xy=(r.get_x() + r.get_width()/2, h),
                 xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=8, color=c_dark)

plt.tight_layout()
plt.savefig('images/cache_coherence_bus_traffic.png', dpi=150, bbox_inches='tight')
plt.close()

# =========================================================================
# 2. Empirical False Sharing Execution Time & Speedup Scaling Chart
# =========================================================================
threads = [1, 2, 4]
adj_time = [0.0207, 0.0176, 0.0216]
pad_time = [0.0204, 0.0121, 0.0118]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 3.8), facecolor='#FAFBFC')

# Panel 1: Execution Time
ax1.plot(threads, adj_time, marker='o', markersize=6, color=c_red, lw=2, label='Adjacent (False Sharing)')
ax1.plot(threads, pad_time, marker='s', markersize=6, color=c_green, lw=2, linestyle='--', label='Padded (Aligned)')

for t, at, pt in zip(threads, adj_time, pad_time):
    ax1.annotate(f'{at:.4f}s', (t, at), xytext=(-8, 5), textcoords='offset points', fontsize=7.5, color=c_dark)
    ax1.annotate(f'{pt:.4f}s', (t, pt), xytext=(-8, -12), textcoords='offset points', fontsize=7.5, color=c_dark)

ax1.set_title('Execution Time: 100M Increments', fontsize=10.5, fontweight='bold', color=c_dark, pad=10)
ax1.set_xlabel('Threads', fontsize=9, color=c_gray)
ax1.set_ylabel('Seconds (Lower is Better)', fontsize=9, color=c_gray)
ax1.set_xticks(threads)
ax1.set_ylim(0.008, 0.026)
ax1.set_facecolor('#FFFFFF')
ax1.grid(True, linestyle=':', color='#E2E8F0', alpha=0.8)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=7.5)

# Panel 2: Speedup Advantage of Padded Layout
speedup_advantage = [at / pt for at, pt in zip(adj_time, pad_time)]
x_pos = np.arange(len(threads))

bars = ax2.bar(x_pos, speedup_advantage, width=0.45, color=[c_amber, c_slate, c_green], edgecolor='#334155', linewidth=0.8)
for b, val in zip(bars, speedup_advantage):
    ax2.annotate(f'{val:.2f}x', xy=(b.get_x() + b.get_width()/2, val),
                 xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=8, color=c_dark)

ax2.set_title('Padded Layout Speedup Gain over Adjacent', fontsize=10.5, fontweight='bold', color=c_dark, pad=10)
ax2.set_xlabel('Thread Count', fontsize=9, color=c_gray)
ax2.set_ylabel('Speedup Factor', fontsize=9, color=c_gray)
ax2.set_xticks(x_pos)
ax2.set_xticklabels([f'{t}T' for t in threads])
ax2.set_ylim(0, 2.5)
ax2.set_facecolor('#FFFFFF')
ax2.grid(True, linestyle=':', color='#E2E8F0', alpha=0.8)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('images/false_sharing_scaling.png', dpi=150, bbox_inches='tight')
plt.close()

# =========================================================================
# 3. NUMA Memory Sweep Throughput
# =========================================================================
labels = ['1T Default', '1T Bound', '2T Default', '2T Bound']
sweep_times = [0.1152, 0.1027, 0.1108, 0.0984]
total_gb = (512 * 4) / 1024.0  # 2.0 GB
sweep_bw = [total_gb / t for t in sweep_times]

fig, ax1 = plt.subplots(figsize=(6.5, 3.8), facecolor='#FAFBFC')
bar_colors = [c_blue, c_slate, c_blue, c_green]
bars = ax1.bar(labels, sweep_bw, color=bar_colors, width=0.48, edgecolor='#334155', linewidth=0.8)

for b, t_val, bw_val in zip(bars, sweep_times, sweep_bw):
    ax1.annotate(f'{bw_val:.1f} GB/s\n({t_val:.3f}s)', xy=(b.get_x() + b.get_width()/2, bw_val),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=7.5, color=c_dark)

ax1.set_title('NUMA 512 MB Memory Sweep Bandwidth', fontsize=11, fontweight='bold', color=c_dark, pad=10)
ax1.set_ylabel('Throughput (GB/s)', fontsize=9.5, color=c_gray)
ax1.set_ylim(0, 26)
ax1.grid(True, linestyle=':', color='#E2E8F0', alpha=0.8)
ax1.set_facecolor('#FFFFFF')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('images/numa_sweep_latency.png', dpi=150, bbox_inches='tight')
plt.close()

# =========================================================================
# 4. Master 4-Panel Performance Dashboard
# =========================================================================
fig, ((d1, d2), (d3, d4)) = plt.subplots(2, 2, figsize=(9.5, 7.2), facecolor='#FAFBFC')

# Panel 1: Protocol Bus Transactions
d1.bar(x - width/2, adjacent_bus_tx, width, label='Adjacent', color=c_red, edgecolor='#334155', linewidth=0.8)
d1.bar(x + width/2, padded_bus_tx, width, label='Padded', color=c_green, edgecolor='#334155', linewidth=0.8)
d1.set_title('(A) Protocol Bus Transactions', fontsize=10, fontweight='bold', color=c_dark)
d1.set_xticks(x)
d1.set_xticklabels(protocols)
d1.set_ylabel('Transactions', fontsize=8.5, color=c_gray)
d1.grid(True, linestyle=':', color='#E2E8F0', alpha=0.8)
d1.set_facecolor('#FFFFFF')
d1.legend(frameon=True, facecolor='#F8FAFC', fontsize=7.5)

# Panel 2: False Sharing Degradation vs Padded Scaling
d2.plot(threads, adj_time, marker='o', color=c_red, lw=1.8, label='Adjacent')
d2.plot(threads, pad_time, marker='s', color=c_green, lw=1.8, linestyle='--', label='Padded')
d2.set_title('(B) False Sharing: 100M Increments', fontsize=10, fontweight='bold', color=c_dark)
d2.set_xticks(threads)
d2.set_xlabel('Threads', fontsize=8.5, color=c_gray)
d2.set_ylabel('Seconds', fontsize=8.5, color=c_gray)
d2.grid(True, linestyle=':', color='#E2E8F0', alpha=0.8)
d2.set_facecolor('#FFFFFF')
d2.legend(frameon=True, facecolor='#F8FAFC', fontsize=7.5)

# Panel 3: Speedup Factor
d3.bar(['1T', '2T', '4T'], speedup_advantage, color=[c_amber, c_slate, c_green], width=0.45, edgecolor='#334155', linewidth=0.8)
for i, val in enumerate(speedup_advantage):
    d3.annotate(f'{val:.2f}x', xy=(i, val), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=8, color=c_dark)
d3.set_title('(C) Speedup: Padded vs Adjacent', fontsize=10, fontweight='bold', color=c_dark)
d3.set_ylabel('Speedup Factor', fontsize=8.5, color=c_gray)
d3.set_ylim(0, 2.5)
d3.grid(True, linestyle=':', color='#E2E8F0', alpha=0.8)
d3.set_facecolor('#FFFFFF')

# Panel 4: Memory Bandwidth Scaling
d4.bar(labels, sweep_bw, color=bar_colors, width=0.48, edgecolor='#334155', linewidth=0.8)
for i, bw in enumerate(sweep_bw):
    d4.annotate(f'{bw:.1f}', xy=(i, bw), xytext=(0, 2), textcoords="offset points", ha='center', va='bottom', fontsize=7.5, color=c_dark)
d4.set_title('(D) Bandwidth: 512 MB Sweep', fontsize=10, fontweight='bold', color=c_dark)
d4.set_ylabel('GB/s', fontsize=8.5, color=c_gray)
d4.set_ylim(0, 26)
d4.grid(True, linestyle=':', color='#E2E8F0', alpha=0.8)
d4.set_facecolor('#FFFFFF')

plt.suptitle('Experiment 4: Coherence & NUMA Performance Dashboard',
             fontsize=12, fontweight='bold', color=c_dark, y=0.99)
plt.tight_layout()
plt.savefig('images/performance_comparison_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()

print('Experiment 4 charts regenerated with compact sizing and muted palette.')
