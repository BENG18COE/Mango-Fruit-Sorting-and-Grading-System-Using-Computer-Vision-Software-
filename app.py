import subprocess
from threading import Thread

def run_inference():
    command = "python detect.py --source 0 --weights grading_best.pt --imgsz 416"
    process = subprocess.Popen(command, stdout=subprocess.PIPE,  stderr=subprocess.STDOUT, encoding='utf-8', universal_newlines=True)
    while True:
        realtime_output = process.stdout.readline()
        if realtime_output != '':
            print(realtime_output)

if __name__ == "__main__":
    inference = Thread(target=run_inference)
    inference.start()
    # inference.join()