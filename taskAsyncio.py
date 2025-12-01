import asyncio

async def main(filenames):
    tasks = []
    for filename in filenames:
        task = asyncio.create_task(read_file_async(filename))
        tasks.append(task)
    
    names = await asyncio.gather(*tasks)
    
    names_str = ' '.join(name for name in names)
    return names_str