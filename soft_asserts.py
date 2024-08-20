class SoftAssert:
    def __init__(self):
        self.errors = []

    def assert_equal(self, actual, expected, message):
        if actual != expected:
            self.errors.append(f'Assertion failed: {message}. Expected {expected}, but got {actual}.')

    def assert_no_errors(self):
        if self.errors:
            raise AssertionError('\n'.join(self.errors))