# 业务异常 处理器
class BusinessException(Exception):
    code: int
    message: str

    def __init__(self, message: str, code: int = 500):
        self.message = message
        self.code = code
        super().__init__(self.message)
