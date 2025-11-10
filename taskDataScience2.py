import pandas as pd
import sys
from collections import Counter



def main(vacancy, ascending, file_path, re):
    def check_list_lenght(l1, l2, l3):
        l1 = l1
        l2 = list(l2)
        l3 = list(l3)
        if len(l1) - len(l2) > 0:
            for i in range(len(l1) - len(2)):
                l1.append('NaN')
        else:
            for i in range(len(l2) - len(l1)):
                l2.append('NaN')
                l3.append('NaN')
        return l1, l2, l3
    vacancies = pd.read_csv(file_path)
    ascending = True if ascending == 'asc' else False

    mask = vacancies['name'].str.contains(vacancy, case=False, na=False)
    result = [str.split(re) for str in vacancies[mask]['key_skills'].dropna().tolist()]
    
    to_counter = []
    for elem0 in result:
        for elem1 in elem0:
            to_counter.append(elem1)

    to_sort_by_place = []
    for str in vacancies[mask]['key_skills'].dropna().tolist():
        for elem in str.split(re):
            to_sort_by_place.append(elem)
    
    result = Counter(to_counter)
    sorted_skills = dict(sorted(
        result.items(),
        key=lambda x: x[1],
        reverse= True 
    )[:5])
  
    not_to_remove = [item[0] for item in sorted_skills.items()]
    to_sort_by_place = [x for x in to_sort_by_place if x in not_to_remove]
    to_sort_by_place = list(dict.fromkeys(to_sort_by_place))
    to_sort_by_place, sorted_skills_keys, sorted_skills_values = check_list_lenght(to_sort_by_place, 
                                            sorted_skills.keys(), 
                                            sorted_skills.values()
                                            )
    df = pd.DataFrame({'pos': to_sort_by_place, 'skill': sorted_skills_keys, 'nums': sorted_skills_values})
    # print(to_sort_by_place)        
    # print(sorted_skills.keys())

    df = df.reset_index().sort_values(
        by=['nums', 'index'],
        ascending=[not ascending, False]
    )

    df = (df
          .drop(columns='pos')
          .drop(columns='index')
          )
    result = list(zip(df['skill'], df['nums']))
    print(result[::-1])
def test():
    main('программист', 'asc', r'test/vacancies_small.csv', '\r\n')
try:
    if sys.argv[1] == 'test':
        test() 
except IndexError:
    key = input()
    ascending = input()
    main(key, ascending, 'vacancies_small.csv', '\n')