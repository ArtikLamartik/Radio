import argparse
import requests
import time
import sys

BASE_URL = "https://radio.pythonanywhere.com"

def send_message(thread_key, text):
    url = f"{BASE_URL}/send"
    params = {"key": thread_key}
    payload = {"text": text}
    try:
        resp = requests.post(url, params=params, json=payload, timeout=60)
        if resp.status_code == 200:
            print("Message sent!")
        else:
            print(f"Send failed: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"Error sending: {e}")

def listen_for_messages(thread_key):
    print(f"Listening for new messages in '{thread_key}' (Ctrl+C to stop)...")
    last_time = 0
    while True:
        try:
            url = f"{BASE_URL}/receive"
            params = {"key": thread_key}
            resp = requests.get(url, params=params, timeout=60)
            if resp.status_code == 200:
                message = resp.json()
                if message and last_time != time.localtime(message["timestamp"]):
                    last_time = time.localtime(message["timestamp"])
                    t = time.strftime("%H:%M:%S", time.localtime(message["timestamp"]))
                    print(f"[{t}] {message['text']}")
            elif resp.status_code == 500:
                pass
            else:
                print(f"Server error: {resp.status_code}")
                time.sleep(2)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except requests.exceptions.Timeout:
            continue
        except Exception as e:
            print(f"Connection error: {e}")
            time.sleep(3)

def main():
    parser = argparse.ArgumentParser(description="Radio Messaging Client")
    parser.add_argument("action", choices=["send", "listen"], help="Action to perform")
    parser.add_argument("--key", required=True, help="Thread/chat room key")
    parser.add_argument("--text", help="Message text (for 'send')")
    args = parser.parse_args()
    if args.action == "send":
        if not args.text:
            print("--text is required for 'send'")
            sys.exit(1)
        send_message(args.key, args.text)
    elif args.action == "listen":
        listen_for_messages(args.key)

if __name__ == "__main__":
    main()