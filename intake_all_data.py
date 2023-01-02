import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from intake_data_precip import intake_data_precip
from intake_data_reservoir import intake_data_reservoir

# reservoirs to track
reservoirs = ["ORO", "SHA"]
lookback = 90

# initiate the classes
intake_precip = intake_data_precip()
intake_reservoir = intake_data_reservoir()

# call the modules to intake data
print("\nNOTE: Scraping precipitation data")
intake_precip.intake(reservoirs = reservoirs, lookback = lookback)
print("\nNOTE: Scraping reservoir data")
intake_reservoir.intake(reservoirs = reservoirs, lookback = lookback)