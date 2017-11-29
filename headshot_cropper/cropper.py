import numpy as np
import os
import cv2

extra_dimensions_percent = 0.3
show_window = False
draw_face_box = False

face_cascade = cv2.CascadeClassifier('xml/haarcascade_frontalface_default.xml')


def cropper(files):
    for current_file in files:
        img = cv2.imread('inputs/' + current_file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            if draw_face_box:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        (x, y, w, h) = faces[0]
        max_dim = max(w, h)
        extra_dimensions = int(max_dim * extra_dimensions_percent)

        headshot = img[y-extra_dimensions:y+max_dim+extra_dimensions, x-extra_dimensions:x+max_dim+extra_dimensions]
        height, width = headshot.shape[:2]

        cv2.imwrite("outputs/" + current_file, headshot)
        if show_window:
            cv2.imshow('img', cv2.resize(headshot, (width // 4, height //4)))
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        print "Cropped %s" % current_file

if __name__ == '__main__':
    print "Started Cropper"
    cropper(os.listdir("inputs"))
    print "Cropping Complete"
