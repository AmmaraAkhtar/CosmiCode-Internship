import asyncio


async def fetch_data():
    print("Fetching data...")
    await asyncio.sleep(2)   
    print("Data fetched!")
    return {"id": 1, "name": "Ali"}


async def process_data():
    print("Processing data...")
    await asyncio.sleep(3)   
    print("Data processed!")
    return True


async def main():
    
    results = await asyncio.gather(
        fetch_data(),
        process_data()
    )
    print("Results:", results)


asyncio.run(main())
