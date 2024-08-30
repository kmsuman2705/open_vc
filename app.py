from flask import Flask, render_template, Response
import cv2


app = Flask(__name__)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Define the function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Open the camera
cap = cv2.VideoCapture(0)



def generate_frames():
    while True:
        # Capture frame-by-frame
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

@app.route('/')
def index():
    # Renders the index.html file
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Returns the response generated along with the specific media type (mime type)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
