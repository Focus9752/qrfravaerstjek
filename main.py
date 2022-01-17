import cv2
from pyzbar import pyzbar
import pyttsx3
from playsound import playsound
import json

seennames = []

# Stores s

studentsDict = {
    ("Alberte Cort"): False,
    ("Anton Lauve Hermann"): False,
    ("Clara Thorsø Kousgaard"): False,
    ("Ella Petersen"): False,
    ("Eniola Felix Ladipo Oyebo"): False,
    ("Frederik Elstrøm Hansen"): False,
    ("Frederikke Ankjær Andersen"): False,
    ("Hector Chamero Andersen"): False,
    ("Josefine Victoria Wildschiødtz"): False,
    ("Lasse West Holstvig"): False,
    ("Lucca Vibeke Prühs"): False,
    ("Marcus Koschmieder Krogsgaard"): False,
    ("Maya Oh Holmen"): False,
    ("Oliver Christian Glæsel Fugmann"): False,
    ("Pauline Baden Munkholm"): False,
    ("Philip Søholt"): False,
    ("Samuel Alvarez Grønbech-Jensen"): False,
    ("Thor Marner"): False
}

def read_barcodes(frame):
    # Læs det nuværende billede fra kameraet og led efter QR-koder
    barcodes = pyzbar.decode(frame)

    # For hver QR-kode som vi ser i billedet
    for barcode in barcodes:
        # Koordinaterne til QR-koden i billedet
        x, y , w, h = barcode.rect
        
        # Aflæs QR-koden (antag at den indeholder tekst i utf-8 format)
        barcode_info = barcode.data.decode('utf-8')
        # Tegn en grøn kant rundt om QR-koden
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        
        # Vis teksten fra QR koden oven på koden
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        
        # Hvis vi ikke har set navnet før
        if barcode_info not in seennames:
            # Tilføj det til listen af sete navne
            seennames.append(barcode_info)

            # Opdater filen med de sete navne
            with open("barcode_result.txt", mode ='w') as file:
                file.write(str(seennames))
            
            # 
            engine = pyttsx3.init()
            engine.say(barcode_info + "has checked in.")
            engine.runAndWait()
    return frame

def main():
    #1
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    #2
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame)
        cv2.imshow('Barcode/QR code reader', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    #3
    camera.release()
    cv2.destroyAllWindows()
#4
if __name__ == '__main__':
    main()


