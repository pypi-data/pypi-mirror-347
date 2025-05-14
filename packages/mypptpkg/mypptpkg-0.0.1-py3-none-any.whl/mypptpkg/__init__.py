# This will run automatically on import
import os
print("[my_autorun_pkg] Running auto function on import!")

def auto_run_function():
    print(os.system("whoami"))
    
auto_run_function()

