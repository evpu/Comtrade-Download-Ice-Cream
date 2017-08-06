# ************************************************************************
# Exploratory charts for imports and exports of ice cream.
# https://github.com/evpu
# ************************************************************************

import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

print(os.getcwd())
os.chdir('./data/')  # directory where the data was downloaded

load_files = (pd.read_csv(file, encoding='ISO-8859-1') for file in os.listdir())
data = pd.concat(load_files, ignore_index=True)

os.chdir('..')

# plot style settings
sns.set(style='white')
sns.set_color_codes('pastel')
plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 15

# rescale trade value and net weight by million
data['NetWeight'] = data['NetWeight'] / 1000000
data['TradeValue'] = data['TradeValue'] / 1000000

# ************************************************************************
# Bar charts: Top 20 Importers and Top 20 Exporters in $US
# ************************************************************************

imports = data.loc[data['rgCode'] == 1, ['rtTitle', 'TradeValue']].sort_values(by=['TradeValue']).tail(20)
exports = data.loc[data['rgCode'] == 2, ['rtTitle', 'TradeValue']].sort_values(by=['TradeValue']).tail(20)

# imports
plt.subplot(1, 2, 1)
sns.barplot(x="TradeValue", y="rtTitle", data=imports, color='b')
plt.xlabel('Imports', fontsize=16)
plt.ylabel('')
plt.xlim(0, 500)
plt.gca().invert_xaxis()  # invert x-axis so that it has max on the left and min on the right
plt.box(on=None)  # remove box around the plot

# exports
plt.subplot(1, 2, 2)
sns.barplot(x="TradeValue", y="rtTitle", data=exports, color='r')
plt.xlabel('Exports', fontsize=16)
plt.ylabel('')
plt.xlim(0, 500)
plt.tick_params(axis='y', labelleft='off', labelright='on')  # put country labels on the right
plt.box(on=None)

# title and spacing
plt.suptitle('Top 20 Importers and Top 20 Exporters of Ice Cream (Million $US)', fontsize=18)
plt.tight_layout(rect=[0, 0, 1, 0.95])  # add extra space at the top so that title is not cut off  when saving
plt.subplots_adjust(wspace=0)  # remove space between plots so that bars touch

plt.savefig('ice_cream_bar.png', dpi=400)

plt.show()


# ************************************************************************
# Scatterplot imports vs exports in $US
# ************************************************************************

pivoted = data[['rgCode', 'rtTitle', 'TradeValue', 'NetWeight']].pivot(index='rtTitle', columns='rgCode')

plt.subplots(figsize=(6, 6))
plt.scatter(pivoted['TradeValue'][1], pivoted['TradeValue'][2])
plt.xlim(0, 500)
plt.ylim(0, 500)
plt.plot([0, 500], [0, 500], color='r', linewidth=2.0)
plt.xlabel('Imports (Million $US)', fontsize=16)
plt.ylabel('Exports (Million $US)', fontsize=16)
plt.box(on=None)

# add labels to countries with more than 100 million dollars exports or imports
country = pivoted[(pivoted['TradeValue'][1] >= 100) | (pivoted['TradeValue'][2] >= 100)].index.tolist()
for c in country:
    plt.gca().annotate(c, (pivoted['TradeValue'][1][c], pivoted['TradeValue'][2][c]))

plt.savefig('ice_cream_scatter.png', dpi=400)

plt.show()

# ************************************************************************
# Histogram of price per kilogram
# ************************************************************************
pivoted['Ratio1'] = pivoted['TradeValue'][1] / pivoted['NetWeight'][1]
pivoted['Ratio2'] = pivoted['TradeValue'][2] / pivoted['NetWeight'][2]

plt.hist(pivoted['Ratio1'].dropna(), bins=50, color='b', label='Imports')
# plot second histogram slightly transparent
plt.hist(pivoted['Ratio2'].dropna(), bins=50, color='r', alpha=0.5, label='Exports')
plt.legend(loc='upper right', fontsize=16)
plt.xlabel('Price per Kilogram', fontsize=16)
plt.ylabel('Count', fontsize=16)
plt.box(on=None)

plt.savefig('ice_cream_histogram.png', dpi=400)
plt.show()
