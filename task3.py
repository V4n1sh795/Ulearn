import re
import csv

input_csv = input()
new_file = input()
key_words = input().split(',')

def first_step(text):
    result = re.sub(r'<[^>]*>', '', text)
    result = re.sub(r'(\d{4})-(\d{2})-(\d{2})T(\d{2})[.:](\d{2}):(\d{2})\+\d{4}', r'\4:\5:\6 \3/\2/\1', result)
    result = re.sub(r'(?<=\s)(\d{2})\.(\d{2})(?=\s)', r'\1:\2', result)
    result = re.sub(r'(?<=^)(\d{2})\.(\d{2})(?=\s)', r'\1:\2', result)
    result = re.sub(r'(?<=\s)(\d{2})\.(\d{2})(?=$)', r'\1:\2', result) 
    return result

def highlight_keywords(text, keywords):
    def replace_func(match):
        word = match.group(0)
        for keyword in keywords:
            if keyword.lower() in word.lower():
                return word.upper()
        return word
    return re.sub(r'\b\w+[\'\w]*\b', replace_func, text)

with open(input_csv, 'r', encoding='utf-8') as inp, open(new_file, 'w', encoding='utf-8', newline='') as out:
    reader = csv.reader(inp)
    writer = csv.writer(out)    
    
    for row in reader:
        processed_row = []
        for cell in row:
            result = first_step(cell)
            result = highlight_keywords(result, key_words)
            processed_row.append(result)
        
        writer.writerow(processed_row)
