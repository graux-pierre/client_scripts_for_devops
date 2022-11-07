import requests
import json

from collections import defaultdict

from ip_lists import get_providers, get_banks

BANKS = get_banks()
PROVIDERS = get_providers()

def get_balance(bank):
    res = requests.get('http://%s/extraction' % bank, timeout=2)
    if res:
        if res.status_code == 200:
             return json.loads(res.text)

balances = defaultdict(int)
for bank in BANKS:
    try:
        json_balance = get_balance(bank)
        for provider in PROVIDERS:
            balance = json_balance[provider]["compte"]
            if isinstance(balance, int):
                balances[provider] += balance
    except Exception as e:
        print("Exception caught when talking to %s:" % bank)
        print(e)
        pass

for provider in PROVIDERS:
    print("%s\t%s" % (provider, balances[provider]))
