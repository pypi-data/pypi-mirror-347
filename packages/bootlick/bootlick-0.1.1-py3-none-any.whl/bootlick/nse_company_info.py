import datetime as dt
import io
import json
import logging
import math
import os
import re
import time
import traceback
from pathlib import Path
from nse import NSE
import pandas as pd
from chameli.dateutils import valid_datetime
from chameli.interactions import (file_exists_and_valid,
                                  read_csv_in_pandas_out, readRDS, save_file,
                                  save_pandas_in_csv_out, saveRDS, send_mail)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .config import get_config

logger = logging.getLogger(__name__)


def get_dynamic_config():
    return get_config()


DIR = Path(__file__).parent

nse = NSE(download_folder=DIR, server=False)


def save_symbol_data(session, saveToFolder: bool = True):
    try:
        url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
        url = "https://openapi.5paisa.com/VendorsAPI/Service1.svc/ScripMaster/segment/All"
        dest_file = f"{get_dynamic_config().get('bhavcopy_folder')}/{dt.datetime.today().strftime('%Y%m%d')}_codes.csv"
        response = session.get(url, allow_redirects=True)
        if response.status_code == 200:
            df = pd.read_csv(io.BytesIO(response.content))
            # Rename the column
            df.rename(columns={"ScripCode": "Scripcode"}, inplace=True)
            # Save the DataFrame back to CSV
            save_pandas_in_csv_out(dest_file, index=False)
            codes = read_csv_in_pandas_out(dest_file, dtype=str)
            numeric_columns = [
                "Scripcode",
                "StrikeRate",
                "LotSize",
                "QtyLimit",
                "Multiplier",
                "TickSize",
            ]
            for col in numeric_columns:
                codes[col] = pd.to_numeric(codes[col], errors="coerce")
            codes.columns = [col.strip() for col in codes.columns]
            codes = codes.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            codes = codes[
                (codes.Exch.isin(["N", "M"]))
                & (codes.ExchType.isin(["C", "D"]))
                & (codes.Series.isin(["EQ", "BE", "XX", "BZ", "RR", "IV", ""]))
            ]
            pattern = r"\d+GS\d+"
            codes = codes[~codes["Name"].str.contains(pattern, regex=True, na=True)]
            codes["long_symbol"] = None
            # Converting specific columns to numeric
            numeric_columns = ["LotSize", "TickSize", "Scripcode"]

            for col in numeric_columns:
                codes[col] = pd.to_numeric(codes[col], errors="coerce")

            # Vectorized string splitting
            codes["symbol_vec"] = codes["Name"].str.split(" ")

            # Function to process each row
            def process_row(row):
                symbol_vec = row["symbol_vec"]
                ticksize = row["TickSize"]

                if len(symbol_vec) == 1 or ticksize == 0:
                    return f"{symbol_vec[0]}_STK___" if ticksize > 0 else f"{''.join(symbol_vec)}_IND___".upper()
                elif len(symbol_vec) == 4:
                    expiry_str = f"{symbol_vec[3]}{symbol_vec[2]}{symbol_vec[1]}"
                    try:
                        expiry = dt.datetime.strptime(expiry_str, "%Y%b%d").strftime("%Y%m%d")
                        return f"{symbol_vec[0]}_FUT_{expiry}__".upper()
                    except ValueError:
                        return pd.NA
                elif len(symbol_vec) == 6:
                    expiry_str = f"{symbol_vec[3]}{symbol_vec[2]}{symbol_vec[1]}"
                    try:
                        expiry = dt.datetime.strptime(expiry_str, "%Y%b%d").strftime("%Y%m%d")
                        right = "CALL" if symbol_vec[4] == "CE" else "PUT"
                        strike = ("%f" % float(symbol_vec[5])).rstrip("0").rstrip(".")
                        return f"{symbol_vec[0]}_OPT_{expiry}_{right}_{strike}".upper()
                    except ValueError:
                        return pd.NA
                else:
                    return pd.NA

            # Apply the function to each row
            codes["long_symbol"] = codes.apply(process_row, axis=1)

            # Save to CSV
            if saveToFolder:
                dest_symbol_file = f"{get_dynamic_config().get('static_downloads')}/symbols/{dt.datetime.today().strftime('%Y%m%d')}_symbols.csv"
                save_pandas_in_csv_out(
                    codes[["long_symbol", "LotSize", "Scripcode", "Exch", "ExchType", "TickSize"]],
                    dest_symbol_file,
                    index=False,
                )
            return codes
        else:
            send_mail(
                get_dynamic_config().get("from_email_id"),
                get_dynamic_config().get("to_email_id"),
                get_dynamic_config().get("from_email_password"),
                "Unable to download symbol file from 5paisa",
                f"{traceback.format_exc()}",
            )
    except Exception:
        send_mail(
            get_dynamic_config().get("from_email_id"),
            get_dynamic_config().get("to_email_id"),
            get_dynamic_config().get("from_email_password"),
            f"Unable to download symbol file for {dt.datetime.today().strftime('%Y%m%d')}",
            f"{traceback.format_exc()}",
        )


