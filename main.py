#!/usr/bin/env python3
from python_bitvavo_api.bitvavo import Bitvavo
import os
import sys

# General Settings
CHECK_AVAILABILITY = True # True = Execute the availablity check (see: MIN_AVAILABLE_EURO), False = if you want to execute others _without_ checking the euro balance.
MIN_AVAILABLE_EURO = 10.0 # Min amount of euro balance in order to proceed futher
ORDER_AMOUNT_EURO = 5.0 # The order buy (or sell) amount in euros (used for market orders and used as base price for limit orders)
ORDER_TYPE_MARKET = False # True = Market order (= current price), False = Limit order (see specific limit order settings below)
ORDER_MARKET_PAIR = 'BTC-EUR' # The trading pair to buy/sell (Bitcoin/euro is the default), full list of markets: https://api.bitvavo.com/v2/markets
ORDER_SIDE = 'buy' # Buy or sell?
# Specific limit order settings
ORDER_LIMIT_SET_FIXED_PRICE = False # True = Set your own predefined limit price (see: ORDER_LIMIT_PRICE_EURO), False = Limit price will be calculated based on: current market price x ORDER_LIMIT_PRICE_AS_PERCENTAGE_MARKET_PRICE (otherwise not used)
ORDER_LIMIT_PRICE_AS_PERCENTAGE_MARKET_PRICE = 0.999 # We set the limit price to 0.999% of the _current_ market price (eg. current bitcoin price x percentage), only used when ORDER_LIMIT_SET_FIXED_PRICE set to False
ORDER_LIMIT_PRICE_EURO = 0 # The predefined limit order price in euros, only used when ORDER_LIMIT_SET_FIXED_PRICE is set to True (otherwise not used)

if 'API_KEY' not in os.environ:
  print('ERROR: Missing \'API_KEY\' environment variable. Exit')
  sys.exit(1)
if 'API_SECRET' not in os.environ:
  print('ERROR: Missing \'API_SECRET\' environment variable. Exit')
  sys.exit(1)

# Setup connection
bitvavo = Bitvavo({
  'APIKEY': os.environ['API_KEY'],
  'APISECRET': os.environ['API_SECRET']
})

# Placing order helper function
def placeMarketOrder():
  global bitvavo 
  orderResponse = None
  if ORDER_TYPE_MARKET:
    # Order type = market order
    # Place buy/sell market order with quote currency as amountQuote (= euro)
    print('INFO: Placing market ' + ORDER_MARKET_PAIR + ' ' + ORDER_SIDE + ' order. With quote amount: ' + str(ORDER_AMOUNT_EURO) + ' euros')
    orderResponse = bitvavo.placeOrder(ORDER_MARKET_PAIR, ORDER_SIDE, 'market', { 'amountQuote': str(ORDER_AMOUNT_EURO) })
  else:
      # Order type = limit order, we first need to retrieve the current ticker price of the market pair
      priceResponse = bitvavo.tickerPrice({ 'market': ORDER_MARKET_PAIR })
      if 'price' in priceResponse:
        # Calculate the amount (eg. bitcoin amount) based on the amount requsted in euros
        euroTickerMarketPrice = float(priceResponse['price'])
        amount = (1.0 / euroTickerMarketPrice) * ORDER_AMOUNT_EURO
        # Round the amount to 8 decimal places (for Bitcoin)
        amountString = "{0:.8f}".format(amount)
        if ORDER_LIMIT_SET_FIXED_PRICE:
          # Place buy/sell limit order with predefined limit price
          print('INFO: Placing limit ' + ORDER_MARKET_PAIR + ' ' + ORDER_SIDE + ' order. With amount: ' + amountString + ' and predefined limit price: ' + str(ORDER_LIMIT_PRICE_EURO) + ' euros')
          orderResponse = bitvavo.placeOrder(ORDER_MARKET_PAIR, ORDER_SIDE, 'limit', { 'amount': amountString, 'price': str(ORDER_LIMIT_PRICE_EURO) })
        else:
          # Calculate the limit price based on the market price x percentage
          limitPrice = euroTickerMarketPrice * ORDER_LIMIT_PRICE_AS_PERCENTAGE_MARKET_PRICE
          # Bitcoin wants to limit the price to a precision of 5 (which currently means no decimal points)
          limitPrice = round(limitPrice)
          # Place buy/sell limit order with calculated limit price (see one line above)
          print('INFO: Placing limit ' + ORDER_MARKET_PAIR + ' ' + ORDER_SIDE + ' order. With amount: ' + amountString + ' and limit price: ' + str(limitPrice) + ' euros (' + str(ORDER_LIMIT_PRICE_AS_PERCENTAGE_MARKET_PRICE) + '% of '+  str(euroTickerMarketPrice) + ' euro price)')
          orderResponse = bitvavo.placeOrder(ORDER_MARKET_PAIR, ORDER_SIDE, 'limit', { 'amount': amountString, 'price': str(limitPrice) })
      else:
        print('ERROR: Could not retrieve current market price for ' + ORDER_MARKET_PAIR + '. Required for limit order calculations.')

  # Order successfully placed?
  if orderResponse is None:
    print('ERROR: Order is not executed. Something went wrong before that.')
  elif 'orderId' in orderResponse:
    print('INFO: Order is successfully placed!')
  elif 'error' in orderResponse:
    print('ERROR: Order could not be placed. Error message: ' + str(orderResponse['error']))
  else:
    print('ERROR: Order could not be placed. Unknown error.')
    print(orderResponse)

if __name__ == "__main__":
  if CHECK_AVAILABILITY:
    # Retrieve current euro fiat balance first
    balanceRes = bitvavo.balance({ 'symbol': 'EUR'})
    if len(balanceRes) >= 1:
      euroBalance = balanceRes[0]
      euroAvailable = euroBalance['available']
      # We want at least x euros available
      if float(euroAvailable) >= MIN_AVAILABLE_EURO:
        # Start buying/selling
        placeMarketOrder()
      else:
        print('WARNING: Not enough balance (minimum amount should be ' + str(MIN_AVAILABLE_EURO) + ' euros).')
    else:
      print('ERROR: Could not retrieve euro balance!?')
  else:
    # Start buying/selling
    placeMarketOrder()

  # Display rate limit info, in all cases
  limit = bitvavo.getRemainingLimit()
  print('INFO: Remaining rate limit calls for this minute: ' + str(limit))