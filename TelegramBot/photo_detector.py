from argparse import ArgumentParser

import face_recognition
import numpy as np
import os
import cv2
from deepface import DeepFace

# модель, выделяющая лицо на фотографии
face_cropper = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
embeddings_path_man = './embeddings/man'
embeddings_path_woman = './embeddings/woman'


def sqrt2_norm(arr):
    normalized_array = [value / 2**0.5 for value in arr]
    return normalized_array


def photo_detector(path):
    img = cv2.imread(path)
    if img is None:
        raise Exception("No such file of directory")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cropper.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return None

    result_list = []
    for index, (x, y, w, h) in enumerate(faces):
        face_img = img[y:y + h, x:x + w]
        try:
            face_encoding1 = DeepFace.represent(img_path=face_img, enforce_detection=False)[0]['embedding']
        except Exception as e:
            print(e)
            raise Exception("Corrupted file")

        embedings_man = os.listdir(embeddings_path_man)
        embedings_woman = os.listdir(embeddings_path_woman)

        d = {}
        for emb in embedings_man:
            loaded_arr = np.load(f'{embeddings_path_man}/{emb}')
            d[emb] = []

            for el in loaded_arr:
                distance = face_recognition.face_distance([face_encoding1], el)[0]

                d[emb].append(distance)

        res_mass = []
        for cl, emb in d.items():
            res_mass.append((cl, np.min(sqrt2_norm(emb))))

        sorted_arr_man = sorted(res_mass, key=lambda x: x[1])

        res_d_man = {'class': [cls[0].split('.')[0] for cls in sorted_arr_man[:3]],
                     'prob': [round((1-prob[1])*100, 2) for prob in sorted_arr_man[:3]]}

        d = {}
        for emb in embedings_woman:
            loaded_arr = np.load(f'{embeddings_path_woman}/{emb}')
            d[emb] = []

            for el in loaded_arr:
                distance = face_recognition.face_distance([face_encoding1], el)[0]

                d[emb].append(distance)

        res_mass = []
        for cl, emb in d.items():
            res_mass.append((cl, np.min(sqrt2_norm(emb))))

        sorted_arr_woman = sorted(res_mass, key=lambda x: x[1])
        res_d_woman = {
            'class': [cls[0].split('.')[0] for cls in sorted_arr_woman[:3]],
            'prob': [round((1-prob[1])*100, 2) for prob in sorted_arr_woman[:3]]
        }

        res_d = {'class': res_d_man['class'] + res_d_woman['class'], 'prob': res_d_man['prob'] + res_d_woman['prob']}
        result_list.append(((x, y, w, h), res_d))
    return result_list


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename")
    args = parser.parse_args()

    photo_detector(args.filename)
