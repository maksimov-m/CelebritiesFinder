import face_recognition
import numpy as np
import os
import cv2
from deepface import DeepFace
from argparse import ArgumentParser

face_cropper = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')


embeddings_path_man = "./embeddings/video_emb"


def sqrt2_norm(arr):
    normalized_array = [value / 2**0.5 for value in arr]
    return normalized_array
def get_result(img):
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
        #embedings_woman = os.listdir(embeddings_path_woman)

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

        res_d_man = {'class': [cls[0].split('.')[0] for cls in sorted_arr_man[:4]],
                     'prob': [round((1-prob[1])*100, 2) for prob in sorted_arr_man[:4]]}

        """d = {}
        for emb in embedings_woman:
            loaded_arr = np.load(f'{embeddings_path_woman}/{emb}')
            d[emb] = []

            for el in loaded_arr:
                distance = face_recognition.face_distance([face_encoding1], el)[0]

                d[emb].append(distance)

        res_mass = []
        for cl, emb in d.items():
            res_mass.append((cl, np.mean(emb)))

        sorted_arr_woman = sorted(res_mass, key=lambda x: x[1])

        res_d_woman = {
            'class': [cls[0].split('.')[0] for cls in sorted_arr_woman[:3]],
            'prob': [prob[1] for prob in sorted_arr_woman[:3]]
        }"""

        res_d = {'class': res_d_man['class'],
                 'prob': res_d_man['prob']}
        result_list.append(((x, y, w, h), res_d))

    res_max = []

    for face, el in result_list:
        max_ = (0, 0, float('-inf'))
        for cls, prob in zip(el['class'], el['prob']):
            if prob > max_[2]:
                max_ = (face, cls, prob)
        res_max.append(max_)


    return res_max

def video_detect(path):

    cap = cv2.VideoCapture(path)

    if (cap.isOpened() == False):
        print("Error opening video stream or file")
        return

    count = 0

    set_res = []
    while True:

        ret, frame = cap.read()

        if not ret:
            break

        count += 1

        if count % 30 == 0:
            continue

        res = get_result(frame)
        # [(img, {cls : [], prob : []) ...]

        if res is None:
            continue
        for _, el, el1 in res:
            set_res.append((el, el1))

    set_res1 = {'class' : [], 'prob' : []}

    flag = False
    for d_res in set_res:
        if d_res[0] not in set_res1['class']:
            set_res1['class'].append(d_res[0])
            set_res1['prob'].append(d_res[1])
            if len(set_res1['class']) > 8:
                break
        if flag:
            break

    #d_res = {'class' : [cls[0] for cls in set_res], 'prob' : [prob[1] for prob in set_res]}
    print('end:', set_res1)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="filename")
    args = parser.parse_args()

    video_detect(args.filename)
