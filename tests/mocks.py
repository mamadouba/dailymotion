class MockRedis:
    def __init__(self, cache={}) -> None:
        self.cache = cache

    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        return None

    def set(self, key, val):
        self.cache[key] = val


class MockSMTPClient:
    def sendmail(self):
        print("mail sent")

    def close(self):
        print("smtp client closed")
