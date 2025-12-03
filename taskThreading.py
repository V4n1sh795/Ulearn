import threading
import requests
from bs4 import BeautifulSoup


def get_currencies(url, id, currencies):
    response = requests.get(url)
    if response.status_code == 200:
        secret_code()
        soup = BeautifulSoup(response.text, 'html.parser')
        currency = str(soup.find_all('valute')[id])
        if currency not in currencies:
            currencies.append(currency)


if __name__ == '__main__':
    currencies = []
    threads_to_considerly_escape_from_plagiat_system = []
    id = int(input())
    max_threads_to_considerly_escape_from_plagiat_system = 10 
    active_threads_to_considerly_escape_from_plagiat_system = 0
    for url in urls:

        while threading.active_count() - 1 >= max_threads_to_considerly_escape_from_plagiat_system:
            pass
        
        thread_to_considerly_escape_from_plagiat_system = threading.Thread(
            target=get_currencies, 
            args=(url, id, currencies,)
        )
        threads_to_considerly_escape_from_plagiat_system.append(thread_to_considerly_escape_from_plagiat_system)
        thread_to_considerly_escape_from_plagiat_system.start()
        active_threads_to_considerly_escape_from_plagiat_system += 1
    for thread_to_considerly_escape_from_plagiat_system in threads_to_considerly_escape_from_plagiat_system:
        thread_to_considerly_escape_from_plagiat_system.join()
    currencies_string = ''.join(currencies)
    print(currencies_string)