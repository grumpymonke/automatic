from flask import stream_with_context, Flask, Response, render_template, request, jsonify, url_for, redirect, json
from flask_cors import CORS, cross_origin
import cv2
import base64
from ultralytics import YOLO
import time

app = Flask(__name__,template_folder='../template')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

items = {0: 'CloseUp', 1: 'Cocoa Powder', 2: 'Colgate', 3: 'Hershey-s', 4: 'KeraGlo', 5: 'Lays', 6: 'Loreal', 7: 'Maggi', 8: 'MarieLight', 9: 'Perk'}

model=YOLO("C:\\Users\\Harsha\\retail-billing-system\\runs\\detect\\train\\weights\\best.pt")

def gen_frames():
    detected_prod = 'None'
    frame_data = '0'
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if success:
            results = model(frame, show=False, conf=0.85, hide_labels=True)
            annotated_frame = results[0].plot(show_conf=False, line_thickness=10)
            product = results[0].boxes.cls.tolist()
            if product:
                #app.test_client().post('http://localhost:5000/product-name', data=items[product[0]])
                #time.sleep(3)
                detected_prod = str(items[product[0]])
            annotated_frame = cv2.resize(annotated_frame, (780, 400))
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            #annotated_frame = buffer.tobytes()
            #encoded_image = (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + annotated_frame + b'\r\n')
            """Frame data gets clipped if sent in json format, hence it is impossible to send an entire frame with this level of compression along with the product detected"""
            frame_data = base64.b64encode(buffer).decode('utf-8')
            #product_message = {'product': detected_prod}
            #bytes = json.dumps(jsonify({'product': product_message,'frame': frame_data})).decode('utf-8')
            #yield '{"message": "'
            #yield detected_prod + '", '
            #yield '"frame": "'
            #yield frame_data
            #yield '"}'
            yield json.dumps({'message': detected_prod,'frame': frame_data})
        else:
            cap.release()
            cv2.destroyAllWindows()

def annotate():
    while True:
        frame = request.files
        if frame:
            results = model(frame, show=False, conf=0.85, hide_labels=True)
            annotated_frame = results[0].plot(show_conf=False, line_thickness=10)
            product = results[0].boxes.cls.tolist()
            if product:
                time.sleep(1)
                """decision = input("Is this "+items[product[0]]+"?Y/n ")
                if decision == 'y' or decision=='Y':
                    products.append(items[product[0]])
                print(products)"""
            flag, buffer = cv2.imencode('.jpg', annotated_frame)
            annotated_frame = buffer.tobytes()
            return (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + annotated_frame + b'\r\n')
        

@app.route("/", methods=['GET'])
@cross_origin()
def index():
    return render_template('home.html')

@app.route("/video-feed", methods=['GET'])
@cross_origin()
def video_feed():
    return Response(stream_with_context(gen_frames()), mimetype='application/json')

@app.route("/process-frames", methods=['POST'])
@cross_origin()
def process_frames():
    return Response(annotate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
        app.run(debug=True)