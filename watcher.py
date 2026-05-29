import time, os
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler
from src.core.watchdog import update_manifest

class VaultHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".txt"):
            print(f"[*] Change detected in {event.src_path}. Re-signing manifest...")
            update_manifest()
            
            print("[*] Allocating MemoryEngine for Hot-Ingestion...")
            # Lazy-load to prevent dual-VRAM exhaustion on startup
            from src.core.memory_engine import MemoryEngine
            engine = MemoryEngine()
            engine.ingest_knowledge()
            print("[+] Hot-ingestion complete. System secure.")

if __name__ == "__main__":
    if not os.path.exists("storage/knowledge/manifest.sha256"):
        update_manifest()
    
    observer = Observer()
    observer.schedule(VaultHandler(), path='storage/knowledge', recursive=False)
    observer.start()
    print("[*] FSI Hot-Ingestion Daemon Active. Watching storage/knowledge (Polling Mode)...")
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
