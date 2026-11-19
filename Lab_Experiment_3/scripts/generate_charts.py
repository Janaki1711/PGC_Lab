import os
import matplotlib.pyplot as plt
import numpy as np

os.makedirs('graphs', exist_ok=True)
os.makedirs('images', exist_ok=True)

# Typography & theme settings
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Segoe UI', 'Arial']

# Benchmark Data (10,000,000 increments)
threads = [1, 2, 4, 8]
mechanisms = ['None (Race)', 'Atomic', 'Critical', 'Lock (Mutex)']

# Times in seconds
times = {
    'None (Race)': [0.0098, 0.0628, 0.0871, 0.1044],
    'Atomic':      [0.0262, 0.1178, 0.1362, 0.1867],
    'Critical':    [0.0715, 0.3884, 0.8596, 1.4656],
    'Lock (Mutex)': [0.0774, 0.5356, 1.2421, 2.4512]
}

# Lost updates percentage for None (Race)
lost_pct = [0.0, (1 - 4757077/10000000)*100, (1 - 2407346/10000000)*100, (1 - 1524653/10000000)*100]

# Muted, professional engineering palette
colors = {
    'None (Race)': '#64748B',  # Slate Gray
    'Atomic':      '#387864',  # Muted Teal / Sage
    'Critical':    '#B85D43',  # Muted Terracotta
    'Lock (Mutex)': '#2B5C8F'  # Deep Slate Blue
}

# ==============================================================================
# 1. Compact 2x2 Performance Dashboard
# ==============================================================================
fig, axes = plt.subplots(2, 2, figsize=(9.5, 7.2), facecolor='#FAFBFC')

# Subplot 1: Execution Time vs Thread Count (Log Scale)
ax1 = axes[0, 0]
for name in mechanisms:
    ax1.plot(threads, times[name], marker='o', linewidth=1.8, markersize=5,
             label=name, color=colors[name])
ax1.set_yscale('log')
ax1.set_title('Execution Time (Log Scale)', fontsize=10.5, fontweight='bold', color='#1E293B', pad=8)
ax1.set_xlabel('Threads (P)', fontsize=9, color='#475569')
ax1.set_ylabel('Seconds (Lower is Better)', fontsize=9, color='#475569')
ax1.set_xticks(threads)
ax1.grid(True, which='both', linestyle=':', color='#E2E8F0', alpha=0.8)
ax1.set_facecolor('#FFFFFF')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=7.5)

# Subplot 2: Grouped Bar Chart of Execution Times
ax2 = axes[0, 1]
x = np.arange(len(threads))
bar_width = 0.2
for i, name in enumerate(mechanisms):
    offset = (i - 1.5) * bar_width
    ax2.bar(x + offset, times[name], bar_width, label=name,
            color=colors[name], edgecolor='#334155', linewidth=0.8)
ax2.set_yscale('log')
ax2.set_title('Mechanism Comparison (Log Scale)', fontsize=10.5, fontweight='bold', color='#1E293B', pad=8)
ax2.set_xlabel('Threads (P)', fontsize=9, color='#475569')
ax2.set_ylabel('Seconds', fontsize=9, color='#475569')
ax2.set_xticks(x)
ax2.set_xticklabels([f'{t}T' for t in threads])
ax2.grid(True, which='both', linestyle=':', color='#E2E8F0', alpha=0.8)
ax2.set_facecolor('#FFFFFF')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=7.5)

# Subplot 3: Effective Throughput (Million Operations per Second)
ax3 = axes[1, 0]
for name in mechanisms:
    throughput = [10.0 / t for t in times[name]]
    ax3.plot(threads, throughput, marker='s', linewidth=1.8, markersize=5,
             label=name, color=colors[name])
ax3.set_yscale('log')
ax3.set_title('Throughput (Mops/s, Higher is Better)', fontsize=10.5, fontweight='bold', color='#1E293B', pad=8)
ax3.set_xlabel('Threads (P)', fontsize=9, color='#475569')
ax3.set_ylabel('Mops/sec', fontsize=9, color='#475569')
ax3.set_xticks(threads)
ax3.grid(True, which='both', linestyle=':', color='#E2E8F0', alpha=0.8)
ax3.set_facecolor('#FFFFFF')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=7.5)

# Subplot 4: Data Race Counter Loss
ax4 = axes[1, 1]
bars_loss = ax4.bar([f'{t}T' for t in threads], lost_pct, color='#B85D43', width=0.45,
                    edgecolor='#334155', linewidth=0.8)
ax4.set_title('Unsynchronized Data Loss (%)', fontsize=10.5, fontweight='bold', color='#1E293B', pad=8)
ax4.set_xlabel('Threads (P)', fontsize=9, color='#475569')
ax4.set_ylabel('% Lost (Zero is Ideal)', fontsize=9, color='#475569')
ax4.set_ylim(0, 100)
ax4.grid(True, which='both', linestyle=':', color='#E2E8F0', alpha=0.8)
ax4.set_facecolor('#FFFFFF')
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

for bar, pct in zip(bars_loss, lost_pct):
    yval = bar.get_height()
    label = f'{pct:.1f}%' if pct > 0 else '0%'
    ax4.text(bar.get_x() + bar.get_width()/2.0, yval + 2, label,
             ha='center', va='bottom', fontsize=8, color='#1E293B')

plt.suptitle('Experiment 3: Synchronization Performance Dashboard',
             fontsize=12, fontweight='bold', color='#1E293B', y=0.99)
plt.tight_layout()
plt.savefig('graphs/performance_comparison_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()

# ==============================================================================
# 2. Standalone Scalability & Overhead Multiplier Chart
# ==============================================================================
fig, ax = plt.subplots(figsize=(6.5, 3.8), facecolor='#FAFBFC')

for name in ['Atomic', 'Critical', 'Lock (Mutex)']:
    overhead = [times[name][i] / times[name][0] for i in range(len(threads))]
    ax.plot(threads, overhead, marker='o', linewidth=2, markersize=6,
            label=f'{name}', color=colors[name])

ax.set_title('Contention Overhead Multiplier (T_P / T_1)', fontsize=11, fontweight='bold', color='#1E293B', pad=10)
ax.set_xlabel('Threads (P)', fontsize=9.5, color='#475569')
ax.set_ylabel('Overhead Multiplier', fontsize=9.5, color='#475569')
ax.set_xticks(threads)
ax.grid(True, which='both', linestyle=':', color='#E2E8F0', alpha=0.8)
ax.set_facecolor('#FFFFFF')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=8.5)

plt.tight_layout()
plt.savefig('graphs/contention_overhead_analysis.png', dpi=150, bbox_inches='tight')
plt.close()

print('Experiment 3 charts regenerated with compact sizing and muted palette.')
