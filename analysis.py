import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# Load data
df = pd.read_csv('data/sl_cost_of_living.csv')

# Create output folder
os.makedirs('charts', exist_ok=True)

# Style
sns.set_theme(style='whitegrid')
PALETTE = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b']

# ── CHART 1: Yearly average total cost per region ──────────────────────────
yearly = df.groupby(['Year','Region'])['Monthly_Cost_LKR'].sum().reset_index()
yearly.columns = ['Year','Region','Total_Monthly_Cost']

plt.figure(figsize=(12,6))
for i, region in enumerate(yearly['Region'].unique()):
    data = yearly[yearly['Region']==region]
    plt.plot(data['Year'], data['Total_Monthly_Cost'], marker='o',
             label=region, color=PALETTE[i], linewidth=2.5)

plt.title('Total Monthly Cost of Living by Region (2019–2024)', fontsize=15, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Total Monthly Cost (LKR)', fontsize=12)
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.legend(title='Region')
plt.tight_layout()
plt.savefig('charts/chart1_cost_by_region.png', dpi=150)
plt.close()
print("Chart 1 saved.")

# ── CHART 2: Category-wise cost breakdown (Colombo 2024) ───────────────────
colombo_2024 = df[(df['Region']=='Colombo') & (df['Year']==2024)]
cat_avg = colombo_2024.groupby('Category')['Monthly_Cost_LKR'].mean().sort_values(ascending=False)

plt.figure(figsize=(10,6))
bars = plt.bar(cat_avg.index, cat_avg.values, color=PALETTE)
plt.title('Average Monthly Cost by Category — Colombo 2024', fontsize=15, fontweight='bold')
plt.xlabel('Category', fontsize=12)
plt.ylabel('Average Monthly Cost (LKR)', fontsize=12)
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
for bar, val in zip(bars, cat_avg.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 300,
             f'{val:,.0f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig('charts/chart2_category_breakdown.png', dpi=150)
plt.close()
print("Chart 2 saved.")

# ── CHART 3: Inflation impact — Food cost across all regions ───────────────
food = df[df['Category']=='Food'].groupby(['Year','Region'])['Monthly_Cost_LKR'].mean().reset_index()

plt.figure(figsize=(12,6))
for i, region in enumerate(food['Region'].unique()):
    data = food[food['Region']==region]
    plt.plot(data['Year'], data['Monthly_Cost_LKR'], marker='s',
             label=region, color=PALETTE[i], linewidth=2.5)

plt.axvspan(2021.5, 2022.5, alpha=0.15, color='red', label='2022 Crisis Period')
plt.title('Food Cost Inflation Across Regions (2019–2024)', fontsize=15, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Avg Monthly Food Cost (LKR)', fontsize=12)
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.legend(title='Region')
plt.tight_layout()
plt.savefig('charts/chart3_food_inflation.png', dpi=150)
plt.close()
print("Chart 3 saved.")

# ── CHART 4: Heatmap — avg cost by category and year (Colombo) ────────────
colombo = df[df['Region']=='Colombo']
pivot = colombo.groupby(['Year','Category'])['Monthly_Cost_LKR'].mean().unstack()

plt.figure(figsize=(12,6))
sns.heatmap(pivot, annot=True, fmt=',.0f', cmap='YlOrRd', linewidths=0.5,
            cbar_kws={'label':'Avg Monthly Cost (LKR)'})
plt.title('Cost Heatmap by Category & Year — Colombo', fontsize=15, fontweight='bold')
plt.xlabel('Category', fontsize=12)
plt.ylabel('Year', fontsize=12)
plt.tight_layout()
plt.savefig('charts/chart4_heatmap.png', dpi=150)
plt.close()
print("Chart 4 saved.")

# ── CHART 5: Regional comparison 2019 vs 2024 ─────────────────────────────
compare = df[df['Year'].isin([2019,2024])]
compare = compare.groupby(['Year','Region'])['Monthly_Cost_LKR'].sum().reset_index()
compare.columns = ['Year','Region','Total']

regions = compare['Region'].unique()
x = range(len(regions))
vals_2019 = compare[compare['Year']==2019].set_index('Region').reindex(regions)['Total']
vals_2024 = compare[compare['Year']==2024].set_index('Region').reindex(regions)['Total']

fig, ax = plt.subplots(figsize=(12,6))
width = 0.35
bars1 = ax.bar([i - width/2 for i in x], vals_2019, width, label='2019', color='#1f77b4')
bars2 = ax.bar([i + width/2 for i in x], vals_2024, width, label='2024', color='#d62728')
ax.set_title('Total Monthly Cost: 2019 vs 2024 by Region', fontsize=15, fontweight='bold')
ax.set_xlabel('Region', fontsize=12)
ax.set_ylabel('Total Monthly Cost (LKR)', fontsize=12)
ax.set_xticks(list(x))
ax.set_xticklabels(regions)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
for bar in bars1:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+500,
            f'{bar.get_height():,.0f}', ha='center', va='bottom', fontsize=8)
for bar in bars2:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+500,
            f'{bar.get_height():,.0f}', ha='center', va='bottom', fontsize=8)
ax.legend()
plt.tight_layout()
plt.savefig('charts/chart5_2019_vs_2024.png', dpi=150)
plt.close()
print("Chart 5 saved.")

print("\n✅ All 5 charts saved to the charts folder.")