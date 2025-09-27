import asyncio

async def task_a():
    await asyncio.sleep(1)
    return "Result from Task A"

async def task_b():
    await asyncio.sleep(0.5)
    return "Result from Task B"

async def main():
    results = await asyncio.gather(task_a(), task_b())
    print(results)

if __name__ == "__main__":
    asyncio.run(main())