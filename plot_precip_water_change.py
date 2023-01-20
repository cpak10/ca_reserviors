import matplotlib.pyplot as plt
import pandas as pd

# filters
reservoir = input("INPUT - Enter reservoir code (e.g. SHA): ")
reservoir_spelled = input("INPUT - Enter reservoir name (e.g. Shasta): ")
number_days_lookback = int(input("INPUT - Enter number of days lookback: "))
reservoir_full_name = f"{reservoir_spelled} Reservoir Last {number_days_lookback} Days"
date = input("INPUT - Enter date of data pull (e.g. 20230119): ")
reservoir_column = input("INPUT - Enter variable name for y-axis (e.g. storage_af): ")
reservoir_column_lab = input("INPUT - Enter name for y-axis (e.g. Storage): ")
reservoir_y_lab = input("INPUT - Enter name for y-axis label (e.g. Storage (Million Acre Feet)): ")
sw_replace_zero = int(input("INPUT - Enter '1' to replace missing zeros in reservoir data, else '0': "))
sw_zero_line = int(input("INPUT - Enter '1' to add a zero line to plot, else '0': "))
sw_historic_line = int(input("INPUT - Enter '1' to add a historic line to plot, else '0': "))
sw_total_capacity = int(input("INPUT - Enter '1' to add a total capacity line to plot, else '0': "))

# file root
file_root = "C:\\GitHub\\ca_reservoirs"

# load the two datasets
data_reservoir = pd.read_csv(f"{file_root}\\working\\reservoir_levels_{date}.csv")
data_precip = pd.read_csv(f"{file_root}\\working\\precip_levels_{date}.csv")

# format dates
data_reservoir["date_f"] = pd.to_datetime(data_reservoir['date'], format = "%Y%m%d")
data_precip["date_f"] = pd.to_datetime(data_precip['date'], format = "%Y%m%d")

# filter the datasets
data_reservoir_filt = data_reservoir[data_reservoir["station_id"] == reservoir].reset_index(drop = True)
data_precip_filt = data_precip[data_precip["station_id"] == reservoir]

# replace zeros
if sw_replace_zero == 1:
    indices_zeros = data_reservoir_filt[data_reservoir_filt[reservoir_column] == 0].index
    for i in indices_zeros:
        data_reservoir_filt.loc[i, reservoir_column] = data_reservoir_filt.loc[i + 1, reservoir_column]

# plot the line chart
fig, ax1 = plt.subplots()
fig.set_size_inches(18.5, 10.5)
ax2 = ax1.twinx()
ax1.plot(data_reservoir_filt["date_f"], data_reservoir_filt[reservoir_column], "-b", label = reservoir_column_lab)
if sw_zero_line == 1:
    ax1.axhline(0, linestyle = "--", color = "r", alpha = .75)
if sw_total_capacity == 1:
    ax1.axhline(data_reservoir_filt.loc[0, "capacity_af"], linestyle = "--", color = "g", alpha = .75, label = "Total Capacity")
if sw_historic_line == 1:
    ax1.axhline(data_reservoir_filt.loc[0, "average_storage"], linestyle = "--", color = "b", alpha = .75, label = "Historic Level")
ax1.set_ylim(bottom = 0)

# plot the bar chart
ax2.bar(data_precip_filt["date_f"], data_precip_filt["precip_24"], width = 0.9, alpha = .5, label = "Precipitation")

# add in extra information
ax1.set_ylabel(reservoir_y_lab)
ax2.set_ylabel("Precipitation (Inches)")
ax1.set_title(reservoir_full_name)
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc = 2)

# show the plot
plt.savefig(f"{file_root}\\outputs\\{reservoir_full_name}_{date}.png", dpi = 300)