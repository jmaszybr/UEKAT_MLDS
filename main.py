import cv2
import requests
import imutils
from io import BytesIO
import numpy as np
from flask import Flask, request, make_response
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

# Inicjalizacja deskryptora HOG / detektora ludzi
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

app = Flask(__name__)
api = Api(app)


class PeopleCounter(Resource):
    @staticmethod
    def get():
        # Wczytywanie obrazu
        filename = 'images/test06.png'
        image = cv2.imread(filename)
        image = imutils.resize(image,
                               width=min(500, image.shape[1]))

        # Wykrywanie ludzi na obrazie
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

        # Zwraca nazwę ppliku i liczbę wykrytych ludzi
        return {'filename': filename, 'peopleCount': len(rects)}


class PeopleCounterDynamicUrl(Resource):
    @staticmethod
    def get():
        # Pobieranie adresu URL z parametrów zapytania
        url = request.args.get('url')

        # Sprawdzanie, czy URL został podany
        if not url:
            return {'error': 'No URL provided'}, 400

        try:
            # Pobieranie obrazu z URL
            response = requests.get(url)
            response.raise_for_status()

            # Konwersja zawartości odpowiedzi na obraz
            image_bytes = BytesIO(response.content)
            image = cv2.imdecode(np.frombuffer(image_bytes.read(), np.uint8), 1)
            image = imutils.resize(image, width=min(500, image.shape[1]))

            # Wykrywanie ludzi na obrazie
            (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

            # Zwraca URL i liczbę wykrytych ludzi
            return {'url': url, 'peopleCount': len(rects)}

        except requests.RequestException as e:
            return {'error': str(e)}, 500


class PeopleCounterUpload(Resource):
    @staticmethod
    def get():
        # HTML do wyświetlania formularza przesyłania obrazu z dodanym stylem CSS
        html = '''<!DOCTYPE html>
                  <html>
                  <head>
                      <title>Upload Image</title>
                      <style>
                          body {
                              font-family: Arial, sans-serif;
                              background-color: #f4f4f4;
                              display: flex;
                              flex-direction: column;
                              align-items: center;
                              justify-content: center;
                              height: 100vh;
                              margin: 0;
                          }
                          h1 {
                              color: #333;
                              margin-bottom: 20px;
                          }
                          form {
                              background-color: #fff;
                              padding: 20px;
                              border-radius: 8px;
                              box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                          }
                          input[type=file] {
                              margin-bottom: 10px;
                          }
                          input[type=submit] {
                              background-color: #4CAF50;
                              color: white;
                              padding: 10px 15px;
                              border: none;
                              border-radius: 4px;
                              cursor: pointer;
                          }
                          input[type=submit]:hover {
                              background-color: #45a049;
                          }
                      </style>
                  </head>
                  <body>
                      <h1>Upload Image to Count People</h1>
                      <form method="post" enctype="multipart/form-data">
                          <input type="file" name="file" accept="image/*">
                          <input type="submit" value="Upload">
                      </form>
                  </body>
                  </html>'''
        return make_response(html)

    @staticmethod
    def post():
        # Sprawdzenie, czy plik został przesłany
        if 'file' not in request.files:
            return {'error': 'No file part'}, 400

        file = request.files['file']
        if file.filename == '':
            return {'error': 'No selected file'}, 400

        if file:
            try:
                # Czytanie obrazu bezpośrednio z przesłanego pliku
                file_stream = file.read()
                np_img = np.frombuffer(file_stream, np.uint8)
                image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
                image = imutils.resize(image, width=min(500, image.shape[1]))

                # Wykorzystanie globalnego deskryptora HOG do detekcji ludzi
                (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

                # Zwrócenie wyniku za pomocą return
                return {'filename': secure_filename(file.filename), 'peopleCount': len(rects)}, 200
            except Exception as e:
                return {'error': str(e)}, 500


api.add_resource(PeopleCounterDynamicUrl, '/dynamic')
api.add_resource(PeopleCounter, '/')
api.add_resource(PeopleCounterUpload, '/upload')

if __name__ == '__main__':
    app.run(debug=True)
