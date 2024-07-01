import cv2 as cv
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
import argparse
import csv
import tensorflow as tf


cap = None
initializeaza_camera = False


def dim_camera():
    p = argparse.ArgumentParser()
    p.add_argument("--device", type=int, default=0)
    p.add_argument("--width", type=int, default=960)
    p.add_argument("--height", type=int, default=540)
    argumentele = p.parse_args()
    return argumentele
    
    
def main():
    global initializeaza_camera, cap

    args = dim_camera()
    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)
    
    model_salvare = 'C:/Users/Adda/PycharmProjects/licenta/clasificare.hdf5' 
    clasificare = load_model(model_salvare)

    clasificare.compile(
        optimizer='adam',  
        loss='sparse_categorical_crossentropy',  
        metrics=['accuracy']  
    )

    model = mp.solutions.hands
    instanta = model.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    )

    gest_digit = {
        0: 0,  
        1: 1,  
        2: 2   
    }

    gestul_curent = None
    file_path = "C:/Users/Adda/PycharmProjects/licenta/gestul_salvat.csv"

    gest_label = ['Hartie', 'Piatra', 'Foarfeca']

    while True:
        ret, image = cap.read()
        if not ret:
            break

        if not initializeaza_camera:
            initializeaza_camera = True  

        image = cv.flip(image, 1)
        debug_image = image.copy()
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        results = hands.process(image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmark_list = [(lm.x, lm.y) for lm in hand_landmarks.landmark]

                pre_processed_landmark_list = pre_process_landmark(landmark_list)

                prediction = model.predict(np.array([pre_processed_landmark_list]), verbose=0)  
                gest_id = np.argmax(prediction)
                gest_label = gest_label[gest_id]

                if gest_id != gestul_curent:
                    print("ID-ul gestului este: ", gest_id)
                    gestul_curent = gest_id
                    gest_digit = gest_digit.get(gest_id, -1)
                    if gest_digit != -1:
                        with open(file_path, mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([gest_digit])

    cap.release()
    cv.destroyAllWindows()


def pre_process_landmark(landmark_list):
    base_x, base_y = landmark_list[0]
    normalized_landmarks = [(x - base_x, y - base_y) for x, y in landmark_list]
    normalized_landmarks = np.array(normalized_landmarks).flatten()
    max_value = np.max(np.abs(normalized_landmarks))
    normalized_landmarks /= max_value
    return normalized_landmarks


def opresete_camera():
    global cap
    if cap is not None:
        cap.release()


if __name__ == '__main__':
    main()
