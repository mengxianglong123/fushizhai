class Result:
    """
    最终响应结果
    """
    code: int
    message: str
    data: object

    def __init__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.message,
            "data": self.data
        }
