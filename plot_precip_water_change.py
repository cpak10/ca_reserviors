import matplotlib.pyplot as plt
import pandas as pd

# filters
reservoir = "ORO"
reservoir_full_name = "Oroville Reservoir Last 90 Days"
date = "20230101"

# file root
file_root = "C:\\GitHub\\ca_reservoirs"

# load the two datasets
data_reservoir = pd.read_csv(f"{file_root}\\working\\reservoir_levels_{date}.csv")
data_precip = pd.read_csv(f"{file_root}\\working\\precip_levels_{date}.csv")

# format dates
data_reservoir["date_f"] = pd.to_datetime(data_reservoir['date'], format = "%Y%m%d")
data_precip["date_f"] = pd.to_datetime(data_precip['date'], format = "%Y%m%d")

# filter the datasets
data_reservoir_filt = data_reservoir[data_reservoir["station_id"] == reservoir]
data_precip_filt = data_precip[data_precip["station_id"] == reservoir]

# plot the line chart
fig, ax1 = plt.subplots()
fig.set_size_inches(18.5, 10.5)
ax2 = ax1.twinx()
ax1.plot(data_reservoir_filt["date_f"], data_reservoir_filt["storage_change"], "-b", label = "Water Change")
ax1.axhline(0, linestyle = "--", color = "r", alpha = .75)

# plot the bar chart
ax2.bar(data_precip_filt["date_f"], data_precip_filt["precip_24"], width = 0.9, alpha = .5, label = "Precipitation")

# add in extra information
ax1.set_ylabel("Water Change (Acre Feet)")
ax2.set_ylabel("Precipitation (Inches)")
ax1.set_title(reservoir_full_name)
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc = 2)

# show the plot
plt.savefig(f"{file_root}\\outputs\\{reservoir_full_name}_{date}.png", dpi = 300)