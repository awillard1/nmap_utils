import signal
import requests
import sys

def signal_handler(signal, frame):
  raise KeyboardInterrupt()

def make_http_request(ip, max_retries=3):
  retries = 0
  while retries < max_retries:
    try:
      response = requests.get(f"http://{ip}")
      return response
    except Exception as e:
      retries += 1
      print(f"Failed to make HTTP request to {ip}: {e}")

  return None

def make_https_request(ip, max_retries=3):
  retries = 0
  while retries < max_retries:
    try:
      response = requests.get(f"https://{ip}")
      return response
    except Exception as e:
      retries += 1
      print(f"Failed to make HTTPS request to {ip}: {e}")

  return None

if __name__ == "__main__":
  signal.signal(signal.SIGINT, signal_handler)

  for line in sys.stdin:
    ip = line.strip()

    http_response = make_http_request(ip)
    https_response = make_https_request(ip)

    if http_response:
      print(f"HTTP response status code for {ip}: {http_response.status_code}")
    else:
      print(f"Failed to make HTTP request to {ip}")

    if https_response:
      print(f"HTTPS response status code for {ip}: {https_response.status_code}")
    else:
      print(f"Failed to make HTTPS request to {ip}")
