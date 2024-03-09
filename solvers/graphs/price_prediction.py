import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('day.csv')
df_filtered = df[df.index % 3 == 0]
df_filtered.reset_index(drop=True, inplace=True)
df_filtered["date"][0].split(" ")[1][-3]
df_filtered["date"] = df_filtered["date"].apply(lambda x: ' '.join([x.split(" ")[1][:-3], x.split(" ")[2]]))
#df_filtered["date"] = df_filtered["date"].apply(lambda x: x.split(" ")[1])

y_values = [12.13, 10.3, 9.12,  8.73,  8.88,  7.67, 17.24, 25.08, 41.61, 55.74, 56.28, 53.72, 55.36, 51.63, 46.39, 42.72, 41.67, 46.03, 53.16, 47.29, 33.67, 22.71, 18.47, 15.66]
y_values = [value * 8 for value in y_values]

y_values_array = np.repeat(y_values, 4)

result = df_filtered['price'] + y_values_array/20 + 40

plt.plot(df_filtered['date'], result)
plt.axhline(y=100, color='red', linestyle='--')
plt.ylabel('Charging Price')
plt.xlabel('date')
plt.title("Charging Price vs Time")
plt.xticks(df_filtered.index[::4], df_filtered['date'][::4], rotation='vertical')
plt.show()