def fetch_json_with_selenium(driver, url):
    try:
        data = []
        driver.get(url)
    except Exception:
        time.sleep(3)
        driver.back()
        time.sleep(2)
        driver.forward()
        time.sleep(3)
        raw_data_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "rawdata-tab")))
        raw_data_tab.click()
        time.sleep(2)  # Wait for the raw data to load

        # Locate the element containing the raw JSON data
        raw_data_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".panelContent"))
        )
        raw_data_text = raw_data_element.text

        # Parse the JSON data
        data = json.loads(raw_data_text)
    finally:
        return data

def fetch_json_with_nseapi(category):
    out = []
    # Ensure the `nse` instance is used to call the method
    if category == "corporate-actions":
        out = nse.actions(segment='equities')
    elif category == "board-meetings":
        out = nse.boardMeetings(index='equities')  # Use the `nse` instance
    else:
        pass
    return out



def update_board_meetings(driver, update_historical_bm: bool = False):
    """
    Update board meetings using Selenium WebDriver.
    """

    def get_board_meeting(driver, symbol=None):

        if symbol is not None:
            modified_endpoint = nse_api_endpoint + "&symbol=" + symbol
        else:
            modified_endpoint = nse_api_endpoint

        try:
            # data = fetch_json_with_selenium(driver, modified_endpoint)
            data = fetch_json_with_nseapi("board-meetings")
            json_str = json.dumps(data, indent=2)
            logger.info(f"Board Meetings :\n{json_str}")
            # Process the data
            out = []
            for d in data:
                if isinstance(d, dict):
                    purpose = d.get("bm_purpose", "") + d.get("bm_desc", "")
                    if purpose != "":
                        results = ["results", "financial", "statement"]
                        dividends = ["dividend"]
                        fundraise = ["fundrai", "capitalrai"]
                        purpose_result = []
                        if any(ele in purpose.replace(" ", "").lower() for ele in results):
                            purpose_result.append("Results")
                        if any(ele in purpose.replace(" ", "").lower() for ele in dividends):
                            purpose_result.append("Dividend")
                        if any(ele in purpose.replace(" ", "").lower() for ele in fundraise):
                            purpose_result.append("FundRaise")
                        else:
                            pass
                    purpose = "/".join(purpose_result) if purpose_result else "Other"
                    date = d.get("bm_date")
                    if date is not None:
                        date = valid_datetime(date, "%Y%m%d")[0]
                    symbol = d.get("bm_symbol")
                    announce_date = d.get("bm_timestamp")
                    if announce_date is not None:
                        announce_date = valid_datetime(announce_date, "%Y%m%d-%H%M%S")[0]
                    out.append({"date": date, "symbol": symbol, "purpose": purpose, "announce_date": announce_date})
            return pd.DataFrame(out)

        except Exception as e:
            logger.error(f"Error while fetching board meetings: {e}")
            return pd.DataFrame()

    try:
        nse_api_endpoint = get_dynamic_config().get("nse_bm_api_endpoint")
        bm = readRDS(get_dynamic_config().get("bm_file"))
        if update_historical_bm:
            symbols = symbols = list(set(bm.symbol))
            for symbol in symbols:
                bm_new = get_board_meeting(driver, symbol)
                if len(bm_new) > 0:
                    bm = pd.concat([bm, bm_new])
        else:
            bm_new = get_board_meeting(driver, symbol=None)
            if len(bm_new) > 0:
                bm = pd.concat([bm, bm_new])
        bm.reset_index(inplace=True, drop=True)

        # Normalize the 'announce_date' column to ensure consistent data types
        bm["announce_date"] = bm["announce_date"].astype(str).replace("nan", "")
        bm["announce_date_flag"] = bm["announce_date"].notna()
        bm = (
            bm.sort_values(by=["announce_date_flag", "announce_date"], ascending=[False, True])
            .drop_duplicates(["symbol", "date"])
            .drop("announce_date_flag", axis=1)
        )
        bm.sort_values("date", inplace=True)
        bm.reset_index(inplace=True, drop=True)
        saveRDS(bm, get_dynamic_config().get("bm_file"))
    except Exception:
        send_mail(
            get_dynamic_config().get("from_email_id"),
            get_dynamic_config().get("to_email_id"),
            get_dynamic_config().get("from_email_password"),
            f"Error while trying to get board meetings on {dt.datetime.today().strftime('%Y%m%d')}",
            f"{traceback.format_exc()}",
        )


