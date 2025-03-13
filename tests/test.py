from qtl_instrument_book import FuturesInstrumentBook
from qtl_instrument_book import OptionsInstrumentBook


def test():
    symbol = 'INE.sc2509'
    futures_instrument_book = FuturesInstrumentBook()

    i = futures_instrument_book.get_instrument(symbol)
    print(i)

    i = futures_instrument_book.get_instrument_by_id('sc2509')
    print(i)

    r = futures_instrument_book.is_trading_time(symbol)
    print(r)

    symbol = 'CFFEX.IO2504-C-3900'
    options_instrument_book = OptionsInstrumentBook()

    i = options_instrument_book.get_instrument(symbol)
    print(i)

    i = options_instrument_book.get_instrument_by_id('IO2504-C-3900')
    print(i)

    r = options_instrument_book.is_trading_time(symbol)
    print(r)


if __name__ == '__main__':
    test()
