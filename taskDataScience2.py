import pandas as pd
import sys
from collections import Counter

def main(vacancy, ascending, file_path):
    vacancies = pd.read_csv(file_path)
    ascending = True if ascending == 'asc' else False

    mask = vacancies['name'].str.contains(vacancy, case=False, na=False)
    result = [str.split('\n') for str in vacancies[mask]['key_skills'].dropna().tolist()]
    to_counter = []
    for elem0 in result:
        for elem1 in elem0:
            to_counter.append(elem1)
    result = Counter(to_counter)
    sorted_skills = sorted(
        result.items(),
        key=lambda x: x[1],    
        reverse=ascending    
    )    
    rev = reversed(sorted_skills[:5])
    print(list(rev))                  
def test():
    assert main('программист', 'asc', r'test/vacancies_small.csv')
try:
    if sys.argv[1] == 'test':
        test() 
except IndexError:
    key = input()
    ascending = input()
    main(key, ascending, 'vacancies_small.csv')