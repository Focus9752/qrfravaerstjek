import cv2, openpyxl, pyttsx3, pandas, sys
from pyzbar import pyzbar
import PySimpleGUI as sg

seennames = []

studentsDict = {
    "Antal elever til stede:": ["2/18", ""],
    "3a 02": ["Alberte Cort", "Fraværende"],
    "3a 31": ["Anton Lauve Hermann", "Fraværende"],
    "3a 07": ["Clara Thorsø Kousgaard", "Fraværende"],
    "3a 08": ["Ella Petersen", "Fraværende"],
    "3a 29": ["Eniola Felix Ladipo Oyebo", "Fraværende"],
    "3a 10": ["Frederik Elstrøm Hansen", "Fraværende"],
    "3a 11": ["Frederikke Ankjær Andersen", "Fraværende"],
    "3a 12": ["Hector Chamero Andersen", "Fraværende"],
    "3a 13": ["Josefine Victoria Wildschiødtz", "Fraværende"],
    "3a 14": ["Lasse West Holstvig", "Fraværende"],
    "3a 30": ["Lucca Vibeke Prühs", "Fraværende"],
    "3a 16": ["Marcus Koschmieder Krogsgaard", "Fraværende"],
    "3a 17": ["Maya Oh Holmen", "Fraværende"],
    "3a 20": ["Oliver Christian Glæsel Fugmann", "Fraværende"],
    "3a 21": ["Pauline Baden Munkholm", "Fraværende"],
    "3a 22": ["Philip Søholt", "Fraværende"],
    "3a 25": ["Samuel Alvarez Grønbech-Jensen", "Fraværende"],
    "3a 26": ["Thor Marner", "Fraværende"]
}

def updateFile():
    studentsAttendingCount = 0

    for name in seennames:
        studentsDict[name][1] = "Til stede"
    
    for key, value in studentsDict.items():
        if studentsDict[key][1] == "Til stede":
            studentsAttendingCount += 1

    studentsDict["Antal elever til stede:"] = [str(studentsAttendingCount) + "/18", " "]

    df = pandas.DataFrame(data=studentsDict)
    df.to_excel("fravær.xlsx", index=False) 

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
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 0, 255), 2)
        
        # Vis teksten fra QR koden oven på koden
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (0, 0, 255), 1)
        
        # Hvis vi ikke har set navnet før
        if barcode_info not in seennames:
            # Tilføj det til listen af sete navne
            seennames.append(barcode_info)

            updateFile()
            
            # Kom med tts-melding om at eleven har tjekket ind
            engine = pyttsx3.init()
            engine.say(studentsDict[barcode_info][0] + "has checked in.")
            engine.runAndWait()
    return frame

# Driver kode
print("Velkommen!")
print()
print("Når du lige om lidt starter programmet vil du se en kameravisning der hjælper dig med at scanne QR-koderne.")
print("Hold QR-koden op til kameraet og vent indtil programmet siger at du er tjekket ind.")
print()
print("Outputtet vil blive gemt i filen 'fravær.xlsx'.")
print("Husk dog først at tjekke excelfilen når du har lukket programmet!")
print()
if input("Vil du starte programmet? (J/N): ").lower() == "j":
    pass
else:
    sys.exit()

window = sg.Window('Demo Application - OpenCV Integration', [[sg.Image(filename='', key='image')],], location=(800,400))
camera = cv2.VideoCapture(0)       # Indlæs kameraet
updateFile()

while True:                     # Løkke til visning af video
    event, values = window.Read(timeout=20, timeout_key='timeout')      # Tjek om vinduet stadig er åbent hvert 20. ms
    if event is None:  
        break                                            # Bryd løkken og stop programmet hvis vinduet er lukket
    cv2image= cv2.cvtColor(camera.read()[1],cv2.COLOR_BGR2RGB)
    frame = read_barcodes(cv2image)
    window.find_element('image').Update(data=cv2.imencode('.png', frame)[1].tobytes()) # Opdater billedet i videoen

