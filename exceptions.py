class UnknownSymbol(BaseException):
    pass


class DataIncomplete(BaseException):
    pass


class TooManyRequest(BaseException):
    pass


class HttpStatusCodeOtherThan200(BaseException):
    pass


class InValidJson(BaseException):
    pass


class JsonFieldMissing(BaseException):
    pass


class IBShortDataFileFormatException(BaseException):
    pass