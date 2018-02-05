import unittest

if __name__ == "__main__":
    test_loader = unittest.defaultTestLoader
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_suite = test_loader.discover("test", pattern="*tests.py")
    test_runner.run(test_suite)

