import requests
import sys

def make_http_request(ip):
  proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
  response = requests.get(f"http://{ip}", proxies=proxies)
  return response

def make_https_request(ip):
  proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
  response = requests.get(f"https://{ip}", proxies=proxies)
  return response

if __name__ == "__main__":
  for line in sys.stdin:
    ip = line.strip()
    http_response = make_http_request(ip)
    https_response = make_https_request(ip)
    print(f"HTTP response status code for {ip}: {http_response.status_code}")
    print(f"HTTPS response status code for {ip}: {https_response.status_code}")