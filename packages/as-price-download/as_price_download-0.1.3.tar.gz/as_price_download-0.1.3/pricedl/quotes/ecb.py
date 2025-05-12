"""
Price downloader for ECB data (currencies).
"""

import datetime
import os
import tempfile
import eurofx

from loguru import logger
import pandas as pd

from pricedl.model import Price
from pricedl.quote import Downloader


class EcbDownloader(Downloader):
    """
    Downloader for ECB data (currencies).
    """

    async def download(self, security_symbol, currency):
        """
        Download the price for the given symbol.
        """
        currency = currency.upper()
        symbol = security_symbol.mnemonic.upper()
        logger.debug(f"Downloading price for {symbol} in {currency}")

        # Check if we have cached daily rates file.
        if self.daily_cache_exists():
            logger.debug("Using cached daily rates")
            daily_df = self.read_daily_cache()
        else:
            daily_df = eurofx.get_daily_data_df()
            # cache it
            self.write_daily_cache(daily_df)

        # daily = eurofx.get_daily_data()
        # historical = eurofx.get_historical_data()
        # currencies = eurofx.get_currency_list()

        # historical_df = eurofx.get_historical_data_df()
        # currencies_df_ = eurofx.get_currency_list_df()

        df = daily_df
        # rate = df.at['2025-05-10', 'USD']
        rate = df.iloc[0][symbol]

        # pd.Timestamp
        timestamp = df.index[0]
        logger.debug(f"timestamp: {timestamp}")
        date = timestamp.date()

        return Price(symbol=security_symbol, date=date, value=rate, currency=currency,
                     source="ECB")

    def daily_cache_exists(self):
        """
        Checks if the daily rates file exists.
        """
        cache_path = self.get_cache_path()
        return os.path.exists(cache_path)

    def get_cache_path(self):
        """
        Returns the path to the cache file.
        """
        temp_dir = tempfile.gettempdir()
        filename = datetime.date.today().isoformat()
        # Change extension to change the format.
        extension = "csv"
        return os.path.join(temp_dir, f"{filename}.{extension}")

    def write_daily_cache(self, df: pd.DataFrame):
        """
        Caches the daily rates.
        """
        cache_path = self.get_cache_path()

        # support different formats
        if cache_path.endswith(".csv"):
            df.to_csv(cache_path, index=True)
        elif cache_path.endswith(".feather"):
            df.to_feather(cache_path)
        else:
            raise ValueError(f"Unsupported file format: {cache_path}")

    def read_daily_cache(self) -> pd.DataFrame:
        """
        Reads the cached daily rates.
        """
        logger.debug("Reading cached daily rates")

        cache_path = self.get_cache_path()

        # support different formats
        if cache_path.endswith(".csv"):
            df = pd.read_csv(cache_path, index_col=0, parse_dates=True)
        elif cache_path.endswith(".feather"):
            df = pd.read_feather(cache_path)
        else:
            raise ValueError(f"Unsupported file format: {cache_path}")
        return df
