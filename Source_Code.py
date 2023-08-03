import face_recognition
import cv2
import numpy as np
import pandas as pd  
import csv
import os 
from datetime import datetime

video_capture = cv2.VideoCapture(0)

anand_image = face_recognition.load_image_file(r"C:\Users\anand\OneDrive\Desktop\project\Photos\anand.jpg")
anand_encoding = face_recognition.face_encodings(anand_image)[0]

vipin_image = face_recognition.load_image_file(r"C:\Users\anand\OneDrive\Desktop\project\Photos\vipin.jpg")
vipin_encoding = face_recognition.face_encodings(vipin_image)[0]

known_faces_encodings = [
    anand_encoding,
    vipin_encoding,
]

known_faces_names = [
    "anand",
    "vipin",
]
print(known_faces_names)
students = known_faces_names.copy()

face_location = []
face_encodings = []
face_names = []
s = True
df = pd.DataFrame()
print("DataFrame created")
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f = open(current_date + '.csv', 'w+', newline='')
lnwriter = csv.writer(f)
print("still running")
allName=[]
allDate=[]
allTime=[]
# data={"Current_Date":[], "Name":[], "Current_Time":[]}
# df=pd.DataFrame(data)
while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    if s:
        face_location = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_location)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_faces_encodings, face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(known_faces_encodings, face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]
            
            face_names.append(name)
            if name in known_faces_names:
                if name in students:
                    students.remove(name)
                    print(students)
                    current_time = datetime.now().strftime("%H:%M:%S")
                    lnwriter.writerow([current_date, name, current_time,])
                    a="Book.xlsx"
                    # data.update({"Current_Date":current_date, "Name":name, "Current_Time":current_time})
                    # df.append(data,ignore_index=True)
                    
                    allDate.append(current_date)
                    allTime.append(current_time)
                    allName.append(name)
                    

    cv2.imshow("attendance system", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
f.close()
# print(data)
print('The end Running')
b=pd.DataFrame({"Current_Date":allDate, "Name":allName, "Current_Time":allTime})
print(b)
b.to_excel(a,sheet_name="Sheet1",index=False)
print("done")




