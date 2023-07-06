import keyboard
import queue
import threading
import time

def start_recording(esc_queue, audio_queue):
    print("Recorder started.")
    # Simuliere das Aufnehmen von Audio und füge es zur Audio-Warteschlange hinzu
    audio_data = b"Dummy Audio Data"
    audio_queue.put(audio_data)

    # Beispielcode für eine Endlosschleife, die auf das ESC-Tastenereignis wartet
    while True:
        if not esc_queue.empty():
            esc_key = esc_queue.get()
            if esc_key == "esc":
                print("ESC key pressed. Stopping recording.")
                break

    print("Recording stopped.")

def listen_for_esc(esc_queue):
    keyboard.on_press_key("esc", lambda _: esc_queue.put("esc"))

def start_recorder():
    esc_queue = queue.Queue()
    audio_queue = queue.Queue()

    # Starte den Thread zum Abhören des ESC-Tastenereignisses
    esc_thread = threading.Thread(target=listen_for_esc, args=(esc_queue,))
    esc_thread.start()

    # Starte den Thread für die Aufnahme
    recording_thread = threading.Thread(target=start_recording, args=(esc_queue, audio_queue,))
    recording_thread.start()

    # Hier kannst du die Audio-Warteschlange verwenden, um das aufgezeichnete Audio in der main.py zu erhalten
    return audio_queue
