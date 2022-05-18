#!/usr/bin/env python3
from python_bitvavo_api.bitvavo import Bitvavo
import os
import sys

# Settings
MIN_AVAILABLE_EURO = 10.0 # Min amount of euro balance in order to proceed futher
BUY_AMOUNT_EURO = 5.0 # How much do you want to buy in euros (market order)?
ORDER_MARKET_PAIR = 'BTC-EUR' # What trading pair to buy (Bitcoin/euro is the default), full list of markets: https://api.bitvavo.com/v2/markets
ORDER_SIDE = 'buy' # Buy or sell?
ORDER_TYPE = 'market' # Order type: market (= current best price)

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
  print('INFO: Place BTC buy trade')
  # Buy BTC-EUR at market price based on quote currency (=euro)
  response = bitvavo.placeOrder(ORDER_MARKET_PAIR, ORDER_SIDE, ORDER_TYPE, { 'amountQuote': str(BUY_AMOUNT_EURO) })
  # Order successfully placed?
  if 'orderId' in response:
    print('INFO: Order is successfully placed!')
  elif 'error' in response:
    print('ERROR: Order could not be placed. Error message: ' + str(response['error']))
  else:
    print('ERROR: Order could not be placed. Unknown error.')
    print(response)

if __name__ == "__main__":
  # Retrieve current euro fiat balance first
  balanceRes = bitvavo.balance({ 'symbol': 'EUR'})
  if len(balanceRes) >= 1:
    euroBalance = balanceRes[0]
    euroAvailable = euroBalance['available']
    # We want at least x euros available
    if float(euroAvailable) >= MIN_AVAILABLE_EURO:
      # Start buying
      placeMarketOrder()
    else:
      print('WARNING: Not enough balance (minimum amount should be ' + str(MIN_AVAILABLE_EURO) + ' euros).')
  else:
    print('ERROR: Could not retrieve euro balance!?')