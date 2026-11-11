import socket
import time
import csv
import concurrent.futures

# Target Load Balancer IP and Port (configured by Person 4)
LB_IP = "10.0.0.4"  
LB_PORT = 5000      

def send_request(client_id):
    start_time = time.time()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((LB_IP, LB_PORT))
        s.sendall(b"GET / HTTP/1.1\r\nHost: loadbalancer\r\n\r\n")
        response = s.recv(1024)
        latency = time.time() - start_time
        s.close()
        return True, latency
    except Exception as e:
        return False, 0.0

def run_load_test(num_requests=100, max_workers=10):
    print(f"[*] Launching {num_requests} requests using {max_workers} concurrent threads...")
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(send_request, i) for i in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            success, latency = future.result()
            results.append((success, latency))

    # Save performance data to a CSV file
    with open('results.csv', mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Success', 'Latency_Seconds'])
        writer.writerows(results)
    print("[+] Load test complete. Results successfully saved to results.csv")

if __name__ == "_main_":
    run_load_test()
