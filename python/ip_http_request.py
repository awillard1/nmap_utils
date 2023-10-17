import signal
import sys
import threading
import socket
import concurrent.futures
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

_proxy = 'http://127.0.0.1:8080'
def signal_handler(signal, frame):
    print("Ctrl-C pressed. Exiting gracefully.")
    sys.exit(0)

def is_port_listening(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect((host, port))
        sock.close()
        return True
    except ConnectionRefusedError:
        return False
    except Exception as e:
        print(e)
        return None

def make_http_request(ip, port, max_retries=1, timeout=4):
    retries = 0
    while retries < max_retries:
        try:
            url = f"http://{ip}:{port}/"
            with requests.Session() as s:
                s.proxies['http'] = _proxy
                s.proxies['https'] = _proxy
                response = s.get(url, verify=False, timeout=timeout)
                return response
        except requests.exceptions.RequestException as e:
            retries += 1
            print(f"Failed to make HTTP request to {ip}:{port}: {e}")

    return None

def make_https_request(ip, port, max_retries=1, timeout=4):
    retries = 0
    while retries < max_retries:
        try:
            url = f"https://{ip}:{port}/"
            with requests.Session() as s:
                s.proxies['http'] = _proxy
                s.proxies['https'] = _proxy
                response = s.get(url, verify=False, timeout=timeout)
                return response
        except requests.exceptions.RequestException as e:
            retries += 1
            print(f"Failed to make HTTPS request to {ip}:{port}: {e}")

    return None

def worker(ip):
    print("testing - " + ip)
    x = ip.split(":")
    if is_port_listening(x[0], int(x[1])):
        http_response = make_http_request(x[0], int(x[1]))
        https_response = make_https_request(x[0], int(x[1]))

        if http_response:
            print(f"HTTP response status code for {ip}: {http_response.status_code}")
        else:
            print(f"Failed to make HTTP request to {ip}")

        if https_response:
            print(f"HTTPS response status code for {ip}: {https_response.status_code}")
        else:
            print(f"Failed to make HTTPS request to {ip}")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    # Create a thread pool with 10 threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Submit tasks to the thread pool
        for line in sys.stdin:
            ip = line.strip()
            executor.submit(worker, ip)
