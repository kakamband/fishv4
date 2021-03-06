#!/usr/bin/python

import cv2 as cv
import numpy as np
import pandas as pd
import streamlit as st

from utils import yolov4 as yolo
from utils import GrabCut
from utils.draw_rectanges import draw_rectangles


def run():
    yolopath = "./fishv4"
    confidence = 0.30
    threshold = 0.40

    st.title("Fishv4[tiny] Demo 2020")
    st.text("Repo from: https://fishv4.herokuapp.com/")
    st.text("More info: https://github.com/DZPeru/fishv4")

    uploaded_img = st.file_uploader("Elige una imagen compatible", type=[
                                    'png', 'jpg', 'bmp', 'jpeg'])
    if uploaded_img is not None:
        file_bytes = np.asarray(bytearray(uploaded_img.read()), dtype=np.uint8)
        image = cv.imdecode(file_bytes, 1)

        st.write("This is your uploaded image:")
        st.image(image, caption='Uploaded Image', channels="BGR", use_column_width=True)

        boxes, idxs = yolo.runYOLOBoundingBoxes_streamlit(image, yolopath, confidence, threshold)
        st.write(pd.DataFrame.from_dict({'confidence' : [confidence],
                                        'threshold' : [threshold],
                                        'Encontrados (Boxes)': [len(boxes)],
                                        'Válidos (idxs)': [len(idxs)],}))
        result_images = GrabCut.runGrabCut(image, boxes, idxs)


        st.write("Here appears the rectangles that the algorithm recognize:")
        
        img_mod=draw_rectangles(image,boxes,idxs)

        st.image(img_mod, channels="BGR", use_column_width=True)

        st.write("")
        st.write("finish grabcut")
        st.write(f"There are {len(result_images)} segmented fish image. Each listed as below:")
        for i in range(len(result_images)):
            #cv.imwrite(f'grabcut{i}.jpg', result_images[i])
            st.image(result_images[i], channels="BGR", use_column_width=True)

if __name__ == '__main__':
    run()