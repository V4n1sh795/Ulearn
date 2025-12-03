import asyncio

async def main(filenames):
    tasks_to_considerly_escape_from_plagiat_system = []
    for filename in filenames:
        task_to_considerly_escape_from_plagiat_system = asyncio.create_task(read_file_async(filename))
        tasks_to_considerly_escape_from_plagiat_system.append(task_to_considerly_escape_from_plagiat_system)
    
    names_to_considerly_escape_from_plagiat_system = await asyncio.gather(*tasks_to_considerly_escape_from_plagiat_system)
    
    names_str_to_considerly_escape_from_plagiat_system = ' '.join(name for name in names_to_considerly_escape_from_plagiat_system)
    return names_str_to_considerly_escape_from_plagiat_system