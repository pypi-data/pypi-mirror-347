import datetime as dt
import logging
import os
import traceback

import numpy as np
import pandas as pd
from chameli.dateutils import valid_datetime
from chameli.interactions import (file_exists_and_valid, list_directory,
                                  make_directory, read_csv_from_zip,
                                  read_csv_in_pandas_out, readRDS, save_file,
                                  saveRDS, send_mail)
from ohlcutils.data import _split_adjust_market_data, get_linked_symbols
from ohlcutils.enums import Periodicity

from .config import get_config

logger = logging.getLogger(__name__)


def get_dynamic_config():
    return get_config()


def catch(func, *args, handle=lambda e: e, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return handle(e)


def check_float(potential_float):
    try:
        return float(potential_float)
    except ValueError:
        return potential_float


def get_first_day_of_the_quarter(p_date: dt.date):
    currQuarter = (p_date.month - 1) // 3 + 1
    return dt.datetime(p_date.year, 3 * currQuarter - 2, 1)


def save_equity_data(p: str, session, save_to_rds=True):
    """Save Equity Data to Folder

    Args:
        p (str): processing date as YYYYMMDD
        session: HTTP session for making requests
    """

    def update_symbol(filename_to_update, filename_to_save, row):
        try:
            md = readRDS(filename_to_update)
            md["date"] = md["date"].dt.tz_localize("UTC")
            md["date"] = md["date"].dt.tz_convert("Asia/Kolkata")
        except Exception as e:
            logger.warning(f"Failed to read RDS file {filename_to_update}: {e}")
            md = pd.DataFrame()
        md_updated = pd.concat([md, row], ignore_index=True)
        md_updated = md_updated.drop_duplicates(subset="date", keep="last")
        md_updated = md_updated.sort_values(by="date")
        md_updated.symbol = md_updated.symbol.iloc[0]
        if "splitadjust" in md_updated.columns:
            md_updated.drop("splitadjust", axis=1, inplace=True)
        if "tradecount" in md_updated.columns:
            md_updated["tradecount"].fillna(-1, inplace=True)
            md_updated["tradecount"] = md_updated["tradecount"].astype(int)
        md_updated.set_index("date", inplace=True)
        md_updated = _split_adjust_market_data(md_updated, src=Periodicity.DAILY, tz="Asia/Kolkata")
        md_updated.reset_index(inplace=True)
        saveRDS(md_updated, filename_to_save)

    try:
        outfolder = f"{get_dynamic_config().get('daily_prices')}/stk"
        url = f"https://archives.nseindia.com/products/content/sec_bhavdata_full_{valid_datetime(p,'%d%m%Y')[0]}.csv"
        dest_file = f"{get_dynamic_config().get('bhavcopy_folder')}/{p}_equity.csv"

        # Check if destination file exists
        if file_exists_and_valid(dest_file, min_size=1000):
            logger.info(f"File already exists: {dest_file}")
            if not save_to_rds:
                return
            data = read_csv_in_pandas_out(dest_file, dtype=str)
        else:
            # Downloading the file
            response = session.get(url)
            if response.status_code == 200:
                save_file(dest_file, response.content)
                logger.info(f"Equity bhavcopy downloaded and saved successfully for {p}")
                if not save_to_rds:
                    return
                data = read_csv_in_pandas_out(dest_file, dtype=str)
            else:
                logger.error(f"Failed to download equity file for {p}. Status code: {response.status_code}")
                send_mail(
                    get_dynamic_config().get("from_email_id"),
                    get_dynamic_config().get("to_email_id"),
                    get_dynamic_config().get("from_email_password"),
                    f"Unable to download equity file for {p}",
                    f"HTTP Status Code: {response.status_code}",
                )
                return

        if file_exists_and_valid(dest_file, min_size=1000):
            # Reading the CSV file
            data.columns = [col.strip() for col in data.columns]
            data = data.map(lambda x: x.strip() if isinstance(x, str) else x)
            data = data[data["SERIES"].isin(["EQ", "BZ", "BE", "IV", "RR"])]

            # Converting 'DATE1' to datetime and adjusting timezone
            data.loc[:, "TIMESTAMP"] = pd.to_datetime(data["DATE1"], format="%d-%b-%Y")
            data.loc[:, "TIMESTAMP"] = data["TIMESTAMP"].dt.tz_localize("Asia/Kolkata")

            # Renaming 'NO_OF_TRADES' to 'TOTALTRADES'
            data.loc[:, "TOTALTRADES"] = data["NO_OF_TRADES"]

            # Trimming whitespace and converting 'DELIV_QTY' to numeric, replacing NaNs with 0
            data.loc[:, "DELIV_QTY"] = data["DELIV_QTY"].str.strip()
            data.loc[:, "DELIV_QTY"] = pd.to_numeric(data["DELIV_QTY"], errors="coerce").fillna(0)
            data.loc[:, "TURNOVER_LACS"] = pd.to_numeric(data["TURNOVER_LACS"], errors="coerce").fillna(0)

            # Converting specific columns to numeric
            numeric_columns = [
                "OPEN_PRICE",
                "HIGH_PRICE",
                "LOW_PRICE",
                "LAST_PRICE",
                "CLOSE_PRICE",
                "TTL_TRD_QNTY",
                "NO_OF_TRADES",
                "DELIV_QTY",
                "TURNOVER_LACS",
            ]
            for col in numeric_columns:
                data[col] = pd.to_numeric(data[col], errors="coerce")

            # Process each row in the data
            for i in range(len(data)):
                d = data.iloc[i]
                symbol = f"{d['SYMBOL']}_STK___"
                logger.info(f"Processing Daily Bars for {symbol}")
                df = pd.DataFrame(
                    {
                        "date": pd.to_datetime(d["TIMESTAMP"]),
                        "open": d["OPEN_PRICE"],
                        "high": d["HIGH_PRICE"],
                        "low": d["LOW_PRICE"],
                        "close": d["LAST_PRICE"],
                        "settle": d["CLOSE_PRICE"],
                        "volume": d["TTL_TRD_QNTY"],
                        "tradecount": d["NO_OF_TRADES"],
                        "delivered": d["DELIV_QTY"],
                        "tradedvalue": d["TURNOVER_LACS"] * 100000,
                        "symbol": symbol,
                    },
                    index=[0],
                )
                filename = os.path.join(outfolder, f"{symbol}.rds")
                if file_exists_and_valid(filename, min_size=1):
                    update_symbol(filename, filename, df)
                    potential_link = get_linked_symbols(df.symbol.item())
                    if len(potential_link) > 1:
                        current_link_index = np.where(d.symbol == potential_link.symbol)[0][0]
                        if current_link_index > 0:  # we have name change[s]. merge current data into new name[s]
                            potential_link = potential_link[0:current_link_index]
                            for new_symbol in potential_link.symbol:
                                new_symbol = f"{outfolder}/{new_symbol}_STK___.rds"
                                update_symbol(new_symbol, new_symbol, df)
                else:
                    potential_link = get_linked_symbols(df.symbol.item())
                    if len(potential_link) > 1:
                        current_link_index = np.where(d.symbol == potential_link.symbol)[0][0]
                        for new_symbol in potential_link.symbol[current_link_index:][::-1]:
                            new_symbol = f"{outfolder}/{new_symbol}_STK___.rds"
                            filename_to_save = f"{outfolder}/{df.symbol[0]}.rds"
                            update_symbol(new_symbol, filename_to_save, df)
                    else:
                        filename_to_save = f"{outfolder}/{df.symbol[0]}.rds"
                        update_symbol(filename_to_save, filename_to_save, df)
    except Exception as e:
        logger.error(f"Error in save_equity_data: {e}")
        send_mail(
            get_dynamic_config().get("from_email_id"),
            get_dynamic_config().get("to_email_id"),
            get_dynamic_config().get("from_email_password"),
            f"Unable to process equity data for {p}",
            f"{traceback.format_exc()}",
        )


def save_index_data(p: str, session, save_to_rds=True):
    """Save Index Data to Folder

    Args:
        p (str): processing date as YYYYMMDD
        session: HTTP session for making requests
    """

    def update_symbol(filename_to_update, filename_to_save, row):
        """Update the RDS file with new data."""
        try:
            md = readRDS(filename_to_update)
            md["date"] = md["date"].dt.tz_localize("UTC")
            md["date"] = md["date"].dt.tz_convert("Asia/Kolkata")
        except Exception as e:
            logger.warning(f"Failed to read RDS file {filename_to_update}: {e}")
            md = pd.DataFrame()
        md_updated = pd.concat([md, row], ignore_index=True)
        md_updated = md_updated.drop_duplicates(subset="date", keep="last")
        md_updated = md_updated.sort_values(by="date")
        md_updated.symbol = md_updated.symbol.iloc[0]
        saveRDS(md_updated, filename_to_save)

    try:
        outfolder = f"{get_dynamic_config().get('daily_prices')}/ind"
        url = f"https://archives.nseindia.com/content/indices/ind_close_all_{valid_datetime(p,'%d%m%Y')[0]}.csv"
        dest_file = f"{get_dynamic_config().get('bhavcopy_folder')}/{p}_index.csv"

        # Check if destination file exists
        if file_exists_and_valid(dest_file, min_size=1000):
            logger.info(f"File already exists: {dest_file}")
            if not save_to_rds:
                return
            data = read_csv_in_pandas_out(dest_file, dtype=str)
        else:
            # Downloading the file
            response = session.get(url)
            if response.status_code == 200:
                save_file(dest_file, response.content)
                logger.info(f"Index bhavcopy downloaded and saved successfully for {p}")
                if not save_to_rds:
                    return
                data = read_csv_in_pandas_out(dest_file, dtype=str)
            else:
                logger.error(f"Failed to download index file for {p}. Status code: {response.status_code}")
                send_mail(
                    get_dynamic_config().get("from_email_id"),
                    get_dynamic_config().get("to_email_id"),
                    get_dynamic_config().get("from_email_password"),
                    f"Unable to download index file for {p}",
                    f"HTTP Status Code: {response.status_code}",
                )
                return

        if file_exists_and_valid(dest_file, min_size=1000):
            # Reading the CSV file
            data.columns = [col.strip() for col in data.columns]
            data = data.map(lambda x: x.strip() if isinstance(x, str) else x)

            # Converting 'Index Date' to datetime and setting timezone
            data["TIMESTAMP"] = pd.to_datetime(data["Index Date"], format="%d-%m-%Y")
            data["TIMESTAMP"] = data["TIMESTAMP"].dt.tz_localize("Asia/Kolkata")

            # Cleaning and transforming 'Index Name'
            data["SYMBOL"] = data["Index Name"].str.replace(" ", "", regex=False).str.upper()

            # Replacing specific patterns in 'SYMBOL'
            replacements = {
                r"^NIFTY50$": "NSENIFTY",
                r"^CNXNIFTY$": "NSENIFTY",
                r"^NIFTYBANK$": "BANKNIFTY",
                r"^CNXBANK$": "BANKNIFTY",
                r"^NIFTYFINANCIALSERVICES$": "FINNIFTY",
            }
            for pattern, replacement in replacements.items():
                data.loc[data["SYMBOL"].str.match(pattern), "SYMBOL"] = replacement

            # Removing slashes and appending "_IND___"
            data["SYMBOL"] = data["SYMBOL"].str.replace("/", "", regex=False) + "_IND___"

            # Converting specific columns to numeric
            numeric_columns = [
                "Open Index Value",
                "High Index Value",
                "Low Index Value",
                "Closing Index Value",
                "Volume",
                "P/E",
                "P/B",
                "Div Yield",
                "Turnover (Rs. Cr.)",
            ]
            for col in numeric_columns:
                data[col] = pd.to_numeric(data[col], errors="coerce")

            # Process each row in the data
            for i in range(len(data)):
                d = data.iloc[i]
                df = pd.DataFrame(
                    {
                        "date": [d["TIMESTAMP"]],
                        "open": [d["Open Index Value"]],
                        "high": [d["High Index Value"]],
                        "low": [d["Low Index Value"]],
                        "close": [d["Closing Index Value"]],
                        "settle": [d["Closing Index Value"]],
                        "volume": [d["Volume"]],
                        "tradedvalue": [d["Turnover (Rs. Cr.)"]],
                        "pe": [d["P/E"]],
                        "pb": [d["P/B"]],
                        "dividendyield": [d["Div Yield"]],
                        "symbol": [d["SYMBOL"]],
                    }
                )

                # Construct the filename
                filename = os.path.join(outfolder, f"{d['SYMBOL']}.rds")
                logger.info(f"Processing Daily Bars for {d['SYMBOL']}")

                if file_exists_and_valid(filename, min_size=1):
                    update_symbol(filename, filename, df)
                    potential_link = get_linked_symbols(df.symbol.item())
                    if len(potential_link) > 1:
                        current_link_index = np.where(d["SYMBOL"] == potential_link.symbol)[0][0]
                        if current_link_index > 0:  # we have name change[s]. merge current data into new name[s]
                            potential_link = potential_link[0:current_link_index]
                            for new_symbol in potential_link.symbol:
                                new_symbol = f"{outfolder}/{new_symbol}_IND___.rds"
                                update_symbol(new_symbol, new_symbol, df)
                else:
                    potential_link = get_linked_symbols(df.symbol.item())
                    if len(potential_link) > 1:
                        current_link_index = np.where(d.symbol == potential_link.symbol)[0][0]
                        for new_symbol in potential_link.symbol[current_link_index:][::-1]:
                            new_symbol = f"{outfolder}/{new_symbol}_IND___.rds"
                            filename_to_save = f"{outfolder}/{df.symbol[0]}_IND___.rds"
                            update_symbol(new_symbol, filename_to_save, df)
                    else:
                        filename_to_save = f"{outfolder}/{df.symbol[0]}_IND___.rds"
                        update_symbol(filename_to_save, filename_to_save, df)

    except Exception as e:
        logger.error(f"Error in save_index_data: {e}")
        send_mail(
            get_dynamic_config().get("from_email_id"),
            get_dynamic_config().get("to_email_id"),
            get_dynamic_config().get("from_email_password"),
            f"Unable to process index data for {p}",
            f"{traceback.format_exc()}",
        )


def save_future_data_old(p: str, session):
    """Save Future Data to Folder (Supported till and including 20240705)

    Args:
        p (str): Processing date as YYYYMMDD
        session: HTTP session for making requests
    """

    def update_symbol(filename_to_update, filename_to_save, row):
        """Update the RDS file with new data."""
        try:
            md = readRDS(filename_to_update)
            md["date"] = md["date"].dt.tz_localize("UTC")
            md["date"] = md["date"].dt.tz_convert("Asia/Kolkata")
        except Exception as e:
            logger.warning(f"Failed to read RDS file {filename_to_update}: {e}")
            md = pd.DataFrame()
        md_updated = pd.concat([md, row], ignore_index=True)
        md_updated = md_updated.drop_duplicates(subset="date", keep="last")
        md_updated = md_updated.sort_values(by="date")
        md_updated.symbol = md_updated.symbol.iloc[0]
        saveRDS(md_updated, filename_to_save)

    def download_and_extract_file(url, dest_file):
        """Download and extract the ZIP file."""
        response = session.get(url)
        if response.status_code == 200:
            save_file(dest_file, response.content)
            logger.info(f"File downloaded successfully for {p}")
            return read_csv_from_zip(dest_file, file_index=0, dtype=str)
        else:
            logger.error(f"Failed to download file for {p}. Status code: {response.status_code}")
            send_mail(
                get_dynamic_config().get("from_email_id"),
                get_dynamic_config().get("to_email_id"),
                get_dynamic_config().get("from_email_password"),
                f"Unable to download future file for {p}",
                f"HTTP Status Code: {response.status_code}",
            )
        return None

    try:
        outfolder = f"{get_dynamic_config().get('daily_prices')}/fut"
        url = f"https://archives.nseindia.com/content/historical/DERIVATIVES/{valid_datetime(p,'%Y')}/{valid_datetime(p,'%b').upper()}/fo{valid_datetime(p,'%d')}{valid_datetime(p,'%b').upper()}{valid_datetime(p,'%Y')}bhav.csv.zip"
        dest_file = f"{get_dynamic_config().get('bhavcopy_folder')}/{p}_fno.zip"

        # Download and extract the data
        data = download_and_extract_file(url, dest_file)
        if data is None:
            return

        # Clean and preprocess the data
        data.columns = [col.strip() for col in data.columns]
        data = data.map(lambda x: x.strip() if isinstance(x, str) else x)
        data = data[data["OPTION_TYP"].isin(["XX", "FF"])]  # Only take future data
        if data.empty:
            logger.info("No data to import from bhavcopy. Check if future data is correct in bhavcopy.")
            return

        # Replace 'SYMBOL' pattern
        nsenifty_pattern = r"^NIFTY$"
        data.loc[data["SYMBOL"].str.match(nsenifty_pattern), "SYMBOL"] = "NSENIFTY"

        # Convert date columns
        date_format = "%d-%b-%Y"
        data["TIMESTAMP"] = pd.to_datetime(data["TIMESTAMP"], format=date_format).dt.tz_localize("Asia/Kolkata")
        data["EXPIRY_DT"] = pd.to_datetime(data["EXPIRY_DT"], format=date_format).dt.strftime("%Y%m%d")

        # Convert numeric columns
        numeric_columns = [
            "VAL_INLAKH",
            "OPEN",
            "HIGH",
            "LOW",
            "CLOSE",
            "SETTLE_PR",
            "CONTRACTS",
            "OPEN_INT",
        ]
        for col in numeric_columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
        data["VAL_INLAKH"] = data["VAL_INLAKH"] * 100000

        # Update 'SYMBOL' column
        data.loc[:, "SYMBOL"] = data["SYMBOL"] + "_FUT_" + data["EXPIRY_DT"] + "__"

        # Process each row in the data
        for _, row in data.iterrows():
            logger.info(f"Processing Daily Bars for {row['SYMBOL']}")
            df = pd.DataFrame(
                {
                    "date": [row["TIMESTAMP"]],
                    "open": [row["OPEN"]],
                    "high": [row["HIGH"]],
                    "low": [row["LOW"]],
                    "close": [row["CLOSE"]],
                    "settle": [row["SETTLE_PR"]],
                    "volume": [row["CONTRACTS"]],
                    "oi": [row["OPEN_INT"]],
                    "tradevalue": [row["VAL_INLAKH"]],
                    "symbol": [row["SYMBOL"]],
                }
            )

            # Construct the filename and directory
            subdir = os.path.join(outfolder, str(row["EXPIRY_DT"]))
            filename = os.path.join(subdir, f"{row['SYMBOL']}.rds")

            # Create directory if it doesn't exist
            make_directory(subdir)
            update_symbol(filename, filename, df)

    except Exception as e:
        logger.error(f"Error in save_future_data_old: {e}")
        send_mail(
            get_dynamic_config().get("from_email_id"),
            get_dynamic_config().get("to_email_id"),
            get_dynamic_config().get("from_email_password"),
            f"Unable to process future data for {p}",
            f"{traceback.format_exc()}",
        )


def save_future_data(p: str, session, save_to_rds=True):
    """Save Future Data to Folder

    Args:
        p (str): processing date as YYYYMMDD
        session: HTTP session for making requests
    """

    def update_symbol(filename_to_update, filename_to_save, row):
        """Update the RDS file with new data."""
        try:
            md = readRDS(filename_to_update)
            md["date"] = md["date"].dt.tz_localize("UTC")
            md["date"] = md["date"].dt.tz_convert("Asia/Kolkata")
        except Exception as e:
            logger.warning(f"Failed to read RDS file {filename_to_update}: {e}")
            md = pd.DataFrame()
        md_updated = pd.concat([md, row], ignore_index=True)
        md_updated = md_updated.drop_duplicates(subset="date", keep="last")
        md_updated = md_updated.sort_values(by="date")
        md_updated.symbol = md_updated.symbol.iloc[0]
        saveRDS(md_updated, filename_to_save)

    def download_and_extract_file(url, dest_file):
        """Download and extract the ZIP file."""
        response = session.get(url)
        if response.status_code == 200:
            save_file(dest_file, response.content)
            logger.info(f"File downloaded successfully for {p}")
            if not save_to_rds:
                return
            return read_csv_from_zip(dest_file, file_index=0, dtype=str)
        else:
            logger.error(f"Failed to download file for {p}. Status code: {response.status_code}")
            send_mail(
                get_dynamic_config().get("from_email_id"),
                get_dynamic_config().get("to_email_id"),
                get_dynamic_config().get("from_email_password"),
                f"Unable to download future file for {p}",
                f"HTTP Status Code: {response.status_code}",
            )
        return None

    try:
        outfolder = f"{get_dynamic_config().get('daily_prices')}/fut"
        url = f"https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_{valid_datetime(p,'%Y')[0]}{valid_datetime(p,'%m')[0]}{valid_datetime(p,'%d')[0]}_F_0000.csv.zip"
        dest_file = f"{get_dynamic_config().get('bhavcopy_folder')}/{p}_fno.zip"

        # Check if destination file exists
        if file_exists_and_valid(dest_file, min_size=1000):
            logger.info(f"File already exists: {dest_file}")
            if not save_to_rds:
                return
            data = read_csv_from_zip(dest_file, file_index=0, dtype=str)
        else:
            # Download and extract the data
            data = download_and_extract_file(url, dest_file)

        if data is None:
            return

        # Clean and preprocess the data
        data.columns = [col.strip() for col in data.columns]
        data = data.map(lambda x: x.strip() if isinstance(x, str) else x)
        data = data[data["FinInstrmTp"].isin(["STF", "IDF"])]  # Only take future data
        if data.empty:
            logger.info("No data to import from bhavcopy. Check if future data is correct in bhavcopy.")
            return

        # Replace 'SYMBOL' pattern
        nsenifty_pattern = r"^NIFTY$"
        data.loc[data["TckrSymb"].str.match(nsenifty_pattern), "TckrSymb"] = "NSENIFTY"
        date_format = "%Y-%m-%d"

        # Convert date columns
        data["TradDt"] = pd.to_datetime(data["TradDt"], format=date_format).dt.tz_localize("Asia/Kolkata")
        data["XpryDt"] = pd.to_datetime(data["XpryDt"], format=date_format).dt.strftime("%Y%m%d")

        # Convert numeric columns
        numeric_columns = [
            "TtlTrfVal",
            "OpnPric",
            "HghPric",
            "LwPric",
            "LastPric",
            "SttlmPric",
            "TtlTradgVol",
            "OpnIntrst",
        ]
        for col in numeric_columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

        # Update 'SYMBOL' column
        data.loc[:, "TckrSymb"] = data["TckrSymb"] + "_FUT_" + data["XpryDt"] + "__"

        # Process each row in the data
        for _, row in data.iterrows():
            logger.info(f"Processing Daily Bars for {row['TckrSymb']}")
            df = pd.DataFrame(
                {
                    "date": [row["TradDt"]],
                    "open": [row["OpnPric"]],
                    "high": [row["HghPric"]],
                    "low": [row["LwPric"]],
                    "close": [row["LastPric"]],
                    "settle": [row["SttlmPric"]],
                    "volume": [row["TtlTradgVol"]],
                    "oi": [row["OpnIntrst"]],
                    "tradevalue": [row["TtlTrfVal"]],
                    "symbol": [row["TckrSymb"]],
                }
            )

            # Construct the filename and directory
            subdir = os.path.join(outfolder, str(row["XpryDt"]))
            filename = os.path.join(subdir, f"{row['TckrSymb']}.rds")

            # Create directory if it doesn't exist
            make_directory(subdir)
            update_symbol(filename, filename, df)

    except Exception as e:
        logger.error(f"Error in save_future_data: {e}")
        send_mail(
            get_dynamic_config().get("from_email_id"),
            get_dynamic_config().get("to_email_id"),
            get_dynamic_config().get("from_email_password"),
            f"Unable to process future data for {p}",
            f"{traceback.format_exc()}",
        )


def save_mf_data(p: str, session, save_to_rds=True):
    """Save Mutual Fund Data to Folder

    Args:
        p (str): Processing date as YYYYMMDD
        session: HTTP session for making requests
    """

    def update_symbol(filename_to_update, filename_to_save, row):
        """Update the RDS file with new data."""
        try:
            md = readRDS(filename_to_update)
            md["date"] = md["date"].dt.tz_localize("UTC")
            md["date"] = md["date"].dt.tz_convert("Asia/Kolkata")
        except Exception as e:
            logger.warning(f"Failed to read RDS file {filename_to_update}: {e}")
            md = pd.DataFrame()
        md_updated = pd.concat([md, row], ignore_index=True)
        md_updated = md_updated.drop_duplicates(subset="date", keep="last")
        md_updated = md_updated.sort_values(by="date")
        md_updated.symbol = md_updated.symbol.iloc[0]
        saveRDS(md_updated, filename_to_save)

    def download_csv(url, dest_file):
        """Download the CSV file."""
        response = session.get(url)
        if response.status_code == 200:
            save_file(dest_file, response.content)
            logger.info(f"Mutual fund file downloaded successfully for {p}")
        else:
            logger.error(f"Failed to download mutual fund file for {p}. Status code: {response.status_code}")
            send_mail(
                get_dynamic_config().get("from_email_id"),
                get_dynamic_config().get("to_email_id"),
                get_dynamic_config().get("from_email_password"),
                f"Unable to download mutual fund file for {p}",
                f"HTTP Status Code: {response.status_code}",
            )
            return None
        return dest_file

    try:
        outfolder = f"{get_dynamic_config().get('daily_prices')}/mf"
        url = f"https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt={p}&todt={p}"
        dest_file = os.path.join(get_dynamic_config().get("bhavcopy_folder"), f"{p}_mf.csv")

        # Download the mutual fund data
        if dest_file is None or not file_exists_and_valid(dest_file, min_size=1000):
            dest_file = download_csv(url, dest_file)
        if not save_to_rds or dest_file is None or not file_exists_and_valid(dest_file, min_size=1000):
            return

        # Read and preprocess the data
        data = read_csv_in_pandas_out(dest_file, sep=";", na_values=["", " "])
        data = data.dropna(how="all")
        rows_to_remove = (data.isna().sum(axis=1) == len(data.columns) - 1) & data.iloc[:, 0].str.contains(
            "Mutual Fund", na=False
        )
        data = data[~rows_to_remove]

        # Forward-fill category information
        data["category"] = data.iloc[:, 0]
        data["category"] = data["category"].where(data["category"].isna(), other=None)
        data["category"] = data["category"].ffill()

        # Remove category headers and clean up
        data = data[data.isna().sum(axis=1) < len(data.columns) - 2]
        data.columns = [
            "code",
            "scheme",
            "isin_growth_dividend",
            "isin_reinvestment",
            "nav",
            "repurchase_price",
            "sale_price",
            "date",
            "category",
        ]

        # Convert 'date' to datetime format
        data["date"] = pd.to_datetime(data["date"], format="%d-%b-%Y")

        # Filter rows with valid ISINs
        data["isin_growth_dividend"] = data["isin_growth_dividend"].apply(
            lambda x: x if pd.notna(x) and x.startswith("IN") else pd.NA
        )
        data["isin_reinvestment"] = data["isin_reinvestment"].apply(
            lambda x: x if pd.notna(x) and x.startswith("IN") else pd.NA
        )
        data = data[data["isin_growth_dividend"].notna() | data["isin_reinvestment"].notna()]

        # Process each row in the data
        for _, row in data.iterrows():
            logger.info(f"Processing Daily Bars for {row['scheme']}")
            df = pd.DataFrame(
                {
                    "date": [row["date"]],
                    "symbol": [row["scheme"]],
                    "open": [row["nav"]],
                    "high": [row["nav"]],
                    "low": [row["nav"]],
                    "close": [row["nav"]],
                    "settle": [row["nav"]],
                    "volume": [0],
                    "sale_price": [row["sale_price"]],
                    "repurchase_price": [row["repurchase_price"]],
                    "category": [row["category"]],
                    "isin_growth_dividend": [row["isin_growth_dividend"]],
                    "isin_reinvestment": [row["isin_reinvestment"]],
                }
            )

            # Save data for growth and reinvestment ISINs
            if pd.notna(row["isin_growth_dividend"]):
                filename = os.path.join(outfolder, f"{row['isin_growth_dividend']}_MF___.rds")
                update_symbol(filename, filename, df)

            if pd.notna(row["isin_reinvestment"]):
                filename = os.path.join(outfolder, f"{row['isin_reinvestment']}_MF___.rds")
                update_symbol(filename, filename, df)

        # Update the mutual fund master file
        mfmaster_data = []
        for file in list_directory(outfolder):
            if file != "mfmaster.rds":
                file_path = os.path.join(outfolder, file)
                md = readRDS(file_path)
                if not md.empty:
                    last_row = md.iloc[-1]
                    mfmaster_data.append(
                        {
                            "isin": file.split("_")[0],
                            "scheme": last_row["symbol"],
                            "category": last_row["category"],
                            "lastupdate": last_row["date"],
                        }
                    )

        mfmaster = pd.DataFrame(mfmaster_data, columns=["isin", "scheme", "category", "lastupdate"])
        saveRDS(mfmaster, os.path.join(outfolder, "mfmaster.rds"))

    except Exception as e:
        logger.error(f"Error in save_mf_data: {e}")
        send_mail(
            get_dynamic_config().get("from_email_id"),
            get_dynamic_config().get("to_email_id"),
            get_dynamic_config().get("from_email_password"),
            f"Unable to process mutual fund data for {p}",
            f"{traceback.format_exc()}",
        )


def save_option_data_old(p: str, session):
    """Save Option Data to Folder (Supported till and including 20240705)

    Args:
        p (str): Processing date as YYYYMMDD
        session: HTTP session for making requests
    """

    def update_symbol(filename_to_update, filename_to_save, row):
        """Update the RDS file with new data."""
        try:
            md = readRDS(filename_to_update)
            md["date"] = md["date"].dt.tz_localize("UTC")
            md["date"] = md["date"].dt.tz_convert("Asia/Kolkata")
        except Exception as e:
            logger.warning(f"Failed to read RDS file {filename_to_update}: {e}")
            md = pd.DataFrame()
        md_updated = pd.concat([md, row], ignore_index=True)
        md_updated = md_updated.drop_duplicates(subset="date", keep="last")
        md_updated = md_updated.sort_values(by="date")
        md_updated.symbol = md_updated.symbol.iloc[0]
        saveRDS(md_updated, filename_to_save)

    def download_and_extract_file(url, dest_file):
        """Download and extract the ZIP file."""
        response = session.get(url)
        if response.status_code == 200:
            save_file(dest_file, response.content)
            logger.info(f"File downloaded successfully for {p}")
            return read_csv_from_zip(dest_file, file_index=0, dtype=str)
        else:
            logger.error(f"Failed to download file for {p}. Status code: {response.status_code}")
            send_mail(
                get_dynamic_config().get("from_email_id"),
                get_dynamic_config().get("to_email_id"),
                get_dynamic_config().get("from_email_password"),
                f"Unable to download option file for {p}",
                f"HTTP Status Code: {response.status_code}",
            )
        return None

    try:
        outfolder = f"{get_dynamic_config().get('daily_prices')}/opt"
        url = f"https://archives.nseindia.com/content/historical/DERIVATIVES/{valid_datetime(p,'%Y')[0]}/{valid_datetime(p,'%b')[0].upper()}/fo{valid_datetime(p,'%d')[0]}{valid_datetime(p,'%b')[0].upper()}{valid_datetime(p,'%Y')[0]}bhav.csv.zip"
        dest_file = f"{get_dynamic_config().get('bhavcopy_folder')}/{p}_fno.zip"
        data = download_and_extract_file(url, dest_file)
        if data is None:
            return

        # Clean and preprocess the data
        data.columns = [col.strip() for col in data.columns]
        data = data.map(lambda x: x.strip() if isinstance(x, str) else x)
        data = data[data["OPTION_TYP"] != "XX"]  # Exclude invalid option types
        if data.empty:
            logger.info("No data to import from bhavcopy. Check if option type is correct in bhavcopy.")
            return

        # Replace 'SYMBOL' pattern
        nsenifty_pattern = r"^NIFTY$"
        data.loc[data["SYMBOL"].str.match(nsenifty_pattern), "SYMBOL"] = "NSENIFTY"

        # Convert date columns
        date_format = "%d-%b-%Y"
        data["TIMESTAMP"] = pd.to_datetime(data["TIMESTAMP"], format=date_format).dt.tz_localize("Asia/Kolkata")
        data["EXPIRY_DT"] = pd.to_datetime(data["EXPIRY_DT"], format=date_format).dt.strftime("%Y%m%d")

        # Convert numeric columns
        numeric_columns = [
            "VAL_INLAKH",
            "OPEN",
            "HIGH",
            "LOW",
            "CLOSE",
            "SETTLE_PR",
            "CONTRACTS",
            "OPEN_INT",
        ]
        for col in numeric_columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
        data["VAL_INLAKH"] = data["VAL_INLAKH"] * 100000

        # Update 'SYMBOL' column
        data.loc[data["OPTION_TYP"] == "XX", "SYMBOL"] = data["SYMBOL"] + "_FUT_" + data["EXPIRY_DT"] + "__"
        data.loc[data["OPTION_TYP"].isin(["PA", "PE"]), "SYMBOL"] = (
            data["SYMBOL"] + "_OPT_" + data["EXPIRY_DT"] + "_PUT_" + data["STRIKE_PR"]
        )
        data.loc[data["OPTION_TYP"].isin(["CA", "CE"]), "SYMBOL"] = (
            data["SYMBOL"] + "_OPT_" + data["EXPIRY_DT"] + "_CALL_" + data["STRIKE_PR"]
        )

        # Process each row in the data
        for _, row in data.iterrows():
            logger.info(f"Processing Daily Bars for {row['SYMBOL']}")
            df = pd.DataFrame(
                {
                    "date": [row["TIMESTAMP"]],
                    "open": [row["OPEN"]],
                    "high": [row["HIGH"]],
                    "low": [row["LOW"]],
                    "close": [row["CLOSE"]],
                    "settle": [row["SETTLE_PR"]],
                    "volume": [row["CONTRACTS"]],
                    "oi": [row["OPEN_INT"]],
                    "tradevalue": [row["VAL_INLAKH"]],
                    "symbol": [row["SYMBOL"]],
                }
            )

            # Construct the filename and directory
            subdir = os.path.join(outfolder, str(row["EXPIRY_DT"]))
            filename = os.path.join(subdir, f"{row['SYMBOL']}.rds")

            # Create directory if it doesn't exist
            make_directory(subdir)
            update_symbol(filename, filename, df)

    except Exception as e:
        logger.error(f"Error in save_option_data_old: {e}")
        send_mail(
            get_dynamic_config().get("from_email_id"),
            get_dynamic_config().get("to_email_id"),
            get_dynamic_config().get("from_email_password"),
            f"Unable to process option data for {p}",
            f"{traceback.format_exc()}",
        )


def save_option_data(p: str, session, save_to_rds=True):
    """Save Option Data to Folder

    Args:
        p (str): Processing date as YYYYMMDD
        session: HTTP session for making requests
    """

    def update_symbol(filename_to_update, filename_to_save, row):
        """Update the RDS file with new data."""
        try:
            md = readRDS(filename_to_update)
            md["date"] = md["date"].dt.tz_localize("UTC")
            md["date"] = md["date"].dt.tz_convert("Asia/Kolkata")
        except Exception as e:
            logger.warning(f"Failed to read RDS file {filename_to_update}: {e}")
            md = pd.DataFrame()
        md_updated = pd.concat([md, row], ignore_index=True)
        md_updated = md_updated.drop_duplicates(subset="date", keep="last")
        md_updated = md_updated.sort_values(by="date")
        md_updated.symbol = md_updated.symbol.iloc[0]
        saveRDS(md_updated, filename_to_save)

    def download_and_extract_file(url, dest_file):
        """Download and extract the ZIP file."""
        response = session.get(url)
        if response.status_code == 200:
            save_file(dest_file, response.content)
            logger.info(f"File downloaded successfully for {p}")
            return read_csv_from_zip(dest_file, file_index=0, dtype=str)
        else:
            logger.error(f"Failed to download file for {p}. Status code: {response.status_code}")
            send_mail(
                get_dynamic_config().get("from_email_id"),
                get_dynamic_config().get("to_email_id"),
                get_dynamic_config().get("from_email_password"),
                f"Unable to download option file for {p}",
                f"HTTP Status Code: {response.status_code}",
            )
        return None

    try:
        outfolder = f"{get_dynamic_config().get('daily_prices')}/opt"
        url = f"https://archives.nseindia.com/content/historical/DERIVATIVES/{valid_datetime(p,'%Y')[0]}/{valid_datetime(p,'%b')[0].upper()}/fo{valid_datetime(p,'%d')[0]}{valid_datetime(p,'%b')[0].upper()}{valid_datetime(p,'%Y')[0]}bhav.csv.zip"
        dest_file = f"{get_dynamic_config().get('bhavcopy_folder')}/{p}_fno.zip"

        # Check if destination file exists
        if file_exists_and_valid(dest_file, min_size=1000):
            logger.info(f"File already exists: {dest_file}")
            if not save_to_rds:
                return
            data = read_csv_from_zip(dest_file, file_index=0, dtype=str)
        else:
            # Download and extract the data
            data = download_and_extract_file(url, dest_file)

        if data is None:
            return

        # Clean and preprocess the data
        data.columns = [col.strip() for col in data.columns]
        data = data.map(lambda x: x.strip() if isinstance(x, str) else x)
        data = data[data["OPTION_TYP"] != "XX"]  # Exclude invalid option types
        if data.empty:
            logger.info("No data to import from bhavcopy. Check if option type is correct in bhavcopy.")
            return

        # Replace 'SYMBOL' pattern
        nsenifty_pattern = r"^NIFTY$"
        data.loc[data["SYMBOL"].str.match(nsenifty_pattern), "SYMBOL"] = "NSENIFTY"

        # Convert date columns
        date_format = "%d-%b-%Y"
        data["TIMESTAMP"] = pd.to_datetime(data["TIMESTAMP"], format=date_format).dt.tz_localize("Asia/Kolkata")
        data["EXPIRY_DT"] = pd.to_datetime(data["EXPIRY_DT"], format=date_format).dt.strftime("%Y%m%d")

        # Convert numeric columns
        numeric_columns = [
            "VAL_INLAKH",
            "OPEN",
            "HIGH",
            "LOW",
            "CLOSE",
            "SETTLE_PR",
            "CONTRACTS",
            "OPEN_INT",
        ]
        for col in numeric_columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
        data["VAL_INLAKH"] = data["VAL_INLAKH"] * 100000

        # Update 'SYMBOL' column
        data.loc[data["OPTION_TYP"] == "XX", "SYMBOL"] = data["SYMBOL"] + "_FUT_" + data["EXPIRY_DT"] + "__"
        data.loc[data["OPTION_TYP"].isin(["PA", "PE"]), "SYMBOL"] = (
            data["SYMBOL"] + "_OPT_" + data["EXPIRY_DT"] + "_PUT_" + data["STRIKE_PR"]
        )
        data.loc[data["OPTION_TYP"].isin(["CA", "CE"]), "SYMBOL"] = (
            data["SYMBOL"] + "_OPT_" + data["EXPIRY_DT"] + "_CALL_" + data["STRIKE_PR"]
        )

        # Process each row in the data
        for _, row in data.iterrows():
            logger.info(f"Processing Daily Bars for {row['SYMBOL']}")
            df = pd.DataFrame(
                {
                    "date": [row["TIMESTAMP"]],
                    "open": [row["OPEN"]],
                    "high": [row["HIGH"]],
                    "low": [row["LOW"]],
                    "close": [row["CLOSE"]],
                    "settle": [row["SETTLE_PR"]],
                    "volume": [row["CONTRACTS"]],
                    "oi": [row["OPEN_INT"]],
                    "tradevalue": [row["VAL_INLAKH"]],
                    "symbol": [row["SYMBOL"]],
                }
            )

            # Construct the filename and directory
            subdir = os.path.join(outfolder, str(row["EXPIRY_DT"]))
            filename = os.path.join(subdir, f"{row['SYMBOL']}.rds")

            # Create directory if it doesn't exist
            make_directory(subdir)
            update_symbol(filename, filename, df)

    except Exception as e:
        logger.error(f"Error in save_option_data: {e}")
        send_mail(
            get_dynamic_config().get("from_email_id"),
            get_dynamic_config().get("to_email_id"),
            get_dynamic_config().get("from_email_password"),
            f"Unable to process option data for {p}",
            f"{traceback.format_exc()}",
        )
