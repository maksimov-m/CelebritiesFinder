import face_recognition
import numpy as np
import os
import cv2
from deepface import DeepFace

gender = {'man': 0, 'woman': 0}
data = os.listdir('./res')
for file in data:
    images = os.listdir(f'./res/{file}')
    mass = []
    gender['man'] = 0
    gender['woman'] = 0

    gender_flag = 'woman'

    for j, img in enumerate(images):

        image_path = f"./res/{file}/{img}"  # Путь к вашему изображению
        image = cv2.imread(image_path)

        # Используем библиотеку OpenCV для обнаружения лиц
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        result = None
        # Проходим по каждому обнаруженному лицу
        for i, (x, y, w, h) in enumerate(faces):
            face = image[y:y + h, x:x + w]

            # Используем DeepFace для определения пола, возраста и национальности
            result = DeepFace.analyze(face, actions=['gender'], enforce_detection=False)[0]

            if result is None:
                continue
            break
        if j == 0:
            if result is None or result["gender"]["Woman"] > result["gender"]["Man"]:
                gender_flag = 'woman'
            else:
                gender_flag = 'man'

        image1 = face_recognition.load_image_file(f"./res/{file}/{img}")

        # face_encoding1 = face_recognition.face_encodings(image1, known_face_locations=[(0, 0, image1.shape[0], image1.shape[1])])[0]
        face_embedding1 = DeepFace.represent(
            img_path=f'res/{file}/{img}', enforce_detection=False
        )[0]['embedding']
        mass.append(list(face_embedding1))

    print(file)
    mass = np.array(mass)
    if gender_flag == 'woman':
        np.save(f'./embeddings/woman/{file}.npy', mass)
    else:
        np.save(f'./embeddings/man/{file}.npy', mass)
