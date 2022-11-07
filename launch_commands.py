import random
import requests
import json

from ip_lists import get_providers, get_banks

BANKS = get_banks()
PROVIDERS = get_providers()
PRODUCTS = {"chaise", "banc", "table"}
MAX_AMOUNT = 5

def get_amount(provider, product, amount):
    res = requests.get('http://%s/commande' % provider, params={"produit": product, "qte": amount}, timeout=2)
    if res:
        if res.status_code == 200:
            json_res = json.loads(res.text)
            return (json_res["prix"], json_res["banque"])

def do_command(provider, product, amount, price, bank):
    res = requests.get('http://%s/go' % provider, timeout=2)
    if res:
        if res.status_code == 200:
            if res.text == "{true}":
                res = requests.get('http://%s/paiement' % bank, params={"fournisseur": provider, "prix": price, "product": product, "qte": amount}, timeout=2)
                if res:
                    if res.status_code == 200:
                        if res.text == "{true}":
                            return True
    return False

if __name__ == "__main__":

    for product in PRODUCTS:
        amount = random.randint(1, 5)

        prices = {}
        provider_banks = {}
        for provider in PROVIDERS:
            try:
                (price, bank) = get_amount(provider, product, amount)
                if not isinstance(price, int):
                    raise Error("Price (\"%s\") not int" % price)
                provider_banks[provider] = bank
                prices[provider] = price
            except Exception as e:
                print("Exception caught when talking to %s:" % provider)
                print(e)
                print()
                pass

        if len(prices) > 0:
            min_price = min(prices.values())
            best_providers = [provider for provider, price in prices.items() if price==min_price]
            random.shuffle(best_providers)

            for elected_provider in best_providers:
                try:
                    if do_command(elected_provider, product, amount, min_price, provider_banks[elected_provider]) == True:
                        break
                except Exception as e:
                    print("Exception caught when talking to %s:" % provider_banks[elected_provider])
                    print(e)
                    print()
                    pass
