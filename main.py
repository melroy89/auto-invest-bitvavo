#!/usr/bin/env python3
from python_bitvavo_api.bitvavo import Bitvavo
import os
import sys
import yaml
try:
  config = yaml.safe_load(open('config.yml'))
except yaml.YAMLError as e:
  print ('ERROR: Could not load config file / could not parse config file:', e)
  sys.exit(1)

# Simple config checks
if 'availability' not in config:
  print ('ERROR: availability is missing from the config.yml file')
if 'order_settings' not in config:
  print ('ERROR: order_settings is missing from the config.yml file')

if 'API_KEY' not in os.environ:
  print('ERROR: Missing \'API_KEY\' environment variable. Exit')
  sys.exit(1)
if 'API_SECRET' not in os.environ:
  print('ERROR: Missing \'API_SECRET\' environment variable. Exit')
  sys.exit(1)

# Configs
CHECK_AVAILABILITY = config['availability']['check_availability']
MIN_AVAILABLE_EURO = config['availability']['min_available_euro']
ORDER_AMOUNT_EURO = config['order_settings']['amount_euro']
ORDER_TYPE_MARKET = config['order_settings']['type_market']
ORDER_MARKET_PAIR = config['order_settings']['market_pair']
ORDER_SIDE = config['order_settings']['side']
ORDER_LIMIT_SET_FIXED_PRICE = config['order_settings']['limit_set_fixed_price']
ORDER_LIMIT_PRICE_AS_PERCENTAGE_MARKET_PRICE = config['order_settings']['limit_price_as_percentage_market_price']
ORDER_LIMIT_PRICE_EURO = config['order_settings']['limit_price_euro']

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
    if 'error' in balanceRes:
      print ('Error: ' + balanceRes['error'])
    else:
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
  print('DEBUG: Remaining rate limit calls for this minute: ' + str(limit))