def update_dividends(driver, query_symbol=None):

    try:
        nse_api_endpoint = get_dynamic_config().get("nse_ca_api_endpoint")
        if query_symbol is not None:
            modified_nse_api_endpoint = nse_api_endpoint + "&symbol=" + query_symbol
        else:
            modified_nse_api_endpoint = nse_api_endpoint
        # data = fetch_json_with_selenium(driver, modified_nse_api_endpoint)
        data = fetch_json_with_nseapi("corporate-actions")
        json_str = json.dumps(data, indent=2)
        logger.info(f"Dividends :\n{json_str}")
        out = []
        for d in data:
            if isinstance(d, dict):
                symbol = d.get("symbol")
                fv = d.get("faceVal")
                if fv is not None:
                    fv = float(fv)
                ex_date = d.get("exDate")
                if ex_date is not None:
                    ex_date = valid_datetime(ex_date, "%Y%m%d")[0]
                subject = d.get("subject").lower()
                if subject is not None:
                    dividend_list = subject.split("dividend")[1:]
                    if len(dividend_list) > 0:
                        d_formatted = json.dumps(d, indent=4)
                        logger.info(f"Dividend :\n{d_formatted}")
                        for d in dividend_list:
                            if re.search("bonus", d) is None and re.search("split", d) is None:
                                temp = re.findall(r"([0-9][,.]*[0-9]*)|$", d)[0]
                                if temp != "":
                                    out.append({"date": ex_date, "symbol": symbol, "dps": float(temp), "fv": fv})
                                else:
                                    out.append({"date": ex_date, "symbol": symbol, "dps": 0, "fv": fv})
        out = pd.DataFrame(out)
        div = readRDS(get_dynamic_config().get("div_file"))
        if len(out) > 0:
            div = pd.concat([div, out])
            div = div.sort_values(by=["date", "dps"], ascending=[True, False]).drop_duplicates(["symbol", "date", "fv"])
            div.reset_index(inplace=True, drop=True)
            div.sort_values("date", inplace=True)
        saveRDS(div, get_dynamic_config().get("div_file"))
    except Exception:
        send_mail(
            get_dynamic_config().get("from_email_id"),
            get_dynamic_config().get("to_email_id"),
            get_dynamic_config().get("from_email_password"),
            f"Error while trying to get dividends on {dt.datetime.today().strftime('%Y%m%d')}",
            f"{traceback.format_exc()}",
        )


def update_split_bonus(driver, query_symbol=None):

    out = []
    nse_api_endpoint = get_dynamic_config().get("nse_ca_api_endpoint")
    try:
        if query_symbol is not None:
            modified_nse_api_endpoint = nse_api_endpoint + "&symbol=" + query_symbol
        else:
            modified_nse_api_endpoint = nse_api_endpoint
        # data = fetch_json_with_selenium(driver, modified_nse_api_endpoint)
        data = fetch_json_with_nseapi("corporate-actions")
        json_str = json.dumps(data, indent=4)
        logger.info(f"Splits and Bonus :\n{json_str}")
        for d in data:
            if isinstance(d, dict):
                symbol = d.get("symbol")
                ex_date = d.get("exDate")
                if ex_date is not None:
                    ex_date = valid_datetime(ex_date, "%Y%m%d")[0]
                subject = d.get("subject").lower()
                if subject is not None:
                    bonus_list = subject.split("bonus")[1:]
                    if len(bonus_list) > 0:
                        d_formatted = json.dumps(d, indent=4)
                        logger.info(f"Bonus :\n{d_formatted}")
                        d = bonus_list[0]
                        numbers = re.findall(r"\d+|$", d)
                        if len(numbers) >= 2:
                            new_shares = int(re.findall(r"\d+|$", d)[0])
                            old_shares = int(re.findall(r"\d+|$", d)[1])
                            new_shares = new_shares + old_shares
                            gcd = math.gcd(old_shares, new_shares)
                            old_shares = old_shares / gcd
                            new_shares = new_shares / gcd
                            out.append(
                                {
                                    "date": ex_date,
                                    "symbol": symbol,
                                    "oldshares": old_shares,
                                    "newshares": new_shares,
                                    "purpose": "Bonus",
                                }
                            )
                    split_list = subject.split("split")[1:]
                    if len(split_list) > 0:
                        d_formatted = json.dumps(d, indent=4)
                        logger.info(f"Bonus :\n{d_formatted}")
                        d = split_list[0]
                        numbers = re.findall(r"\d+|$", d)
                        if len(numbers) >= 2:
                            new_shares = int(re.findall(r"\d+|$", d)[0])
                            old_shares = int(re.findall(r"\d+|$", d)[1])
                            gcd = math.gcd(old_shares, new_shares)
                            old_shares = old_shares / gcd
                            new_shares = new_shares / gcd
                            out.append(
                                {
                                    "date": ex_date,
                                    "symbol": symbol,
                                    "oldshares": old_shares,
                                    "newshares": new_shares,
                                    "purpose": "Split",
                                }
                            )
        out = pd.DataFrame(out)
        splits = readRDS(get_dynamic_config().get("splits_file"))
        if len(out) > 0:
            splits = pd.concat([splits, out])
            splits = splits.sort_values(by=["date"], ascending=[True]).drop_duplicates(
                ["symbol", "date", "oldshares", "newshares"]
            )
            splits.reset_index(inplace=True, drop=True)
            splits.sort_values("date", inplace=True)
        saveRDS(splits, get_dynamic_config().get("splits_file"))
    except Exception:
        send_mail(
            get_dynamic_config().get("from_email_id"),
            get_dynamic_config().get("to_email_id"),
            get_dynamic_config().get("from_email_password"),
            f"Error while trying to get splits and bonuses on {dt.datetime.today().strftime('%Y%m%d')}",
            f"{traceback.format_exc()}",
        )


