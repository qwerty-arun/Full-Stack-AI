import threading
from multiprocessing import Process
import time

# CPU-bound task
def brew_chai(name):
    print(f"{name} started brewing...")
    count = 0
    for _ in range(100_000_000):
        count += 1
    print(f"{name} finished brewing...")

# ----------------------------
# THREADING version
# ----------------------------
def threading_demo():
    thread1 = threading.Thread(target=brew_chai, args=("Masala",))
    thread2 = threading.Thread(target=brew_chai, args=("Oolong",))

    start = time.time()
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    end = time.time()

    print(f"[Threading] Total time: {end - start:.2f} seconds\n")

# ----------------------------
# MULTIPROCESSING version
# ----------------------------
def multiprocessing_demo():
    process1 = Process(target=brew_chai, args=("Masala",))
    process2 = Process(target=brew_chai, args=("Oolong",))

    start = time.time()
    process1.start()
    process2.start()
    process1.join()
    process2.join()
    end = time.time()

    print(f"[Multiprocessing] Total time: {end - start:.2f} seconds\n")

if __name__ == "__main__":
    print("=== THREADING DEMO ===")
    threading_demo()

    print("=== MULTIPROCESSING DEMO ===")
    multiprocessing_demo()
