from PIL import Image
import tensorflow as tf
import numpy as np


class ImageProcessor:
    """ImageProcessor class for Telegram Bot"""
    model = tf.keras.applications.MobileNetV2(weights='imagenet')

    @staticmethod
    def preprocess_image(image):
        """Preprocessor of an image"""
        image = image.resize((224, 224))
        image = np.array(image)
        image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
        image = np.expand_dims(image, axis=0)
        return image

    @staticmethod
    def predict_image(image_path):
        """Predictor of an image"""
        image = Image.open(image_path)
        preprocessed_image = ImageProcessor.preprocess_image(image)
        predictions = ImageProcessor.model.predict(preprocessed_image)
        decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
        return decoded_predictions
