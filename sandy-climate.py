import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime


# load data
sandy_df = pd.read_csv("sandy.csv")
sandy_df.head()
sandy_df.describe()


# sort in ascending order of date
sandy_df = sandy_df.sort(columns="Date")
sandy_df.head()


# compute record high and record low temp over all stations by date
smax = sandy_df[sandy_df["Element"]=="TMAX"]
smin = sandy_df[sandy_df["Element"]=="TMIN"]

smax = smax.groupby('Date')["Data_Value"].agg({"Data_Value":np.max})
smin = smin.groupby('Date')["Data_Value"].agg({"Data_Value":np.min})


# merge dataframe savgmax and savgmin on date
s = pd.merge(smax, smin, how='outer', left_index=True, right_index=True)
s.head()
s.describe()


# rename columns "TMAX", "TMIN", add column "Date", reset index
s = s.rename(index=str, columns={"Data_Value_x": "TMAX", "Data_Value_y": "TMIN"})
s["Date"] = s.index
s = s.reset_index()
s.head()


# convert "Date" string to date type
s["Date"] = pd.to_datetime(s["Date"])
s["Date"].head()


# check if all entries TMAX > TMIN
all(s["TMAX"]-s["TMIN"]>0)


# plot data 
x = s["Date"]
y1 = s["TMIN"]
y2 = s["TMAX"]
width = 9
height = 6
plt.figure(figsize=(width, height))
plt.plot(x, y1, 'b-', label="Minimum Temperature", linewidth=0.2)
plt.plot(x, y2, 'r-', label="Maximum Temperature", linewidth=0.2)

plt.title('Daily Temperature Records in Sandy, Utah, United States')
plt.xlabel('Date')
plt.ylabel('Temperature (F)')
plt.legend(loc=4)

# fill the area between TMAX and TMIN
# plt.fill_between(range(len(x)),y1,y2, facecolor='blue', alpha=0.25)
plt.show()
plt.savefig("graph.svg")