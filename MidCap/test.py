import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

numdays = 5
base = datetime.datetime.today()
date_list = [base - datetime.timedelta(hours=x) for x in range(0, numdays*24)]


data = np.random.rand(len(date_list))

fig, ax = plt.subplots(1, 1)
ax.plot(date_list, data)
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_minor_locator(mdates.HourLocator())
fig.autofmt_xdate()

fig.autofmt_xdate()
plt.draw()
plt.show()