import cv2
import imutils


def detect_people_and_display(image_path, winstride=(4, 4), padding=(8, 8), scale=1.05):
    # Wczytanie obrazu
    image = cv2.imread(image_path)
    image = imutils.resize(image, width=min(500, image.shape[1]))
    original_image = image.copy()

    # Inicjalizacja deskryptora HOG / detektora ludzi
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Wykrywanie ludzi na obrazie z użyciem podanych parametrów
    (rects, weights) = hog.detectMultiScale(image, winStride=winstride, padding=padding, scale=scale)

    # Rysowanie prostokątów dookoła wykrytych ludzi
    for (x, y, w, h) in rects:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Wyświetlanie oryginalnego obrazu
    cv2.imshow("Original Image", original_image)

    # Wyświetlanie obrazu po detekcji
    cv2.imshow("After Detection", image)

    # Wyświetlanie ilości wykrytych ludzi
    print("Ilość osób: {}".format(len(rects)))

    # Czekanie na naciśnięcie klawisza, aby zamknąć okna
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Przykładowe użycie funkcji z niestandardowymi parametrami HOG
detect_people_and_display('test06.png', winstride=(4, 4), padding=(8, 8), scale=1.05)
