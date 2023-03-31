import tkinter as tk
import threading
import time
import os

root = tk.Tk()
root.title("Rating Tool")

ratings = [-3, -2, -1, 0, 1, 2, 3]

pointer = 3

recording = False

records = []

records_lock = threading.Lock()

scale_canvas = tk.Canvas(root, width=550, height=50, bg="white")
scale_canvas.pack(pady=20)

label_frame = tk.Frame(root)
label_frame.pack()

for i in range(len(ratings)):
    rating_label = tk.Label(label_frame, text=str(ratings[i]), font=("Arial", 16))
    rating_label.grid(row=0, column=i, padx=30)

def update_pointer():
    global pointer

    scale_canvas.delete("pointer")

    x = (pointer / (len(ratings) - 1)) * 500 + 25

    scale_canvas.create_line(x + 10 , 0, x + 10, 50, width=10, fill="red", tags="pointer")
    
def move_pointer_left():
    global pointer
    pointer = max(0, pointer - 1)
    update_pointer()

def move_pointer_right():
    global pointer
    pointer = min(len(ratings) - 1, pointer + 1)
    update_pointer()

root.bind("<Left>", lambda event: move_pointer_left())
root.bind("<Right>", lambda event: move_pointer_right())

def start_recording():
    global recording
    recording = True

def stop_recording():
    global recording
    recording = False

def print_pointer():
    log_file = 'C:/temp/log.txt'
    if not os.path.exists(log_file):
        with open(log_file, 'w'):
            print('C:/temp/log.txt has been created')
            pass

    with open(log_file, 'a') as f:
        while True:
            if recording:
                with records_lock:
                    records.append((pointer, time.time()))
                    print(f"Pointer is at {ratings[pointer]}")
                    log_msg = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Pointer is at {ratings[pointer]}\n"
                    f.write(log_msg)
                    f.flush()  

                time.sleep(1)

start_button = tk.Button(root, text="Start Recording", font=("Arial", 16), command=start_recording)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Recording", font=("Arial", 16), command=stop_recording)
stop_button.pack(pady=10)

threading.Thread(target=print_pointer).start()

print('Press "left" and "right" to move the pointer')
print('Click "Start Recording" to start recording, "Stop Recording" to stop recording')
print('Click "X" to exit the program')

root.mainloop()