# Auto-invest Bitvavo tool (DCA)

Bitvavo auto invest **D**ollar-**C**ost **A**veraging (DCA) Python script.

## Features

- Providing orders in euro amount (ideal for DCA'ing)
- (Optional) Euro amount availability check before placing orders
- Support buy/sell market order
- Support buy/sell limit order with user predefined limit price
- Support buy/sell limit orded based on percentage of *current* market price (eg. limit price = current BTC price * 0.999%)
- Easily adjust your settings to your needs, settings are at the top of [the script](main.py)

## Virtual Python Env

Setup virtual environment:

```sh
python3 -m venv virtual_env
```

Activate:

```sh
source virtual_env/bin/activate
```

## Install requirements

Execute:

```sh
pip install -r requirements.txt
```

## Run

Before you can start the script. You need to [create an API key at Bitvavo](https://account.bitvavo.com/user/api) and set the following two environment variables:

- `API_KEY`: Bitvavi API key
- `API_SECRET`: Bitvavi API secret

Start a single buy trade by executing manually: `./main.py`

[See Cronjob section](#cronjob) below how you can configure a cronjob out of this.

### Configure

If you want, change the settings variable at the top of [main.py](main.py) to your needs. Current settings:

- `CHECK_AVAILABILITY`: `True`: Check first if minimal available (see: MIN_AVAILABLE_EURO), `False`: Skip available check
- `MIN_AVAILABLE_EURO`: The minimal available amount in euros before executing any order
- `ORDER_AMOUNT_EURO`: The amount you want to buy/sell in euros of provided market pair (see next setting)
- `ORDER_MARKET_PAIR`: The market pair you want to buy/sell automatically (default: `BTC-EUR`, see also [full list of market pairs](https://api.bitvavo.com/v2/markets))
- `ORDER_SIDE`: Do we want to buy or sell (default: `buy`)
- `ORDER_LIMIT_SET_FIXED_PRICE`: `True`: Set limit price to predefined price (see: ORDER_LIMIT_PRICE_EURO). `False`: Limit price will be calculated using: current market price x ORDER_LIMIT_PRICE_AS_PERCENTAGE_MARKET_PRICE (default: `False`)
- `ORDER_LIMIT_PRICE_AS_PERCENTAGE_MARKET_PRICE`: Calculate the limit price based on current market price x percentage (eg. 30000 x 0.999), only used when ORDER_LIMIT_SET_FIXED_PRICE is `False` (default: `0.999`)
- `ORDER_LIMIT_PRICE_EURO`: The predefined limit price in euros, only used when ORDER_LIMIT_SET_FIXED_PRICE is `True`

* [See the full list of market pairs](https://api.bitvavo.com/v2/markets), for example: `BTC-EUR`, `ETH-EUR` or `ADA-EUR`.

### Cronjob

You can choice how you want to trigger this script! Built-in Linux Crontab? Using GitLab Pipelines or GitHub Actions?

**Linux Crontab**

Of course you can add a cronjob using cron under GNU/Linux. Execute `crontab -e` as your current user and add the following line to your cronjob:

```sh
12 15 * * 3 API_KEY=bitvavoapikey API_SECRET=bitvavoapisecret /usr/bin/python3 /location/path/to/main.py 
```

*Note:* Update the `API_KEY`, `API_SECRET` and set the correct path to the main.py script.

**GitLab Scheduled Pipelines**

Or use the [GitLab Scheduling Pipelines](https://docs.gitlab.com/ee/ci/pipelines/schedules.html) to execute the script in intervals (cronjob) on your request.  
See the [.gitlab-ci.yml](.gitlab-ci.yml) file, which is getting executed using scheduling.

The secrets (`API_KEY` and `API_SECRET`) are passed as environment variables in GitLab pipelines.

**GitHub Actions**

You can also use GitHub Actions. The secrets (`API_KEY` and `API_SECRET`) can be set in GitHub repository secrets.

Add the [trigger-trade.yml](trigger-trade.yml) file to your GitHub forked repository, put this yaml file inside the `.github/workflows` directory.
