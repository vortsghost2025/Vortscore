import time
from src.kernel_interface.procfs_bridge import send_to_kernel, read_from_kernel
from src.senses.sigint_processor import SIGINTProcessor
from src.cognition.synthesizer import DataSynthesizer
from src.cognition.memory import MemoryBank
from src.cognition.action_engine import ActionEngine

def main_loop():
    senses = SIGINTProcessor()
    mind = DataSynthesizer()
    memory = MemoryBank()
    actions = ActionEngine()
    
    while True:
        system_status = read_from_kernel()
        raw_signal = senses.listen_to_traffic()
        
        try:
            byte_count = int(raw_signal.split()[-2]) if "bytes" in raw_signal else 0
        except:
            byte_count = 0
            
        interpretation = mind.categorize_signal(byte_count)
        action_taken = actions.execute(interpretation)
        
        memory.record("PULSE_2.0", raw_signal, interpretation)
        
        state_report = f"SYS: {system_status} | INT: {interpretation} | {action_taken}"
        send_to_kernel(state_report)
        print(f"Broadcast: {state_report}")
        time.sleep(1.0)

if __name__ == '__main__':
    main_loop()
