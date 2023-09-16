import unittest
import cv2


# Load the test data
def load_image_data():
    input_image = cv2.imread("error.jpg")
    
    image_shape = input_image.shape
    return str(image_shape[0])

# check if the transfered image has width of 360px
class TestAdd(unittest.TestCase):
    def test_add(self):
        actual = load_image_data()
        expected = "3160"
        self.assertNotEqual(actual, expected)