import unittest
import cv2

# Load the test data
def load_image_data():
    input_image = cv2.imread("error.jpg")
    
    image_shape = input_image.shape
    return str(image_shape)

# check if the transfered image has width, height and depth of 360px, 462, 3
class TestAdd(unittest.TestCase):
    def test_add(self):
        actual = load_image_data()
        expected = "(360, 462, 3)"
        self.assertEqual(actual, expected)