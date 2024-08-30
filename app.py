from flask import Flask, render_template, Response, request, redirect, url_for
import cv2

app = Flask(__name__)

# Global variable to store the camera source
camera_source = 0
cap = None

def generate_frames():
    global cap
    if not cap or not cap.isOpened():
        print("Error: Could not open camera.")
        return b''

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame as a byte array
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/', methods=['GET', 'POST'])
def index():
    global camera_source, cap
    if request.method == 'POST':
        # Get the camera input from the form
        camera_input = request.form.get('camera_input')

        # Check if input is a digit (camera index) or URL (IP camera)
        if camera_input.isdigit():
            camera_source = int(camera_input)
        else:
            camera_source = camera_input

        # Release the current camera and reinitialize with the new source
        if cap:
            cap.release()

        cap = cv2.VideoCapture(camera_source)

        if not cap.isOpened():
            print("Error: Could not open camera with source:", camera_source)
        
        return redirect(url_for('index'))

    # Renders the index.html file
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Returns the response generated along with the specific media type (mime type)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
