
import os, sys  
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.add_dll_directory(os.path.join(f"{root}"))
