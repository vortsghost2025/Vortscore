import threading, time, logging
from core.vitalis_brain import VitalisBrain
from src.kernel_interface.procfs_bridge import read_from_kernel

# Route heartbeat to a hidden log file
logging.basicConfig(filename='vitalis.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class VitalisEngine:
    def __init__(self):
        self.brain = VitalisBrain()

    def _heartbeat(self):
        while True:
            system_status = read_from_kernel()
            logging.info(f"System Status: {system_status}")
            time.sleep(2.0)

    def wake_up(self):
        thread = threading.Thread(target=self._heartbeat, daemon=True)
        thread.start()
        print("[+] VitalisEngine heartbeat started (Logging to vitalis.log).")
