
import aeon.scripts as scripts
import inspect
from aeon.config import check_config
from aeon.core.llm import LLM

def verify_installation():
    print("Verifying AEON Installation...")
    
    # 1. Config Check
    if check_config():
        print("[PASS] Config loaded (API Keys present).")
    else:
        print("[FAIL] Config missing API Keys.")

    # 2. Script Count
    functions = [o for o in inspect.getmembers(scripts) if inspect.isfunction(o[1])]
    print(f"[INFO] Found {len(functions)} independent automation functions.")
    
    # 3. Import Check
    try:
        print(f"[TEST] Random function check: {scripts.generate_uuid()}")
    except Exception as e:
        print(f"[FAIL] Script execution failed: {e}")

    # 4. LLM Check
    try:
        llm = LLM()
        # response = llm.chat("Hello!") # Skip actual network call to save time/cost if needed, or uncomment
        print(f"[PASS] LLM initialized with model {llm.model}")
    except Exception as e:
        print(f"[FAIL] LLM initialization failed: {e}")

if __name__ == "__main__":
    verify_installation()
