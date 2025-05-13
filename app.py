import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image

# Load model
def load_model():
    model = tf.keras.models.load_model("model/mobilenetV2/mobilenetv2_ft.h5", compile=False) 
    return model

model = load_model()

# Prediction function
def predict_image(file):
    classes = {'Coccidiosis': 0, 'Healthy': 1, 'NewCastleDisease': 2, 'Salmonella': 3}
    
    # Open the uploaded file
    img = Image.open(file.name)
    img = img.resize((128, 128))
    
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array*1/255.)
    score = tf.nn.softmax(predictions[0])
    pred_class = [j for j in classes if classes[j] == np.argmax(score)][0]
    confidence = round(100 * np.max(score), 2)
    
    return {pred_class: confidence}

# Gradio interface with file uploader
title = "Poultry Diseases Identifier 🐣🐓💩 App Using Machine Learning"
description = """
You can check your poultry bird's health via Poultry Disease Identifier. 
This app helps to detect unhealthy diseases such as Coccidiosis, Salmonella, 
and Newcastle from image files of chicken feces.
"""

app = gr.Interface(
    fn=predict_image,
    inputs=gr.File(label="Upload Image", file_types=["image"]),
    outputs=gr.Label(num_top_classes=4),
    title=title,
    description=description,
    allow_flagging="never"
)

app.launch(share=True)