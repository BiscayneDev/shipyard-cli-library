import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location('capture_check', pathlib.Path(__file__).with_name('check.py'))
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

class CaptureHygieneTests(unittest.TestCase):
    def test_fictional_example_allowed(self):
        self.assertEqual(list(check.issues('{"securityToken":"FICTIONAL_NOT_A_CREDENTIAL"}')), [])

    def test_sensitive_capture_rejected_without_value_in_diagnostic(self):
        result = list(check.issues('{"securityToken":"made-up-sensitive-test-only"}'))
        self.assertEqual(result, ['non-fictional sensitive response field'])
        self.assertNotIn('made-up-sensitive-test-only', str(result))

    def test_jwt_shape_rejected(self):
        self.assertTrue(list(check.issues('eyJmaWN0aW9uYWwi.dGVzdA.ZmljdGlvbmFs')))

if __name__ == '__main__':
    unittest.main()
