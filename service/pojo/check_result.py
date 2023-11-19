class CheckResult:
    '''
    单字校验结果实体类
    '''
    row: int = -1  # 行号
    column: int = -1  # 列号
    is_pingze_err: bool = False  # 平仄错误
    is_meter_err: bool = False  # 韵律错误
    suggests: list = []  # 修改意见

    def __init__(self, row, column, is_pingze_err, is_meter_err, suggests):
        self.row = row
        self.column = column
        self.is_pingze_err = is_pingze_err
        self.is_meter_err = is_meter_err
        self.suggests = suggests


