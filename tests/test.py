from qtl_instrument_book import InstrumentBook


def test():
    instrument_book = InstrumentBook()

    i = instrument_book.get_instrument('INE.sc2203')
    print(i)

    i = instrument_book.get_instrument_by_id('sc2203')
    print(i)

    instrument_book.is_trading_time()


if __name__ == '__main__':
    test()
