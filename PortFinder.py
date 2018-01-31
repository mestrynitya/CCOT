import socket
import json
from datetime import datetime
import threading
import Queue

IP_List = 'IPs_LIST.json'
num_worker_threads = 2
q = Queue.Queue()

def Create_Dummy_Data():
    ServerIps = {"192.168.12.14": [], "127.0.0.1": []}
    print len(ServerIps)
    Write_data(ServerIps)


def Write_data(ServerIPs):
    with open(IP_List, 'w') as f:
        json.dump(ServerIPs, f, indent=2)
        f.close()


# Creating dummy data
Create_Dummy_Data()

Server_IPs = json.load(open(IP_List))


def worker():
    while True:
        item = q.get()
        print item
        if item is None:
            break
        Make_connection(item)
        q.task_done()


def Make_connection(IP_Address):
    global lock
    lock.acquire()
    try:
        thread = threading._get_ident()
        print thread
        # IPV = IP_Validate(IP_Address)
        # print "Checking available ports for IP:", IP_Address
        # try:
        #     for Port in range(1, 1025):
        #         if IPV == 'IPV4':
        #             try:
        #                 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #                 result = sock.connect_ex((IP_Address, Port))
        #                 if result != 0:
        #                     print "Available Port :", Port
        #                     Server_IPs[IP_Address].append(Port)
        #                     sock.close()
        #             except Exception as e:
        #                 print(e)
        #         else:
        #             try:
        #                 sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        #                 result = sock.connect_ex((IP_Address, Port))
        #                 if result != 0:
        #                     print "Available Port :", Port
        #                     Server_IPs[IP_Address].append(Port)
        #                     sock.close()
        #             except Exception as e:
        #                 print(e)
        for Port in range(1, 1025):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((IP_Address, Port))
                if result != 0:
                    print "Available Port(s):", Port
                    Server_IPs[IP_Address].append(Port)
                    sock.close()
            except Exception as e:
                print(e)
            except socket.error:
                print "Cannot connect to IP", IP_Address
                sys.exit()
        Write_data(Server_IPs)
    finally:
        lock.release();
    # lock.acquire()
    # try:
    #     Write_data(Server_IPs, Action)
    # finally:
    #     lock.release();


t1 = datetime.now()
# Dict_length = len(Server_IPs)
# spawn a pool of threads, and pass them queue instance
threads = []
for i in range(num_worker_threads):
    lock = threading.Lock()
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)
    print "threads", threads


for IP_Address in Server_IPs:
    print IP_Address
    t1 = datetime.now()
    try:
        q.put(IP_Address)
    except Exception as e:
        print(e)


# block until all tasks are done
q.join()


# stop workers
for i in range(num_worker_threads):
    q.put(None)


t2 = datetime.now()
total = t2 - t1
print 'Scanning Completed in: ', total

