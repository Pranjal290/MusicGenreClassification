from flask import Flask, jsonify, render_template, request
import librosa
import numpy as np
import pickle

app = Flask(__name__)

# Load the Logistic Regression model using pickle
with open('../random_forest_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)


# Function to extract features from uploaded audio file
def extract_features(file):
    y, sr = librosa.load(file, duration=30)  # Load 30 seconds of the audio
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    tempogram = librosa.feature.tempogram(y=y, sr=sr)

    features = np.hstack((mfccs.mean(axis=1), spectral_centroid.mean(), tempogram.mean(axis=1)))
    return features.reshape(1, -1)  # Return features as a 2D array


# Route to handle file upload and genre prediction
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file:
            try:
                features = extract_features(file)
                features = np.array(features)

                genres = ["Bollypop", "Carnatic", "Ghazal", "Semiclassical", "Sufi"]
                genre = genres[model.predict(features)[0]]
                return jsonify({'genre': genre})
            except Exception as e:
                return jsonify({'error': 'Error processing file: ' + str(e)})

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
