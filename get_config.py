from requests import get as rget
from init import LOGGER
import os
import subprocess
from dotenv import load_dotenv

try:
    CONFIG_FILE_URL = os.environ.get('CONFIG_FILE_URL', '')
    if len(CONFIG_FILE_URL) == 0:
        raise ValueError("CONFIG_FILE_URL environment variable is empty")

    res = rget(CONFIG_FILE_URL)
    if res.status_code == 200:
        with open('config.env', 'wb') as f:
            f.write(res.content)
    else:
        LOGGER.error(f"Failed to download config.env. Status code: {res.status_code}")

except Exception as e:
    LOGGER.error(f"Error occurred while processing CONFIG_FILE_URL: {e}")

try:
    load_dotenv("config.env", override=True)

    UPSTREAM_REPO = os.environ.get('UPSTREAM_REPO', '') or None
    UPSTREAM_BRANCH = os.environ.get('UPSTREAM_BRANCH', '') or 'master'

    if UPSTREAM_REPO:
        if os.path.exists('.git'):
            subprocess.run(["rm", "-rf", ".git"])

        update = subprocess.run(f'''
            git init -q &&
            git config --global user.email yashoswal18@gmail.com &&
            git config --global user.name mergebot &&
            git add . &&
            git commit -sm update -q &&
            git remote add origin {UPSTREAM_REPO} &&
            git fetch origin -q &&
            git reset --hard origin/{UPSTREAM_BRANCH} -q
        ''', shell=True)

        if update.returncode == 0:
            LOGGER.info('Successfully updated with the latest commit from UPSTREAM_REPO')
        else:
            LOGGER.warning('Something went wrong while updating. Please check UPSTREAM_REPO for validity.')

except Exception as e:
    LOGGER.error(f"An error occurred: {e}")

