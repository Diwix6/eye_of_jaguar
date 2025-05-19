from ultralytics import YOLO
import cv2
import requests
from picamera2 import Picamera2
from math import ceil

def get_number(data_list):
    name_count = {}
    for item in data_list:
        name = item['name']
        name_count[name] = name_count.get(name, 0) + 1
    return name_count


def run():

    model = YOLO("inference.pt")

    cap = Picamera2()
    cap.configure(cap.create_preview_configuration(main={"format": 'RGB888', "size": (640, 480)}))
    cap.start()
    # print('Статус:', response.status_code)
    # print('Ответ сервера:', response.json())
    counter = 0
    print("Скрипт запущен")
    summ = {}
    while 1:
        # Read a frame from the video
        frame = cap.capture_array()
        
        if 1:
            # Run YOLO inference on the frame
            #frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
            results = model(frame)
            counter += 1
            # Visualize the results on the frame
            annotated_frame = results[0].plot()
            objects_in_frame = get_number(results[0].summary())
            # print("---objects in frame:", objects_in_frame)
            for item, value in objects_in_frame.items():
                summ[item] = summ.get(item, 0) + value
                
            if counter == 4:
                data = {}
                for obj, value in summ.items():
                    data.update({obj: ceil(value/4 + 0.1)})
                print('     data:', data)
                print('     summ:', summ)
                response = requests.post('http://127.0.0.1:8000/', json=data)
                counter = 0
                print('Статус:', response.status_code)
                summ = {}
                # print('Ответ сервера:', response.json())
            # Display the annotated frame
            #cv2.imshow("YOLO Inference", annotated_frame)

            # Break the loop if 'q' is pressed
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture object and close the display window

if __name__ == '__main__':
    run()


# send_data.py (в той же директории)
# import json

# data = {
#     'name': 'ULK',
#     'people_count': 5,
# }

# response = requests.post('http://127.0.0.1:8000/api/receive-data/', json=data)

# print('Статус:', response.status_code)
# print('Ответ сервера:', response.json())
