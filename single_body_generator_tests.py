import single_body_generator
import unittest

class TestDateHandling(unittest.TestCase):

    def test_error_handling(self):
        """
        convert_date_to_time takes a string as an input, triest to parse the string as a DateTime object.
        If the function is able to parse the string successfully, it returns a DateTime object, if it fails, it returns None
        :return:
        """
        self.assertEqual(None, single_body_generator.convert_to_date_time(''))
        self.assertEqual(None, single_body_generator.convert_to_date_time('Hello'))
        self.assertEqual(None, single_body_generator.convert_to_date_time('13/12/2000 111111'))

    def test_date_parsing(self):
        self.assertEqual('1990-06-25', str(single_body_generator.convert_to_date_time('06/25/1990 20').date()))



if __name__ == '__main__':
    unittest.main()
