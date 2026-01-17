import subprocess
import sys


print(sys.executable)

if __name__ == "__main__":
    p1 = subprocess.Popen([sys.executable, "-m", "backend.speech.listening"])
    p2 = subprocess.Popen([sys.executable, "-m", "backend.vision.visionwithgem"])

    p1.wait()
    p2.wait()

    while True:
        key = input("Press q to quit: ")
        if key.lower() == "q":
            p1.terminate()
            p2.terminate()
            p1.wait()
            p2.wait()
            break
