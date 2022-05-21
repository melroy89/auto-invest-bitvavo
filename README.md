# Auto-invest Bitvavo tool (DCA)

Bitvavo auto invest **D**ollar-**C**ost **A**veraging (DCA) Python script.

## Features

- Providing orders in euro amount (ideal for DCA'ing)
- Easily change your configuration by adapting the [config.yml](config.yml) file
- (Optional) Euro amount availability check before placing orders
- Support buy/sell market order
- Support buy/sell limit order with user predefined limit price
- Support buy/sell limit orded based on percentage of *current* market price (eg. limit price = current BTC price * defined percentage)
- Example setups provided from Crontab, GitLab Pipeline or GitHub Actions

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

You can adapt the settings in the [config.yml](config.yml) file which is using YAML syntax, so **NO** source file changes are needed. Be sure you also set the `API_KEY` and `API_SECRET` environment variables mentioned above.

*Note:* [See the full list of market pairs at Bitvavo](https://api.bitvavo.com/v2/markets), for example: `BTC-EUR`, `ETH-EUR` or `ADA-EUR`.

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

Add the [github-action-trigger-trade.yml](github-action-trigger-trade.yml) file to your GitHub forked repository, put this yaml file inside the `.github/workflows` directory.
