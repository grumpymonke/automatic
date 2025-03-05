import cv2
from ultralytics import YOLO
import time
model=YOLO("C:\\Users\\Harsha\\Retail-Billing-System\\runs\\detect\\train\\weights\\best.pt")
#model.predict(source=,show=True,save=True, conf=0.7)
items = {0: 'CloseUp', 1: 'Cocoa Powder', 2: 'Colgate', 3: 'Hershey-s', 4: 'KeraGlo', 5: 'Lays', 6: 'Loreal', 7: 'Maggi', 8: 'MarieLight', 9: 'Perk'}
products = []
cap = cv2.VideoCapture(0)
while cap.isOpened():
    try: 
        success, frame = cap.read()
        if success:
            results = model(frame, show=True, conf=0.85, show_labels=True)
            annotated_frame = results[0].plot(show_conf=False, line_thickness=10)
            product = results[0].boxes.cls.tolist()
            for i in range(0,len(product)):
                decision = input("Is this "+items[product[i]]+"?Y/n ")
                if decision == 'y' or decision=='Y':
                    if len(product) != 0:
                        products.append(items[product[i]])
            print(products)
            cv2.imshow("YOLOv8 Inference", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break
    except IndexError:
        time.sleep(0.5)
cap.release()
cv2.destroyAllWindows()