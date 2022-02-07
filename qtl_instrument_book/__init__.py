import itertools
from pathlib import Path
from datetime import datetime
import warnings
import urllib.request

import toml


def load_toml_by_url(url):
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    data = toml.loads(content)
    return data


def time_to_marked_ts(t):
    if t.hour < 6:
        hour = 24 + t.hour
    else:
        hour = t.hour
    seconds = hour * 3600 + t.minute * 60 + t.second
    return seconds


def time_str_to_marked_ts(time_str):
    parts = [int(i) for i in time_str.split(':')]
    seconds = parts[0] * 3600 + parts[1] * 60 + parts[2]
    return seconds


def to_trading_periods(trading_time_config):
    periods = []
    for period_config in itertools.chain(*trading_time_config.values()):
        periods.append((
            time_str_to_marked_ts(period_config[0]), time_str_to_marked_ts(period_config[1])
        ))
    return periods


class BaseInstrumentBook:
    meta_url = 'https://quantalon.gd2.qingstor.com/instrument-book/meta.toml'

    def __init__(self):
        self.data_file_path = None
        self.current_dir = Path(__file__).parent
        self.meta = load_toml_by_url(self.meta_url)
        if self.type is not None:
            self.download_data_file()
            self.load_data()

    def download_data_file(self):
        filename = self.meta[self.type]['filename']
        self.data_file_path = self.current_dir / filename
        if self.data_file_path.exists():
            return
        url = self.meta[self.type]['url']
        response = urllib.request.urlopen(url)
        data = response.read()
        self.data_file_path.write_bytes(data)

    def load_data(self):
        config = toml.load(self.data_file_path)
        self.instruments = config['instruments']
        expire_date = config['expire_date']
        now = datetime.now()
        if now.date() > expire_date:
            warnings.warn('the instruments config is expired...')
        # cache
        self.symbol_trading_periods = {}
        self.instrument_id_instruments = {}

    def get_instrument_by_id(self, instrument_id):
        if instrument_id in self.instrument_id_instruments:
            return self.instrument_id_instruments[instrument_id]
        for symbol, instrument in self.instruments.items():
            if instrument['id'] == instrument_id:
                self.instrument_id_instruments[instrument_id] = instrument
                return instrument
        return None

    def get_instrument(self, symbol):
        return self.instruments[symbol]

    def is_trading_time(self, symbol, dt=None):
        if dt is None:
            t = datetime.now().time()
        else:
            t = dt.time()

        if symbol in self.symbol_trading_periods:
            trading_periods = self.symbol_trading_periods[symbol]
        else:
            trading_time_config = self.instruments[symbol]['trading_time']
            trading_periods = to_trading_periods(trading_time_config)
            self.symbol_trading_periods[symbol] = trading_periods

        marked_ts = time_to_marked_ts(t)
        for p in trading_periods:
            if p[0] <= marked_ts < p[1]:
                return True
        return False


class FuturesInstrumentBook(BaseInstrumentBook):
    type = 'futures'


class OptionsInstrumentBook(BaseInstrumentBook):
    type = 'options'
