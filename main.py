from requests import get
from pprint import PrettyPrinter

BASE_URL = "https://api.currencyapi.com/v3/"
API_KEY = "fca_live_4iqv73NgkSxr1rB4elYXilYp5PghMl8Eeg8MsYvV"

printer = PrettyPrinter()

def get_currencies():
    endpoint = f"currencies?apikey={API_KEY}"
    url = BASE_URL + endpoint
    response = get(url)
    data = response.json()
    
    # Assuming 'data' contains the currency information
    currencies = data.get('data', {})
    
    # Convert to list and sort
    currencies_list = list(currencies.items())
    currencies_list.sort()

    return currencies_list

def print_currencies(currencies):
    for _id, currency in currencies:
        name = currency['name']
        symbol = currency.get("symbol_native", "")
        print(f"{_id} - {name} - {symbol}")

def exchange_rate(currency1, currency2):
    endpoint = f"convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json()

    if len(data) == 0:
        print('Invalid currencies.')
        return

    rate = list(data.values())[0]
    print(f"{currency1} -> {currency2} = {rate}")

    return rate

def convert(currency1, currency2, amount):
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        return

    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount.")
        return

    converted_amount = rate * amount
    print(f"{amount} {currency1} is equal to {converted_amount} {currency2}")
    return converted_amount

def main():
    currencies = get_currencies()

    print("Welcome to the currency converter!")
    print("List - lists the different currencies")
    print("Convert - convert from one currency to another")
    print("Rate - get the exchange rate of two currencies")
    print()

    while True:
        command = input("Enter a command (q to quit): ").lower()

        if command == "q":
            break
        elif command == "list":
            print_currencies(currencies)
        elif command == "convert":
            currency1 = input("Enter a base currency: ").upper()
            amount = input(f"Enter an amount in {currency1}: ")
            currency2 = input("Enter a currency to convert to: ").upper()
            convert(currency1, currency2, amount)
        elif command == "rate":
            currency1 = input("Enter a base currency: ").upper()
            currency2 = input("Enter a currency to convert to: ").upper()
            exchange_rate(currency1, currency2)
        else:
            print("Unrecognized command!")

main()
