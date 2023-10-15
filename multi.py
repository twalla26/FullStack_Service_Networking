import threading
import time
def hard_work():
    time.sleep(5)
    print("is Finished")

hw = threading.Thread(target=hard_work)
hw.daemon = True
hw.start()

print("[Main] is Done")