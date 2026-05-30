import sys, json, urllib.request

def main():
    prompt = " ".join(sys.argv[1:])
    data = json.dumps({"prompt": prompt}).encode()
    req = urllib.request.Request(
        "http://localhost:5001/execute",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        print(json.load(resp))

if __name__ == "__main__":
    main()
