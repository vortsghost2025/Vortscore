import sys, json, urllib.request
def main():
    prompt = " ".join(sys.argv[1:])
    req = urllib.request.Request("http://localhost:8000/run", data=json.dumps({"prompt": prompt}).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        print(json.load(resp)["reply"])
if __name__ == "__main__": main()
