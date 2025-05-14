from chameli.config import load_config

load_config("E:\\code\\lightquant\\lightquant\\config\\config_prod.yaml", force_reload=True)
import datetime as dt

from chameli.dateutils import is_business_day, valid_datetime
from chameli.interactions import get_session_or_driver

from nseparser.company_info import (update_board_meetings, update_dividends,
                                    update_split_bonus)
from nseparser.config import load_config as nse_load_config
from nseparser.eod_prices import (save_equity_data, save_future_data,
                                  save_index_data, save_mf_data,
                                  save_option_data)

nse_load_config("E:\\code\\nseparser\\nseparser\\config_prod.yaml", force_reload=True)
driver = get_session_or_driver("https://nseindia.com", get_session=False, webdriver_path="E:\\geckodriver.exe")
update_board_meetings(driver)
update_split_bonus(driver)
update_dividends(driver)
driver.close()
processing_date = "20250506"
processing_date_yday_dt = dt.datetime.strptime(processing_date, "%Y%m%d") - dt.timedelta(days=1)
processing_date_yday = processing_date_yday_dt.strftime("%Y%m%d")
if is_business_day(processing_date):
    session = get_session_or_driver("https://nseindia.com", get_session=True, webdriver_path="E:\\geckodriver.exe")
    save_index_data(processing_date, session)
    save_equity_data(processing_date, session)
    save_future_data(processing_date, session)
    save_option_data(processing_date, session)
save_mf_data(processing_date_yday, session)
session.close()
