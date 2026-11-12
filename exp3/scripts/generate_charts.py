import os
import matplotlib.pyplot as plt
import numpy as np

# Ensure target directories exist
os.makedirs('graphs', exist_ok=True)
os.makedirs('images', exist_ok=True)

# Custom typography & theme settings matching PGC Lab standard
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

# Palette & styling matching Experiment 1 signature style
colors = {
    'None (Race)': '#6C5CE7',
    'Atomic':      '#00B894',
    'Critical':    '#FD79A8',
    'Lock (Mutex)': '#0984E3'
}
hatches = {
    'None (Race)': '///',
    'Atomic':      '***',
    'Critical':    '\\\\\\',
    'Lock (Mutex)': '...'
}

# ==============================================================================
# 1. Comprehensive 2x2 Performance Dashboard
# ==============================================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 12), facecolor='#FAFAFA')

# Subplot 1: Execution Time vs Thread Count (Log Scale)
ax1 = axes[0, 0]
for name in mechanisms:
    ax1.plot(threads, times[name], marker='o', linewidth=2.5, markersize=8,
             label=name, color=colors[name])
ax1.set_yscale('log')
ax1.set_title('Execution Time vs. Thread Count (Log Scale)', fontsize=13, fontweight='bold', color='#2D3436', pad=12)
ax1.set_xlabel('Thread Count (P)', fontsize=11, fontweight='bold', color='#636E72')
ax1.set_ylabel('Execution Time in Seconds (Lower is Better)', fontsize=11, fontweight='bold', color='#636E72')
ax1.set_xticks(threads)
ax1.grid(True, which='both', linestyle=':', color='#DFE6E9', alpha=0.8)
ax1.set_facecolor('#FFFFFF')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(frameon=True, facecolor='#F1F2F6', edgecolor='#B2BEC3')

# Subplot 2: Grouped Bar Chart of Execution Times
ax2 = axes[0, 1]
x = np.arange(len(threads))
bar_width = 0.2
for i, name in enumerate(mechanisms):
    offset = (i - 1.5) * bar_width
    bars = ax2.bar(x + offset, times[name], bar_width, label=name,
                   color=colors[name], edgecolor='#2D3436', linewidth=1.2,
                   hatch=hatches[name])
ax2.set_yscale('log')
ax2.set_title('Mechanism Comparison Across Thread Counts', fontsize=13, fontweight='bold', color='#2D3436', pad=12)
ax2.set_xlabel('Thread Count (P)', fontsize=11, fontweight='bold', color='#636E72')
ax2.set_ylabel('Execution Time (s, Log Scale)', fontsize=11, fontweight='bold', color='#636E72')
ax2.set_xticks(x)
ax2.set_xticklabels([f'{t} Threads' for t in threads])
ax2.grid(True, which='both', linestyle=':', color='#DFE6E9', alpha=0.8)
ax2.set_facecolor('#FFFFFF')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(frameon=True, facecolor='#F1F2F6', edgecolor='#B2BEC3')

# Subplot 3: Effective Throughput (Million Operations per Second)
ax3 = axes[1, 0]
for name in mechanisms:
    throughput = [10.0 / t for t in times[name]]
    ax3.plot(threads, throughput, marker='s', linewidth=2.5, markersize=8,
             label=name, color=colors[name])
ax3.set_yscale('log')
ax3.set_title('Effective Synchronization Throughput (Mops/s)', fontsize=13, fontweight='bold', color='#2D3436', pad=12)
ax3.set_xlabel('Thread Count (P)', fontsize=11, fontweight='bold', color='#636E72')
ax3.set_ylabel('Throughput (Mops/sec, Higher is Better)', fontsize=11, fontweight='bold', color='#636E72')
ax3.set_xticks(threads)
ax3.grid(True, which='both', linestyle=':', color='#DFE6E9', alpha=0.8)
ax3.set_facecolor('#FFFFFF')
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.legend(frameon=True, facecolor='#F1F2F6', edgecolor='#B2BEC3')

