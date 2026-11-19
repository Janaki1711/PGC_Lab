import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs('images', exist_ok=True)

# Typography & theme settings
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Segoe UI', 'Arial']

models = ['Sequential CPU\n(1 Core)', 'MPI Cluster\n(4 VM Nodes)', 'OpenMP\n(8 Threads)', 'CUDA GPU\n(RTX 5060 Ti)']
times = [244.12, 92.98, 30.83, 0.211]
speedups = [1.0, 2.63, 7.92, 1155.63]

# Muted, professional engineering palette
colors = ['#64748B', '#3B82A6', '#2B5C8F', '#387864']

# 1. Combined Performance Chart (Compact 2-Panel)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), facecolor='#FAFBFC')

# Execution Time
bars1 = ax1.bar(models, times, color=colors, width=0.48, edgecolor='#334155', linewidth=1)
ax1.set_yscale('log')
ax1.set_title('Execution Time (Log Scale, Lower is Better)', fontsize=11, fontweight='bold', color='#1E293B', pad=10)
ax1.set_ylabel('Seconds', fontsize=10, color='#475569')
ax1.grid(True, which='both', linestyle=':', color='#E2E8F0', alpha=0.8)
ax1.set_facecolor('#FFFFFF')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.tick_params(axis='x', labelsize=8.5)

for bar, time in zip(bars1, times):
    yval = bar.get_height()
    label = f'{time:.2f}s' if time >= 1 else f'{time:.3f}s'
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval * 1.35, label, 
             ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1E293B')

# Speedup Factor
bars2 = ax2.bar(models, speedups, color=colors, width=0.48, edgecolor='#334155', linewidth=1)
ax2.set_yscale('log')
ax2.set_title('Parallel Speedup Factor (Higher is Better)', fontsize=11, fontweight='bold', color='#1E293B', pad=10)
ax2.set_ylabel('Speedup (x vs. Sequential)', fontsize=10, color='#475569')
ax2.grid(True, which='both', linestyle=':', color='#E2E8F0', alpha=0.8)
ax2.set_facecolor('#FFFFFF')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.tick_params(axis='x', labelsize=8.5)

for bar, speedup in zip(bars2, speedups):
    yval = bar.get_height()
    label = f'{speedup:.1f}x'
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval * 1.35, label, 
             ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1E293B')

plt.tight_layout()
plt.savefig('images/performance_comparison_charts.png', dpi=150, bbox_inches='tight')
plt.close()

# 2. Standalone Execution Time Chart
fig, ax = plt.subplots(figsize=(7, 4), facecolor='#FAFBFC')
bars = ax.bar(models, times, color=colors, width=0.48, edgecolor='#334155', linewidth=1)
ax.set_yscale('log')
ax.set_title('Matrix Multiplication (4000x4000) Execution Time', fontsize=11, fontweight='bold', color='#1E293B', pad=10)
ax.set_ylabel('Execution Time in Seconds (Log Scale)', fontsize=10, color='#475569')
ax.grid(True, which='both', linestyle=':', color='#E2E8F0', alpha=0.8)
ax.set_facecolor('#FFFFFF')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='x', labelsize=8.5)

for bar, time in zip(bars, times):
    yval = bar.get_height()
    label = f'{time:.2f}s' if time >= 1 else f'{time:.3f}s'
    ax.text(bar.get_x() + bar.get_width()/2.0, yval * 1.35, label, 
            ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1E293B')

plt.tight_layout()
plt.savefig('images/execution_time_chart.png', dpi=150, bbox_inches='tight')
plt.close()

# 3. Standalone Speedup Chart
fig, ax = plt.subplots(figsize=(7, 4), facecolor='#FAFBFC')
bars = ax.bar(models, speedups, color=colors, width=0.48, edgecolor='#334155', linewidth=1)
ax.set_yscale('log')
ax.set_title('Parallel Speedup Factor relative to Sequential Baseline', fontsize=11, fontweight='bold', color='#1E293B', pad=10)
ax.set_ylabel('Speedup Factor (x)', fontsize=10, color='#475569')
ax.grid(True, which='both', linestyle=':', color='#E2E8F0', alpha=0.8)
ax.set_facecolor('#FFFFFF')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='x', labelsize=8.5)

for bar, speedup in zip(bars, speedups):
    yval = bar.get_height()
    label = f'{speedup:.1f}x'
    ax.text(bar.get_x() + bar.get_width()/2.0, yval * 1.35, label, 
            ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1E293B')

plt.tight_layout()
plt.savefig('images/speedup_chart.png', dpi=150, bbox_inches='tight')
plt.close()

print('Experiment 1 charts regenerated with compact sizing and muted palette.')
