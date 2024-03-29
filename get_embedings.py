import face_recognition
import numpy as np
import os

data = os.listdir('./res')
for file in data:
    images = os.listdir(f'./res/{file}')
    mass = []
    for img in images:
        image1 = face_recognition.load_image_file(f"./res/{file}/{img}")

        face_encoding1 = face_recognition.face_encodings(image1, known_face_locations=[(0, 0, image1.shape[0], image1.shape[1])])[0]
        mass.append(list(face_encoding1))
        # Сохранение массива в текстовый файл

    mass = np.array(mass)
    np.save(f'./embedings/{file}.npy', mass)


"""# Загрузка изображений с лицами
# image1 = face_recognition.load_image_file("res7/10.jpg")
# image2 = face_recognition.load_image_file("res7/30.jpg")
image1 = face_recognition.load_image_file("res/1/1.jpg")
image2 = face_recognition.load_image_file("res/7/2.jpg")

# Получение встроенных представлений для каждого изображения
face_encoding1 = face_recognition.face_encodings(image1, known_face_locations=[(0, 0, image1.shape[0], image1.shape[1])])[0]
face_encoding2 = face_recognition.face_encodings(image2, known_face_locations=[(0, 0, image2.shape[0], image2.shape[1])])[0]

# Вычисление расстояния между встроенными представлениями
distance = face_recognition.face_distance([face_encoding1], face_encoding2)[0]

# Вывод результата (чем ближе к нулю, тем более похожи лица)
print("Расстояние между лицами EUC:", distance)"""
