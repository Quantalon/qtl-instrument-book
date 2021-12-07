from qtl_instrument_book import FuturesInstrumentBook
from qtl_instrument_book import OptionsInstrumentBook


def test():
    symbol = 'INE.sc2203'
    futures_instrument_book = FuturesInstrumentBook()

    i = futures_instrument_book.get_instrument(symbol)
    print(i)

    i = futures_instrument_book.get_instrument_by_id('sc2203')
    print(i)

    r = futures_instrument_book.is_trading_time(symbol)
    print(r)

    symbol = 'CFFEX.IO2202-C-5000'
    options_instrument_book = OptionsInstrumentBook()

    i = options_instrument_book.get_instrument(symbol)
    print(i)

    i = options_instrument_book.get_instrument_by_id('IO2202-C-5000')
    print(i)

    r = options_instrument_book.is_trading_time(symbol)
    print(r)


if __name__ == '__main__':
    test()