# Subplot 4: Data Race Counter Loss & Synchronization Overhead
ax4 = axes[1, 1]
bars_loss = ax4.bar([f'{t}T' for t in threads], lost_pct, color='#E17055', width=0.48,
                    edgecolor='#2D3436', linewidth=1.2, hatch='xx')
ax4.set_title('Data Race Integrity Failure: Lost Updates in Unsynchronized Runs', fontsize=13, fontweight='bold', color='#2D3436', pad=12)
ax4.set_xlabel('Thread Count (P)', fontsize=11, fontweight='bold', color='#636E72')
ax4.set_ylabel('% of 10M Increments Lost (Zero is Ideal)', fontsize=11, fontweight='bold', color='#636E72')
ax4.set_ylim(0, 100)
ax4.grid(True, which='both', linestyle=':', color='#DFE6E9', alpha=0.8)
ax4.set_facecolor('#FFFFFF')
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

for bar, pct in zip(bars_loss, lost_pct):
    yval = bar.get_height()
    label = f'{pct:.1f}%' if pct > 0 else '0% (Single Core)'
    ax4.text(bar.get_x() + bar.get_width()/2.0, yval + 2.5, label,
             ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#2D3436',
             bbox=dict(boxstyle='round,pad=0.25', fc='#F1F2F6', ec='#B2BEC3', lw=1))

plt.suptitle('Parallel & GPU Computing Lab — Experiment 3: OpenMP Synchronization Benchmark',
             fontsize=16, fontweight='bold', color='#2D3436', y=0.995)
plt.tight_layout()
plt.savefig('graphs/performance_comparison_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

# ==============================================================================
# 2. Standalone Scalability & Overhead Multiplier Chart
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 6), facecolor='#FAFAFA')

for name in ['Atomic', 'Critical', 'Lock (Mutex)']:
    overhead = [times[name][i] / times[name][0] for i in range(len(threads))]
    ax.plot(threads, overhead, marker='o', linewidth=2.8, markersize=8,
            label=f'{name} (Contention Factor)', color=colors[name])

ax.set_title('Contention Penalty: Execution Time Multiplier Relative to 1 Thread', fontsize=14, fontweight='bold', color='#2D3436', pad=15)
ax.set_xlabel('Thread Count (P)', fontsize=12, fontweight='bold', color='#636E72')
ax.set_ylabel('Overhead Multiplier (T_P / T_1, Lower is Better)', fontsize=12, fontweight='bold', color='#636E72')
ax.set_xticks(threads)
ax.grid(True, which='both', linestyle=':', color='#DFE6E9', alpha=0.8)
ax.set_facecolor('#FFFFFF')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(frameon=True, facecolor='#F1F2F6', edgecolor='#B2BEC3', fontsize=11)

# Annotate points at 8 threads
ax.annotate(f'Lock: 31.67x penalty\n(2.45s vs 0.077s)', xy=(8, times['Lock (Mutex)'][3]/times['Lock (Mutex)'][0]),
            xytext=(6.5, 27), arrowprops=dict(facecolor='#0984E3', shrink=0.08, width=1.5, headwidth=6),
            fontweight='bold', fontsize=10, bbox=dict(boxstyle='round,pad=0.3', fc='#F1F2F6', ec='#B2BEC3'))

ax.annotate(f'Atomic: 7.13x penalty\n(0.187s vs 0.026s)', xy=(8, times['Atomic'][3]/times['Atomic'][0]),
            xytext=(6.2, 10), arrowprops=dict(facecolor='#00B894', shrink=0.08, width=1.5, headwidth=6),
            fontweight='bold', fontsize=10, bbox=dict(boxstyle='round,pad=0.3', fc='#F1F2F6', ec='#B2BEC3'))

plt.tight_layout()
plt.savefig('graphs/contention_overhead_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print('Experiment 3 performance charts generated successfully with custom theme and high-DPI export.')
