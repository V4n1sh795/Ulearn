import multiprocessing

def process_array(array_2d):
    with multiprocessing.Pool() as pool:
        results = pool.map(worker_function, array_2d)
    
    return sum(results)

def main():
    input_data = input()
    # ['[5 2 8 8 6 7 7 5 6 6]', '[1 8 6 10 1 8 10 4 1 3]', '[3 4 1 6 4 5 4 10 9 9]', '[9 3 7 1 6 8 1 7 1 4]', '[3 4 8 5 2 3 7 1 9 10]', '[4 8 9 9 4 9 9 9 4 7]']
    dwmdwmf = [[int(y) for y in x.replace('[', '').replace(']', '').split()] for x in input_data.replace('[[', '[').replace(']]', ']').split(', ')]

    
    print(process_array(dwmdwmf))

if __name__ == "__main__":
    main()