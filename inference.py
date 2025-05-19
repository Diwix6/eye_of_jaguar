from ultralytics import YOLO
import cv2
import requests

def get_number(list):
    dict = {}
    for object in list:
        if dict[object["name"]]:
            dict[object["name"]] += 1
        else:
            dict[object["name"]] = 0
    return dict


def run():

    model = YOLO("inference.pt")

    cap = cv2.VideoCapture(0)
    counter = 0
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        print(success, frame)
        summ = {}
        if success:
            # Run YOLO inference on the frame
            results = model(frame)
            counter += 1
            # Visualize the results on the frame
            annotated_frame = results[0].plot()
            objects_in_frame = get_number(results[0].summary)
            for object, value in objects_in_frame.items():
                summ[object] += value
            if counter == 4:
                data = {}
                for object, value in objects_in_frame.items():
                    data.update({object: value/4})
                response = requests.post('http://127.0.0.1:8000/', json=data)
                counter = 0
            # Display the annotated frame
            cv2.imshow("YOLO Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()

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
