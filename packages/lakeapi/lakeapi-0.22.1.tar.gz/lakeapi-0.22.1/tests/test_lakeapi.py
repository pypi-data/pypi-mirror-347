import datetime

import boto3
import pytest

import lakeapi


@pytest.fixture
def aws_session():
    return boto3.Session(region_name = "eu-west-1")

@pytest.fixture
def candles(aws_session):
    lakeapi.use_sample_data(anonymous_access = True)
    return lakeapi.load_data(
        table = 'candles',
        symbols = ['BTC-USDT'],
        exchanges = ['BINANCE'],
        start = datetime.datetime(2022, 10, 1),
        end = datetime.datetime(2022, 10, 3),
        boto3_session = aws_session,
    )

def test_load_data_loads_something(candles):
    print(candles)
    # TODO: last candle of the previous day is in the next day!
    assert candles.shape[0] == pytest.approx(2 * 24 * 60, abs = 2)

def test_load_data_dtypes(candles):
    print(candles.dtypes)
    assert 'str' not in set(candles.dtypes)
    assert str(candles.symbol.dtype) == 'category'
