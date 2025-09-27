# Projects to work on

---

## **1. Multithreading in Python**

**Use case:** Useful when your program is **I/O-bound** (like file reading/writing, network requests), because threads can run concurrently even with Python’s GIL.

### **Example Projects**

- [ ] **Web Scraper with Multiple Threads**

  - Download multiple webpages concurrently using `threading.Thread`.
  - Use `queue.Queue` to manage URLs to visit.

- [ ] **Chat Server**

  - A simple TCP chat server where each client connection is handled by a separate thread.

- [ ] **Image Downloader**

  - Download hundreds of images from URLs concurrently using threads.

- [ ] **Log Monitoring Tool**

  - Monitor multiple log files in real-time and print new entries.

### **Practice Problems**

- [ ] Implement a **multi-threaded file search**: given a folder, search for a string in all text files concurrently.
- [ ] Write a **multi-threaded downloader** for a list of URLs, storing each page in a separate file.
- [ ] Create a **threaded producer-consumer system** using a `Queue` where one thread produces numbers and others consume and compute factorials.

---

## **2. Multiprocessing in Python**

**Use case:** Best for **CPU-bound tasks** (like heavy computations, data processing) because each process has its **own Python interpreter**, bypassing the GIL.

### **Example Projects**

- [ ] **Parallel Matrix Multiplication**

  - Split matrix rows/columns among multiple processes.

- [ ] **Image Processing Pipeline**

  - Apply filters (blur, edge detection) to multiple images concurrently.

- [ ] **Parallel Web Scraper with CPU-bound Data Processing**

  - Scrape data and process it (e.g., compute statistics) using `multiprocessing.Pool`.

- [ ] **Simulation or Monte Carlo Computation**

  - Run many simulations in parallel to calculate probabilities or statistics.

### **Practice Problems**

- [ ] Write a program to **calculate prime numbers** between 1 and N using multiple processes.
- [ ] Implement a **multiprocessing version of Fibonacci calculation** where each Fibonacci number is computed in a separate process.
- [ ] Write a program that **counts word frequency** in a large text file using multiple processes, splitting the file into chunks.

---

## **3. Understanding GIL (Global Interpreter Lock)**

- Python’s GIL allows only **one thread to execute Python bytecode at a time**.
- Multithreading doesn’t speed up CPU-bound tasks in CPython because of the GIL.
- Multiprocessing or using libraries that release GIL (like `numpy`) are better for CPU-bound tasks.

### **Example Projects**

- [ ] **Benchmarking CPU-bound vs I/O-bound tasks**

   - Compute factorial of large numbers in threads vs processes and compare speed.

- [ ] **Threaded vs Multiprocessing Image Filter**

   - Apply a CPU-intensive filter using threads and processes and compare execution time.

- [ ] **Simulate GIL Locking**

   - Have multiple threads increment a shared counter in Python; measure time vs using `multiprocessing.Value`.

### **Practice Problems**

- [ ] Create a **threaded vs process-based counter** and observe GIL’s effect.
- [ ] Compare performance of **threaded vs process-based prime number computation**.
- [ ] Use `concurrent.futures` to implement both **ThreadPoolExecutor** and **ProcessPoolExecutor** for a CPU-heavy function and analyze speed difference.

---

✅ **Tips for Practicing**

- Start with small scripts (e.g., 2–4 threads/processes), then scale up to dozens.
- Use `time.time()` to measure execution time for threads vs processes.
- Try combining **I/O-bound and CPU-bound tasks** to see which concurrency method is better.

---
