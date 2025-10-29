import cProfile
from functions_to_profile import load_files, read_database, get_id, get_user_data, generate_words
from pstats import Stats

TASK_FUNCTIONS_ORDER = ['load_files', 'read_database', 'get_id', 'get_user_data', 'generate_words']

functions = {
    'load_files': load_files,
    'read_database': read_database,
    'get_id': get_id,
    'get_user_data': get_user_data,
    'generate_words': generate_words,
}

total_time = 0.0
times = {}

for name in TASK_FUNCTIONS_ORDER:
    cProfile.run(name + '()', 'output.prof')
    p = pstats.Stats('output.prof')
    p.strip_dirs().sort_stats('time').print_stats(10)

