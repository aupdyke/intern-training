from scapy.all import ARP, Ether, srp
import numpy as np
import cv2 as cv

target_ip = "192.168.30.1/24"

phone_mac = ("1A:E0:B7:ED:1D:52").lower()

arp = ARP(pdst=target_ip)
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
packet = ether / arp
result = srp(packet, timeout=3, verbose=0)[0]

clients = []

found = False

for sent, received in result:
    if received.hwsrc.lower() == phone_mac:
        print(f"Found phone with IP: {received.psrc} and MAC: {received.hwsrc}")
        found = True

    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

print("Available devices in the network:")
print("IP" + " " * 18 + "MAC")
for client in clients:
    print("{:16}    {}".format(client['ip'], client['mac']))

cap = cv.VideoCapture("http://192.168.30.95:4747/video")

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv.imshow('frame', frame)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()