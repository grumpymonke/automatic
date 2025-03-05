from flask import Flask, render_template, redirect
from flask_cors import CORS, cross_origin
import cv2
from ultralytics import YOLO
import time

app = Flask(__name__, template_folder='../template')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

items = {0: 'CloseUp', 1: 'Cocoa Powder', 2: 'Colgate', 3: 'Hershey-s', 4: 'KeraGlo', 5: 'Lays', 6: 'Loreal', 7: 'Maggi', 8: 'MarieLight', 9: 'Perk'}

id_dict = {'CloseUp': 'hdsbi78dfY', 'Cocoa Powder': 'kahv238923', 'Maggi': 'jhdvsDjh3f', 'Hershey-s': 'kjbw23jhvh', 'KeraGlo': 'JHVgcYVj67', 'Lays': 'Ftuc88cUTI', 'Loreal': 'hvIViV89yv', 'MarieLight': 'iyv9779v97', 'Perk': 'iyvI9v9V76','Colgate':'etyd7890we', 'None': 'None'}

model = YOLO("E:\\Invoice-Generation-using-YOLOv8-main\\ml-model\\runs\detect\\train\\weights\\best.pt")


def gen_frames():
    flag = 0
    detected_prod = 'None'
    cap = cv2.VideoCapture(0)
    start = time.time()
    end = time.time()
    while (end-start)<=7:
        success, frame = cap.read()
        if success:
            results = model(frame, show=False, conf=0.85, show_labels=True)
            product = results[0].boxes.cls.tolist()
            if product:
                flag = 1
                return items[product[0]]
            end = time.time()
        else:
            cap.release()
            cv2.destroyAllWindows()
    if (flag==0):
        return detected_prod


@app.route("/", methods=['GET'])
@cross_origin()
def index():
    return render_template('home.html')

@app.route("/video-feed", methods=['GET'])
@cross_origin()
def video_feed():
    result = gen_frames()
    id = id_dict[result]
    if result:
        return redirect('http://localhost:3000/add-product/'+id)


if __name__ == "__main__":
    app.run(debug=True)