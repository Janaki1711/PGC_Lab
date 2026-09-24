import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs('images', exist_ok=True)

models = ['Sequential CPU', 'MPI (4 VMs)', 'OpenMP (8 Threads)', 'CUDA (NVIDIA GPU)']
times = [244.12, 92.98, 30.83, 0.165]
speedups = [1.0, 2.63, 7.92, 1479.48]
colors = ['#e74c3c', '#f39c12', '#2980b9', '#27ae60']

# 1. Combined Chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

bars1 = ax1.bar(models, times, color=colors, width=0.55, edgecolor='black', linewidth=1.2)
ax1.set_yscale('log')
ax1.set_title('Execution Time Comparison (Log Scale)', fontsize=14, fontweight='bold', pad=15)
ax1.set_ylabel('Execution Time (Seconds)', fontsize=12, fontweight='bold')
ax1.grid(True, which='both', linestyle='--', alpha=0.5)

for bar, time in zip(bars1, times):
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval * 1.3, f'{time:.2f}s' if time >= 1 else f'{time:.3f}s', 
             ha='center', va='bottom', fontsize=11, fontweight='bold')

bars2 = ax2.bar(models, speedups, color=colors, width=0.55, edgecolor='black', linewidth=1.2)
ax2.set_yscale('log')
ax2.set_title('Speedup relative to Sequential Baseline', fontsize=14, fontweight='bold', pad=15)
ax2.set_ylabel('Speedup Factor (x)', fontsize=12, fontweight='bold')
ax2.grid(True, which='both', linestyle='--', alpha=0.5)

for bar, speedup in zip(bars2, speedups):
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval * 1.3, f'{speedup:.2f}x', 
             ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('images/performance_comparison_charts.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Standalone Execution Time Chart
fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.bar(models, times, color=colors, width=0.5, edgecolor='black', linewidth=1.2)
ax.set_yscale('log')
ax.set_title('Matrix Multiplication (4000x4000) Execution Time', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Execution Time (Seconds, Log Scale)', fontsize=12, fontweight='bold')
ax.grid(True, which='both', linestyle='--', alpha=0.5)

for bar, time in zip(bars, times):
    yval = bar.get_height()
    label = f'{time:.2f} s' if time >= 1 else f'{time:.3f} s'
    ax.text(bar.get_x() + bar.get_width()/2.0, yval * 1.3, label, ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('images/execution_time_chart.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Standalone Speedup Chart
fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.bar(models, speedups, color=colors, width=0.5, edgecolor='black', linewidth=1.2)
ax.set_yscale('log')
ax.set_title('Parallel Speedup vs. Sequential Baseline', fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Speedup Factor (x, Log Scale)', fontsize=12, fontweight='bold')
ax.grid(True, which='both', linestyle='--', alpha=0.5)

for bar, speedup in zip(bars, speedups):
    yval = bar.get_height()
    label = f'{speedup:.2f}x'
    ax.text(bar.get_x() + bar.get_width()/2.0, yval * 1.3, label, ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('images/speedup_chart.png', dpi=300, bbox_inches='tight')
plt.close()

print('Charts regenerated successfully.')
