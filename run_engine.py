#!/usr/bin/env python3
import time
from src.comm.channel import channel
from src.loop.self_healing import SelfHealingLoop
from src.core.watchdog import Watchdog

def main():
    print("[SYSTEM] Starting Vitalis Synthetic Neural-Flow Engine...")
    
    # Initialize Core Systems
    loop = SelfHealingLoop()
    watchdog = Watchdog()
    
    # Start the continuous loop
    try:
        while True:
            watchdog.monitor()
            loop.run()
            time.sleep(1)
    except KeyboardInterrupt:
        print("[SYSTEM] Vitalis Engine Halted by Operator.")

if __name__ == "__main__":
    main()
