import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('day.csv')
df_filtered = df[df.index % 3 == 0]
df_filtered.reset_index(drop=True, inplace=True)
df_filtered["date"][0].split(" ")[1][-3]
df_filtered["date"] = df_filtered["date"].apply(lambda x: ' '.join([x.split(" ")[1][:-3], x.split(" ")[2]]))
#df_filtered["date"] = df_filtered["date"].apply(lambda x: x.split(" ")[1])

plt.ylabel('price')
plt.xlabel('date')
plt.title("Price vs Date")
plt.plot(df_filtered['date'], df_filtered['price'])
plt.xticks(df_filtered.index[::4], df_filtered['date'][::4], rotation='vertical')
plt.show()
