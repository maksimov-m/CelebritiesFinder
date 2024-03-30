import cv2
import os


def parse_yolo_annotation(annotation):
    data = annotation.split(' ')
    class_id = int(data[0])
    x_center = float(data[1])
    y_center = float(data[2])
    width = float(data[3])
    height = float(data[4])
    x_coords = [float(coord.split(',')[0]) for coord in data[5:]]
    y_coords = [float(coord.split(',')[1]) for coord in data[5:]]
    return class_id, x_center, y_center, width, height, x_coords, y_coords


def crop_image(image, x_center, y_center, width, height, x_coords, y_coords):
    image_height, image_width, _ = image.shape
    left = int((x_center - width / 2) * image_width)
    top = int((y_center - height / 2) * image_height)
    right = int((x_center + width / 2) * image_width)
    bottom = int((y_center + height / 2) * image_height)
    cropped_image = image[top:bottom, left:right]

    # Adjust coordinates of points relative to cropped image
    x_coords = [(x - left) / (right - left) for x in x_coords]
    y_coords = [(y - top) / (bottom - top) for y in y_coords]

    return cropped_image, x_coords, y_coords


def draw_points(image, x_coords, y_coords):
    for x, y in zip(x_coords, y_coords):
        x = int(x * image.shape[1])
        y = int(y * image.shape[0])
        cv2.circle(image, (x, y), 3, (0, 255, 0), -1)
    return image


data = os.listdir('./data')
for files in data:
    faces = os.listdir(f'./data/{files}')

    count = len(faces) // 2
    if not os.path.exists(f'./res/{files}'):
        os.mkdir(f'./res/{files}')
    for i in range(1, count + 1):
        image = cv2.imread(f"data/{files}/{i}.jpg")
        with open(f"data/{files}/{i}.txt", "r") as f:
            annotation = f.readline()

        try:
            # Parse YOLO annotation
            class_id, x_center, y_center, width, height, x_coords, y_coords = parse_yolo_annotation(annotation)
            # Crop image
            cropped_image, adjusted_x_coords, adjusted_y_coords = crop_image(image, x_center, y_center, width, height,
                                                                             x_coords,
                                                                             y_coords)
            # Draw points on cropped image
            cropped_image_with_points = draw_points(cropped_image.copy(), adjusted_x_coords, adjusted_y_coords)

            cv2.imwrite(f'./res/{files}/{i}.jpg', cropped_image_with_points)
        except:
            print(files, i)
