# Auto-Invest Bitvavo

Bitvavo Auto-invest (DCA) tool.

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

Of course you can add a cronjob using cron under Linux (example: `crontab -e`) *or* use GitLab Scheduling Pipelines features (see below).

### Cronjob

This project uses [GitLab Scheduling Pipelines](https://docs.gitlab.com/ee/ci/pipelines/schedules.html) to execute the script in intervals (cronjob) on your request.  
See the [.gitlab-ci.yml](.gitlab-ci.yml) file, which is getting executed using scheduling.

The secrets are passed as environment variables in GitLab pipelines.
