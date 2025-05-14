from clients.client import ELFiClient
from clients.utils import to_address, multi_pow10
from clients.keys import OrderSide
from time import sleep

PRIVATE_KEY = ''
elfiClient = ELFiClient(PRIVATE_KEY)

# ------ deposit ------

# deposit 100USDC
USDC = to_address("0xaf88d065e77c8cC2239327C5EDb3A432268e5831")
depositAmount = multi_pow10(100, elfiClient.token_decimals(USDC))
elfiClient.deposit(USDC, depositAmount)

# withdraw
# elfiClient.withdraw(USDC, depositAmount)

# ------ open & close long crossed position ------
print("open & close long crossed position")

# place long crossed order with 50 USD
longOrderMargin = multi_pow10(50, 18)

# 10x leverage
leverage = multi_pow10(10, 5)

WBTC = to_address(elfiClient.get_symbol('BTCUSD')[4])

# open long crossed position
elfiClient.create_increase_market_order('BTCUSD', WBTC, OrderSide.LONG, longOrderMargin, leverage, True)

sleep(5)

# get long crossed position
longPosition = elfiClient.get_single_position('BTCUSD', WBTC, True)

print(longPosition)

# close long crossed position
elfiClient.create_decrease_market_order('BTCUSD', WBTC, OrderSide.SHORT, longPosition[7], True)

# ------ open & close short crossed position ------

print("open & close short crossed position")

# place short crossed order with 50 USD
shortOrderMargin = multi_pow10(50, 18)

# 10x leverage
leverage = multi_pow10(10, 5)

# open short crossed position
elfiClient.create_increase_market_order('BTCUSD', USDC, OrderSide.SHORT, shortOrderMargin, leverage, True)

sleep(5)

# get short crossed position
shortPosition = elfiClient.get_single_position('BTCUSD', USDC, True)

print(shortPosition)

# close short crossed position
elfiClient.create_decrease_market_order('BTCUSD', USDC, OrderSide.LONG, shortPosition[7], True)

