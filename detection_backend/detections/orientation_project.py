from scapy.all import ARP, Ether, srp
import numpy as np
import cv2 as cv
from ultralytics import YOLO
import queue
import threading


model = YOLO("yolov8n.pt")
model.classes = [0] # Only detect people

target_ip = "192.168.30.1/24"

phone_mac = ("1A:E0:B7:ED:1D:52").lower()

arp = ARP(pdst=target_ip)

def scan_network():
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=0)[0]

    clients = []


    found = False

    for sent, received in result: # Iterate through the results of the ARP request
     if received.hwsrc.lower() == phone_mac: # Check if the MAC address matches the phone's MAC address
        print(f"Found phone with IP: {received.psrc} and MAC: {received.hwsrc}") # This will print the IP and MAC address of the phone
        found = True
        phone_ip = received.psrc
        clients.append({'ip': received.psrc, 'mac': received.hwsrc}) # Append the IP and MAC address to the clients list


    return found, phone_ip, clients

    # print("Available devices in the network:")
    # print("IP" + " " * 18 + "MAC")
    # for client in clients: # Print the IP and MAC addresses of all devices found in the network
    #     print("{:16}    {}".format(client['ip'], client['mac'])) 

def start_stream(video_url, frame_skip = 3):
    cap = cv.VideoCapture(video_url) #"http://192.168.30.95:4747/video"

    if not cap.isOpened():
        print("Cannot open camera")
        return None, None

    frame_queue = queue.Queue(maxsize=2) # Create a queue to hold frames for processing

def frame_reader(cap, frame_skip, frame_queue):
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame_count += 1
        if frame_count % frame_skip != 0:
           continue  # Skip this frame

        try:
            frame_queue.put(frame, timeout=0.01)
        except queue.Full:
            pass
    
    reader_thread = threading.Thread(target=frame_reader, daemon = True)
    reader_thread.start()

    return cap, frame_queue

def gen_frames(frame_queue):
    while True: # Continuously process frames from the queue
        frame = frame_queue.get() # Get the next frame from the queue
        if frame is None: # If the frame is None, break the loop
            break

        resized = cv.resize(frame, (640, 640)) # Resize the frame to 640x640 for faster processing
        results = model(resized, verbose=False)[0] # Perform inference on the resized frame
        annotated_frame = results.plot() # Annotate the frame with detection results

        ret, buffer = cv.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + 'b\r\n')
    
        

       
       
       
       
       
       
        #if cv.waitKey(1) & 0xFF == ord('q'): # Exit if 'q' is pressed
           # break
   









