#!/usr/bin/env python3
from python_bitvavo_api.bitvavo import Bitvavo
import os
import sys
if 'API_KEY' not in os.environ:
  print('ERROR: Missing \'API_KEY\' environment variable. Exit')
  sys.exit(1)
if 'API_SECRET' not in os.environ:
  print('ERROR: Missing \'API_SECRET\' environment variable. Exit')
  sys.exit(1)

# Settings
MIN_AVAILABLE_EURO = 10.0 # Min amount of euro balance in order to proceed futher
BUY_AMOUNT_EURO = 5.0 # How much do you want to buy (market order)?

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
  response = bitvavo.placeOrder('BTC-EUR', 'buy', 'market', { 'amountQuote': str(BUY_AMOUNT_EURO) })
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