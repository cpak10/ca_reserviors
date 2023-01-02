import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

class intake_data_reservoir:

    def intake(self, reservoirs, lookback):
        # create the file root
        file_root = "C:\\GitHub\\ca_reserviors"

        # set up the dataset
        columns = [
            "date",
            "name",
            "station_id",
            "capacity_af",
            "elevation_ft",
            "storage_af",
            "storage_change",
            "percent_capacity",
            "average_storage",
            "percent_avg_storage",
            "outflow_cfs",
            "inflow_cfs",
            "storage_yb4"
        ]
        data_reservoirs = pd.DataFrame(columns = columns)

        # track the row being appended
        index_row = 0

        # create the dates to iterate
        today = datetime.today()
        dates = []

        # iterate through the past x days
        for i in range(lookback):

            date = today - timedelta(days = (i + 1))
            date_str = date.strftime("%Y%m%d")
            dates.append(date_str)

        # iterate through the days
        for date in dates:

            # make a request and parse HTML
            response = requests.get(f"https://cdec.water.ca.gov/reportapp/javareports?name=RES.{date}")
            soup = BeautifulSoup(response.content, "html.parser")

            # find all table rows (tr) in the table and iterate
            rows = soup.find_all("tr")
            for row in rows:

                # find all table cells (td) in the row and iterate if tracked
                cells = row.find_all("td")
                if len(cells) > 0:
                    if cells[1].text in reservoirs:
                        data_reservoirs.loc[index_row, "date"] = date
                        for index_column, cell in enumerate(cells):
                            if index_column == 3:
                                if cell.text == "---":
                                    value = 0.0
                                else:
                                    value = float(cell.text.replace(",", ""))
                                data_reservoirs.loc[index_row, columns[(index_column + 1)]] = value
                            elif index_column >= 2:
                                if cell.text == "---":
                                    value = 0
                                else:
                                    value = int(cell.text.replace(",", ""))
                                data_reservoirs.loc[index_row, columns[(index_column + 1)]] = value
                            else:
                                data_reservoirs.loc[index_row, columns[(index_column + 1)]] = cell.text
                        index_row += 1

        data_reservoirs.to_csv(f"{file_root}\\working\\reservoir_levels_{today.strftime('%Y%m%d')}")