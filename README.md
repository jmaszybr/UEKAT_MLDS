# UEKAT_MLDS - People Counter
Projekt został opracowany w ramach modułu "Technologie chmurowe" na studiach podyplomowych "Uczenie Maszynowe i Data Science".
### autor:Joanna Maszybrocka 

## Opis
People Counter to aplikacja napisana w języku Python, która wykorzystuje bibliotekę OpenCV oraz algorytm HOG (Histogram of Oriented Gradients) do detekcji ludzi na obrazach. Aplikacja oferuje elastyczne API z różnymi endpointami, umożliwiającymi liczenie osób na obrazach z różnych źródeł.

## Endpointy API

### 1. Liczenie osób na statycznym obrazie
- **Endpoint**: `GET /`
- **Parametry**: Brak. Używa wcześniej zdefiniowanego obrazu (`test01.jpg`).
- **Opis**: Endpoint przetwarza wcześniej zdefiniowany statyczny obraz i zwraca liczbę wykrytych osób.
- **Przykład użycia**:
http://localhost:5000/

### 2. Liczenie osób z obrazu pobranego z URL
- **Endpoint**: `GET /dynamic`
- **Parametry**: `url` - adres URL obrazu do analizy.
- **Opis**: Pobiera obraz z podanego URL, przetwarza go za pomocą HOG i zwraca liczbę wykrytych osób.
- **Przykład użycia**:
http://127.0.0.1:5000/dynamic?url=https://www.fit.pl/img/WELLNESS/_max/nordic_walking.jpg

### 3. Liczenie osób na obrazie, który został przesłany za pomocą formularza
- **Endpoint**: `GET /upload` i `POST /upload`
- **Opis**: `GET /upload` zwraca formularz HTML do przesyłania obrazów. `POST /upload` przyjmuje przesłany obraz, przetwarza go za pomocą HOG i zwraca liczbę wykrytych osób.
- **Parametry (POST)**: `file` - przesłany obraz.
- **Przykład użycia**:
Otwórz `http://localhost:5000/upload` w przeglądarce, aby użyć formularza do przesyłania.


## Detekcja za pomocą HOG
- **Deskryptor HOG**: Używany do ekstrakcji cech z obrazów, które są następnie wykorzystywane do detekcji ludzi.
- **Detektor ludzi**: Wbudowany detektor ludzi w OpenCV, który wykorzystuje HOG do identyfikacji obiektów podobnych do ludzi na obrazie.
- **Parametry**: 
- `winStride`: Krok okna przesuwnego, przyjęto (4, 4).
- `padding`: Padding dla każdego okna, przyjęto (8, 8).
- `scale`: Skala obrazu, przyjęto 1.05.
 
## Format odpowiedzi
Wszystkie endpointy zwracają odpowiedzi w formacie JSON. Przykładowe odpowiedzi:
- Sukces: `{ "filename": nazwa_pliku, "peopleCount": liczba }`
- Błąd: `{ "error": "opis błędu" }`

## Informacje dodatkowe

W Folderze Examples, znajduje się skrypt `detect_people_and_display.py`, który wykorzystuje bibliotekę OpenCV do detekcji osób na obrazach. Skrypt wczytuje obraz, przetwarza go za pomocą deskryptora HOG, a następnie wyświetla oryginalny obraz i obraz z zaznaczonymi wykrytymi osobami, informując o ich liczbie. Jest to narzędzie gotowe do użycia i dostosowania do własnych potrzeb w projektach związanych z przetwarzaniem obrazów i rozpoznawaniem obiektów.

Przykład analizy
![Demo Image](./examples/demo.png)
