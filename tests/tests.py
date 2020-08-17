from speak_to_file.speak_to_file import *
import unittest

logger = logging.getLogger(__name__)
logger.warning("Boop")

class ReplaceInvalidCharsTestCase(unittest.TestCase):
    def test_invalid_chars(self):
        input_chars = """<>:"\|?*"""
        self.assertEqual("", replace_invalid_chars(input_chars))
        
class GlueArgsTestCase(unittest.TestCase):
    def test_glue_args(self):
        fun_input = {'-hide_banner': True, '-i': 'pipe:0',  '-c:a': 'libvorbis',  '-q:a': '1', '-ac': '1', '-ar': '22050', '-y': True}
        fun_output = ['-hide_banner', '-i', 'pipe:0', '-c:a', 'libvorbis', '-q:a', '1', '-ac', '1', '-ar', '22050', '-y']
        self.assertEqual(fun_output, glue_args(fun_input))

class SplitArgsTestCase(unittest.TestCase):
    def test_split_args(self):
        fun_input = "-hide_banner=,-i=pipe:0,-c:a=libvorbis,-q:a=1,-ac=1,-ar=22050,-y="
        fun_output = {'-hide_banner': True, '-i': 'pipe:0',  '-c:a': 'libvorbis',  '-q:a': '1', '-ac': '1', '-ar': '22050', '-y': True}
        self.assertEqual(fun_output, split_args(fun_input))

class ReadStdInTestCase(unittest.TestCase):
    pass

class ExecuteReadConvertTestCase(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
