import threading
import time

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        temp = counter
        time.sleep(0.00001)  # <-- force context switches
        counter = temp + 1

# use lock

# def increment():
#     global counter
#     for _ in range(100000):
#         with lock:
#             counter += 1

# lock + sleep (terrible idea)

def increment():
    global counter
    for _ in range(100000):
        with lock:
            temp = counter
            time.sleep(0.00001)  # simulate context switch
            counter = temp + 1


threads = []
start = time.time()
for _ in range(10):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end = time.time()
print(f"Total time taken: {end-start:.2f} seconds\n")

print(f"Final counter (no lock, with sleep): {counter}")
