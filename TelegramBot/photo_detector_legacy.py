import face_recognition
import numpy as np
import os
import cv2
from deepface import DeepFace

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')


def photo_detect(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    print(len(faces))
    for index, (x,y,w,h) in enumerate(faces):
        #cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        #roi_gray = gray[y:y+h, x:x+w]
        #roi_color = img[y:y+h, x:x+w]


        img = img[y:y+h, x:x+w]

        cv2.imwrite('tmp.jpg', img)
        break





    #try:
        #img = cv2.imread(f'tmp.jpg')
    face_encoding1 = DeepFace.represent(
            img, enforce_detection=False
        )[0]['embedding']
        #face_encoding1 = face_recognition.face_encodings(image1, known_face_locations=[(0, 0, image1.shape[0], image1.shape[1])])[0]
    #except:
        #print('end:', {'class': 'None', 'prob': 'None'})
        #return

    embedings_man = os.listdir('embeddings/man')
    embedings_woman = os.listdir('embeddings/woman')

    d = {}
    for emb in embedings_man:
        loaded_arr = np.load(f'embeddings/man/{emb}')
        d[emb] = []

        for el in loaded_arr:
            distance = face_recognition.face_distance([face_encoding1], el)[0]

            d[emb].append(distance)
            # Вывод результата (чем ближе к нулю, тем более похожи лица)

    result = (0, float('inf'))
    res_mass = []
    for cl, emb in d.items():
        res_mass.append((cl, np.mean(emb)))

    sorted_arr_man = sorted(res_mass, key=lambda x: x[1])

    res_d_man = {'class' : [cls[0].split('.')[0] for cls in sorted_arr_man[:3]], 'prob' : [prob[1] for prob in sorted_arr_man[:3]]}

    d = {}
    for emb in embedings_woman:
        loaded_arr = np.load(f'embeddings/woman/{emb}')
        d[emb] = []

        for el in loaded_arr:
            distance = face_recognition.face_distance([face_encoding1], el)[0]

            d[emb].append(distance)
            # Вывод результата (чем ближе к нулю, тем более похожи лица)

    result = (0, float('inf'))
    res_mass = []
    for cl, emb in d.items():
        res_mass.append((cl, np.mean(emb)))

    sorted_arr_woman = sorted(res_mass, key=lambda x: x[1])

    res_d_woman = {'class' : [cls[0].split('.')[0] for cls in sorted_arr_woman[:3]], 'prob' : [prob[1] for prob in sorted_arr_woman[:3]]}


    res_d = {'class' : res_d_man['class'] + res_d_woman['class'], 'prob' : res_d_man['prob'] + res_d_woman['prob']}

    print('end:', res_d)
    return res_d


