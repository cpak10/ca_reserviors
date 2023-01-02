import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

class intake_data_precip:

    def intake(self, reservoirs, lookback):
        # create the file root
        file_root = "C:\\GitHub\\ca_reservoirs"

        # set up the dataset
        columns = [
            "date",
            "name",
            "station_id",
            "agency",
            "elevation_ft",
            "precip_24",
            "percip_mtd",
            "percip_wytd"
        ]
        data_precip = pd.DataFrame(columns = columns)

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
            response = requests.get(f"https://cdec.water.ca.gov/reportapp/javareports?name=DLYPCP.{date}")
            soup = BeautifulSoup(response.content, "html.parser")

            # find all table rows (tr) in the table and iterate
            rows = soup.find_all("tr")
            for row in rows:

                # find all table cells (td) in the row and iterate if tracked
                cells = row.find_all("td")
                if len(cells) > 0:
                    if cells[1].text in reservoirs:
                        data_precip.loc[index_row, "date"] = date
                        for index_column, cell in enumerate(cells):
                            if index_column == 3:
                                if cell.text == "---":
                                    value = 0
                                else:
                                    value = int(cell.text.replace(",", ""))
                                data_precip.loc[index_row, columns[(index_column + 1)]] = value
                            elif index_column > 3:
                                if cell.text == "---":
                                    value = 0.0
                                else:
                                    value = float(cell.text.replace(",", ""))
                                data_precip.loc[index_row, columns[(index_column + 1)]] = value
                            else:
                                data_precip.loc[index_row, columns[(index_column + 1)]] = cell.text
                        index_row += 1

        data_precip.to_csv(f"{file_root}\\working\\precip_levels_{today.strftime('%Y%m%d')}")