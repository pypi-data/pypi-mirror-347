import os
import sys
from frame_pb2 import Frame

# Pfad zum Protobuf-Python-Package
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

# TODO: Pfad hier anpassen oder per sys.argv laden
FRAME_FILE = r"C:\Users\abaum\Downloads\frame_0002.pb"

def main():
    if not os.path.isfile(FRAME_FILE):
        print(f"Datei nicht gefunden: {FRAME_FILE}")
        sys.exit(1)

    # Laden und Parsen
    with open(FRAME_FILE, "rb") as f:
        data = f.read()
    frame = Frame()
    frame.ParseFromString(data)

    # Einfach ausgeben
    print(frame.object_list)

if __name__ == "__main__":
    main()
