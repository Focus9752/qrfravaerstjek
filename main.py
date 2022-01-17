import cv2
from pyzbar import pyzbar
import pyttsx3
from playsound import playsound
import json

seennames = []

studentsDict = {
    "3a 02": ["Alberte Cort", "false"],
    "3a 31": ["Anton Lauve Hermann", "false"],
    "3a 07": ["Clara Thorsø Kousgaard", "false"],
    "3a 08": ["Ella Petersen", "false"],
    "3a 29": ["Eniola Felix Ladipo Oyebo", "false"],
    "3a 10": ["Frederik Elstrøm Hansen", "false"],
    "3a 11": ["Frederikke Ankjær Andersen", "false"],
    "3a 12": ["Hector Chamero Andersen", "false"],
    "3a 13": ["Josefine Victoria Wildschiødtz", "false"],
    "3a 14": ["Lasse West Holstvig", "false"],
    "3a 30": ["Lucca Vibeke Prühs", "false"],
    "3a 16": ["Marcus Koschmieder Krogsgaard", "false"],
    "3a 17": ["Maya Oh Holmen", "false"],
    "3a 20": ["Oliver Christian Glæsel Fugmann", "false"],
    "3a 21": ["Pauline Baden Munkholm", "false"],
    "3a 22": ["Philip Søholt", "false"],
    "3a 25": ["Samuel Alvarez Grønbech-Jensen", "false"],
    "3a 26": ["Thor Marner", "false"]
}

def updateJSON():
    for name in seennames:
        studentsDict[name][1] = "true"
    
    with open('students.json', 'w') as outfile:
        json.dump(studentsDict, outfile)

def read_barcodes(frame):
    # Læs den nuværende frame fra kameraet og led efter QR-koder
    barcodes = pyzbar.decode(frame)

    # For hver QR-kode som vi ser
    for barcode in barcodes:
        # Koordinaterne til QR-koden på skærmen
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

            updateJSON()
            
            # Kom med tts-melding om at eleven har tjekket ind
            engine = pyttsx3.init()
            engine.say(studentsDict[barcode_info][0] + "has checked in.")
            engine.runAndWait()
    return frame

def main():
    # Hent frame fra kameraet med openCV2-biblioteket
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    
    # Led efter QR-koder i billedet
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame)
        cv2.imshow('Barcode/QR code reader', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    # Luk programmet hvis brugeren trykker esc
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()


