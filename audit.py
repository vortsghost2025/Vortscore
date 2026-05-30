import os

print("\n╔══════════════════════════════════════╗")
print("║    VITALIS FSI — SECURITY AUDIT     ║")
print("╚══════════════════════════════════════╝\n")

print("[1] SCANNING FOR EXPOSED SECRETS")
danger = ["api_key", "secret", "password", "token", "sk-", "Bearer"]
found = []
for root, dirs, files in os.walk(os.path.expanduser("~/vitalis_devcore")):
    dirs[:] = [d for d in dirs if d not in ['__pycache__','.git','node_modules']]
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path, 'r', errors='ignore') as fh:
                for i, line in enumerate(fh, 1):
                    for d in danger:
                        if d.lower() in line.lower() and '=' in line and '#' not in line.split('=')[0]:
                            found.append(f"{path}:{i} — {line.strip()[:60]}")
if found:
    for f in found:
        print(f"    [!] {f}")
else:
    print("    [OK] No exposed secrets found")

print("\n[2] SCANNING FOR EXTERNAL NETWORK CALLS")
external = ["requests.get", "requests.post", "urllib", "http.client"]
ext_found = []
for root, dirs, files in os.walk(os.path.expanduser("~/vitalis_devcore/src")):
    dirs[:] = [d for d in dirs if d not in ['__pycache__']]
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path, 'r', errors='ignore') as fh:
                for i, line in enumerate(fh, 1):
                    for e in external:
                        if e in line:
                            ext_found.append(f"{os.path.basename(path)}:{i} — {line.strip()[:60]}")
if ext_found:
    for f in ext_found:
        print(f"    [NOTE] {f}")
else:
    print("    [OK] No unexpected external calls")

print("\n[3] CHECKING SENSITIVE FILE PERMISSIONS")
sensitive = [
    os.path.expanduser("~/.vitalis_workspace/hippocampus.npy"),
    os.path.expanduser("~/.vitalis_workspace/codebook.npy"),
]
for path in sensitive:
    if os.path.exists(path):
        mode = oct(os.stat(path).st_mode)[-3:]
        print(f"    {os.path.basename(path)}: {mode} {'[OK]' if mode in ['600','644'] else '[REVIEW]'}")

print("\n╔══════════════════════════════════════╗")
print("║           AUDIT COMPLETE            ║")
print("╚══════════════════════════════════════╝\n")