def get_symbol_change(session):
    try:
        symbolchange_old = readRDS(get_dynamic_config().get("symbolchange_file"))
        symbolchange_old["effectivedate"] = symbolchange_old["effectivedate"].dt.tz_localize("UTC")
        symbolchange_old["effectivedate"] = symbolchange_old["effectivedate"].dt.tz_convert("Asia/Kolkata")

        url = "https://archives.nseindia.com/content/equities/symbolchange.csv"
        dest_file = f"{get_dynamic_config().get('static_downloads')}/downloads/symbolchange_{dt.datetime.today().strftime('%Y%m%d')}.csv"
        if not os.path.exists(dest_file):
            # Downloading the file
            response = session.get(url)
            if response.status_code == 200:
                save_file(dest_file, response.content)
            else:
                send_mail(
                    get_dynamic_config().get("from_email_id"),
                    get_dynamic_config().get("to_email_id"),
                    get_dynamic_config().get("from_email_password"),
                    f"Error while trying to download symbolchange.csv {dt.datetime.today().strftime('%Y%m%d')}",
                    "Pleae re-run python script",
                )

        if file_exists_and_valid(dest_file, min_size=1):
            symbolchange_new = read_csv_in_pandas_out(dest_file, encoding="latin1", header=None, dtype=str)
            if symbolchange_new.iloc[0, 3] == "SM_APPLICABLE_FROM":
                symbolchange_new = pd.read_csv(dest_file, encoding="latin1", header=True, dtype=str)
            else:
                symbolchange_new.columns = ["SYMB_COMPANY_NAME", "SM_KEY_SYMBOL", "SM_NEW_SYMBOL", "SM_APPLICABLE_FROM"]

            if len(symbolchange_new) > 0:
                # Convert 'SM_APPLICABLE_FROM' to datetime with the specified format
                symbolchange_new["SM_APPLICABLE_FROM"] = pd.to_datetime(
                    symbolchange_new["SM_APPLICABLE_FROM"], format="%d-%b-%Y"
                )
                symbolchange_new["SM_APPLICABLE_FROM"] = symbolchange_new["SM_APPLICABLE_FROM"].dt.tz_localize(
                    "Asia/Kolkata"
                )
                # Create a new DataFrame 'md1' with selected columns
                md1 = symbolchange_new[["SM_APPLICABLE_FROM", "SM_KEY_SYMBOL", "SM_NEW_SYMBOL"]].copy()
                md1.columns = ["effectivedate", "oldsymbol", "newsymbol"]
                md1 = md1.loc[md1.oldsymbol != md1.newsymbol,]
                symbolchange = pd.concat([symbolchange_old, md1], ignore_index=True)
                symbolchange = symbolchange.drop_duplicates()
                symbolchange = symbolchange.sort_values(by="effectivedate")
                # Resetting the index
                symbolchange.reset_index(drop=True, inplace=True)
                saveRDS(symbolchange, get_dynamic_config().get("symbolchange_file"))
    except Exception:
        send_mail(
            get_dynamic_config().get("from_email_id"),
            get_dynamic_config().get("to_email_id"),
            get_dynamic_config().get("from_email_password"),
            f"Unable to download symbolchange file for {dt.datetime.today().strftime('%Y%m%d')}",
            f"{traceback.format_exc()}",
        )
