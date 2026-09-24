import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs('images', exist_ok=True)

# Custom typography & theme settings
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Segoe UI', 'Arial']

models = ['Sequential CPU\n(Single-Threaded)', 'MPI Cluster\n(4 VM Nodes)', 'OpenMP\n(8 CPU Threads)', 'CUDA Acceleration\n(NVIDIA GPU)']
times = [244.12, 92.98, 30.83, 0.165]
speedups = [1.0, 2.63, 7.92, 1479.48]

# Distinct modern color palette & hatching patterns
colors = ['#6C5CE7', '#0984E3', '#FD79A8', '#00B894']
hatches = ['///', '\\\\\\', '...', '***']

# 1. Combined Performance Chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5), facecolor='#FAFAFA')

bars1 = ax1.bar(models, times, color=colors, width=0.52, edgecolor='#2D3436', linewidth=1.5)
for bar, hatch in zip(bars1, hatches):
    bar.set_hatch(hatch)

ax1.set_yscale('log')
ax1.set_title('Benchmark Execution Time (Log Scale)', fontsize=14, fontweight='bold', color='#2D3436', pad=15)
ax1.set_ylabel('Execution Time in Seconds (Lower is Better)', fontsize=11, fontweight='bold', color='#636E72')
ax1.grid(True, which='both', linestyle=':', color='#DFE6E9', alpha=0.8)
ax1.set_facecolor('#FFFFFF')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

for bar, time in zip(bars1, times):
    yval = bar.get_height()
    label = f'{time:.2f} s' if time >= 1 else f'{time:.3f} s'
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval * 1.4, label, 
             ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#2D3436',
             bbox=dict(boxstyle='round,pad=0.3', fc='#F1F2F6', ec='#B2BEC3', lw=1))

bars2 = ax2.bar(models, speedups, color=colors, width=0.52, edgecolor='#2D3436', linewidth=1.5)
for bar, hatch in zip(bars2, hatches):
    bar.set_hatch(hatch)

ax2.set_yscale('log')
ax2.set_title('Parallel Speedup Factor (Log Scale)', fontsize=14, fontweight='bold', color='#2D3436', pad=15)
ax2.set_ylabel('Speedup Ratio vs. Sequential (Higher is Better)', fontsize=11, fontweight='bold', color='#636E72')
ax2.grid(True, which='both', linestyle=':', color='#DFE6E9', alpha=0.8)
ax2.set_facecolor('#FFFFFF')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

for bar, speedup in zip(bars2, speedups):
    yval = bar.get_height()
    label = f'{speedup:.2f}x'
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval * 1.4, label, 
             ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#2D3436',
             bbox=dict(boxstyle='round,pad=0.3', fc='#F1F2F6', ec='#B2BEC3', lw=1))

plt.suptitle('Parallel & GPU Computing Lab — Experiment 1 Performance Analysis', fontsize=16, fontweight='bold', color='#2D3436', y=1.02)
plt.tight_layout()
plt.savefig('images/performance_comparison_charts.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Standalone Execution Time Chart
fig, ax = plt.subplots(figsize=(9.5, 6), facecolor='#FAFAFA')
bars = ax.bar(models, times, color=colors, width=0.5, edgecolor='#2D3436', linewidth=1.5)
for bar, hatch in zip(bars, hatches):
    bar.set_hatch(hatch)

ax.set_yscale('log')
ax.set_title('Matrix Multiplication (4000x4000) Execution Time Comparison', fontsize=14, fontweight='bold', color='#2D3436', pad=15)
ax.set_ylabel('Execution Time (Seconds, Log Scale)', fontsize=12, fontweight='bold', color='#636E72')
ax.grid(True, which='both', linestyle=':', color='#DFE6E9', alpha=0.8)
ax.set_facecolor('#FFFFFF')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for bar, time in zip(bars, times):
    yval = bar.get_height()
    label = f'{time:.2f} s' if time >= 1 else f'{time:.3f} s'
    ax.text(bar.get_x() + bar.get_width()/2.0, yval * 1.35, label, 
            ha='center', va='bottom', fontsize=11, fontweight='bold', color='#2D3436',
            bbox=dict(boxstyle='round,pad=0.3', fc='#F1F2F6', ec='#B2BEC3', lw=1))

plt.tight_layout()
plt.savefig('images/execution_time_chart.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Standalone Speedup Chart
fig, ax = plt.subplots(figsize=(9.5, 6), facecolor='#FAFAFA')
bars = ax.bar(models, speedups, color=colors, width=0.5, edgecolor='#2D3436', linewidth=1.5)
for bar, hatch in zip(bars, hatches):
    bar.set_hatch(hatch)

ax.set_yscale('log')
ax.set_title('Parallel Speedup Factor relative to Sequential Baseline', fontsize=14, fontweight='bold', color='#2D3436', pad=15)
ax.set_ylabel('Speedup Factor (x, Log Scale)', fontsize=12, fontweight='bold', color='#636E72')
ax.grid(True, which='both', linestyle=':', color='#DFE6E9', alpha=0.8)
ax.set_facecolor('#FFFFFF')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for bar, speedup in zip(bars, speedups):
    yval = bar.get_height()
    label = f'{speedup:.2f}x'
    ax.text(bar.get_x() + bar.get_width()/2.0, yval * 1.35, label, 
            ha='center', va='bottom', fontsize=11, fontweight='bold', color='#2D3436',
            bbox=dict(boxstyle='round,pad=0.3', fc='#F1F2F6', ec='#B2BEC3', lw=1))

plt.tight_layout()
plt.savefig('images/speedup_chart.png', dpi=300, bbox_inches='tight')
plt.close()

print('Charts regenerated successfully with unique custom palette & styling.')
