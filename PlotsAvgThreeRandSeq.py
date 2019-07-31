import numpy as np;
import matplotlib.pyplot as plt;
import pandas as pd;
from sklearn.linear_model import LinearRegression;
from scipy.stats.stats import pearsonr

fig, ax = plt.subplots(1, 2)
# fig.tight_layout()
fig.set_figheight(4.5)
fig.set_figwidth(12)

fig2, ax2 = plt.subplots(1, 2)
# fig2.tight_layout()
fig2.set_figheight(4)
fig2.set_figwidth(8)

# Read in data
withGreen1 = pd.read_csv("data/random/A/with-green.csv")
withoutGreen1 = pd.read_csv("data/random/A/without-green.csv")
invocations1 = pd.read_csv("data/random/A/invocations.csv")
cacheHits1 = pd.read_csv("data/random/A/cacheHits.csv")

withGreen2 = pd.read_csv("data/random/B/with-green.csv")
withoutGreen2 = pd.read_csv("data/random/B/without-green.csv")

withGreen3 = pd.read_csv("data/random/C/with-green.csv")
withoutGreen3 = pd.read_csv("data/random/C/without-green.csv")

withGreen1 = withGreen1.join(invocations1)
withGreen1 = withGreen1.join(cacheHits1)


df1 = pd.merge(withoutGreen1, withGreen1, on=['project', 'package', 'class', 'method'])

df1 = pd.merge(df1, withGreen2, on=['project', 'package', 'class', 'method'])
df1 = pd.merge(df1, withoutGreen2, on=['project', 'package', 'class', 'method'])

df1 = pd.merge(df1, withGreen3, on=['project', 'package', 'class', 'method'])
df1 = pd.merge(df1, withoutGreen3, on=['project', 'package', 'class', 'method'])

df1.rename(columns={'time':'timeA',
                    'time_green':'time_greenA',
                    'time_x':'timeB',
                    'time_green_x':'time_greenB',
                    'time_y':'timeC',
                    'time_green_y':'time_greenC'},
            inplace=True)

df1 = df1[df1['invocations'] > 0]

df1['avgTime'] = df1[['timeA', 'timeB', 'timeC']].mean(axis=1)
df1['avgTime_green'] = df1[['time_greenA', 'time_greenB', 'time_greenC']].mean(axis=1)

# print(df1)

df1.reset_index(inplace=True)
df1 = df1.drop(['index', 'timeA', 'timeB', 'timeC', 'time_greenA', 'time_greenB', 'time_greenC'], axis=1)

print(df1.groupby('class')['method'].nunique().size)
#
# Calculate time ratio
df1['Ts'] = pd.to_numeric(df1['avgTime_green'])/pd.to_numeric(df1['avgTime'])
# print('size of sequence 1 ', df1['Ts'] .size)

x = pd.DataFrame(np.arange(0.0, df1['Ts'].size, 1))

linear_regressor = LinearRegression()
linear_regressor.fit(x, df1['Ts'].values)
Y_pred = linear_regressor.predict(x)

ax[0].plot(df1.index, df1['Ts'], drawstyle="steps-pre", linewidth=0.75)
ax[0].set_ylabel('Ts')
ax[0].set_xlabel('Program #')
ax[0].set_ylim([0, 1.2])
# ax[0].plot(x, Y_pred, color='red')


df1['Rs'] = pd.to_numeric(df1['cacheHits'])/pd.to_numeric(df1['invocations'])

ax[1].plot(df1.index, df1['Rs'], drawstyle="steps-pre", linewidth=0.75)
ax[1].set_ylabel('Rs')
ax[1].set_xlabel('Program #')
# ax[1].title.set_text('S1')

ax2[0].boxplot(df1['Ts'])
ax2[0].set_ylabel('Ts')
ax2[0].set_ylim([0, 1.2])

ax2[1].boxplot(df1['Rs'])
ax2[1].set_ylabel('Rs')

print('pearson coefficient and p value:', pearsonr(df1['Ts'], df1['Rs']))
plt.show()

fig.savefig('plots/random/all/TsRs.png')
fig2.savefig('plots/random/all/TsRsBoxplot.png')

