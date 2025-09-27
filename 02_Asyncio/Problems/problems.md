# Practice Problems for Asyncio

## **Beginner Level**

- [ ] **Hello Async World**

  - Write a simple coroutine that prints “Hello” after 1 second and “World” after 2 seconds using `asyncio.sleep`.
  - Run it using `asyncio.run()`.

- [ ] **Concurrent Greetings**

  - Create three coroutines that print different greetings (`Hi`, `Hello`, `Hey`) after random delays.
  - Run them concurrently using `asyncio.gather()`.

- [ ] **Async Countdown**

  - Write a coroutine that counts down from 5 to 1 with a 1-second delay between numbers.
  - Launch multiple countdowns concurrently.

- [ ] **Async Timer**

  - Write a coroutine that takes a function and a delay as arguments and executes the function after the delay asynchronously.

---

## **Intermediate Level**

- [ ] **Fetching URLs**

  - Use `aiohttp` (or `httpx`) to fetch multiple URLs concurrently.
  - Print the HTTP status code of each response.

- [ ] **Producer-Consumer**

  - Implement a producer coroutine that produces numbers and puts them in an `asyncio.Queue`.
  - Implement a consumer coroutine that consumes numbers from the queue and prints them.

- [ ] **Async File Reader**

  - Write a coroutine to read multiple files concurrently and print the first line of each.
  - Use `aiofiles` library for asynchronous file operations.

- [ ] **Async Calculator**

  - Write coroutines for `add`, `subtract`, `multiply`, `divide`.
  - Execute a batch of math operations concurrently.

- [ ] **Retry with Async**

  - Write a coroutine that tries to fetch a URL but retries up to 3 times if it fails.
  - Use `asyncio.sleep` for delay between retries.

---

## **Advanced Level**

- [ ] **Async Web Scraper**

    - Crawl multiple pages concurrently and extract titles or headings.
    - Use `aiohttp` + `BeautifulSoup` + `asyncio.gather()`.

- [ ] **Rate-limited Tasks**

    - Schedule 100 coroutines but allow only 5 to run concurrently at any time.
    - Use `asyncio.Semaphore` for concurrency control.

- [ ] **Async Timeout**

    - Run a coroutine that may take a long time.
    - Cancel it if it exceeds a timeout using `asyncio.wait_for()`.

- [ ] **Async Chat Simulation**

    - Simulate a chatroom with multiple users sending messages asynchronously.
    - Use `asyncio.Queue` to handle messages.

- [ ] **Async Pipeline**

    - Create a pipeline of coroutines: Fetch → Process → Save.
    - Each stage should run concurrently, passing results via `asyncio.Queue`.

- [ ] **Parallel CPU-bound Simulation**

    - Show the difference between CPU-bound tasks using `asyncio` vs `concurrent.futures.ProcessPoolExecutor`.
    - For example, calculating Fibonacci numbers for multiple inputs.
---
