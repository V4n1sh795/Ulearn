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
    threads = []
    id = int(input())
    max_threads = 10 
    active_threads = 0
    for url in urls:

        while threading.active_count() - 1 >= max_threads:
            pass
        
        thread = threading.Thread(
            target=get_currencies, 
            args=(url, id, currencies,)
        )
        threads.append(thread)
        thread.start()
        active_threads += 1
    for thread in threads:
        thread.join()
    currencies_string = ''.join(currencies)
    print(currencies_string)