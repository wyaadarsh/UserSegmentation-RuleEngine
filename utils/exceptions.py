from logging import getLogger

logger = getLogger(__name__)


class BaseError(Exception):
    def __init__(self, args):
        logger.exception(args)
        super(BaseError, self).__init__(args)
        print(args)


class InvalidRuleException(BaseError):

    def __init__(self):
        errorString = "Invalid Rule"
        errorCode = 410
        arg = {"code": errorCode, "Description": errorString}
        super(InvalidRuleException, self).__init__(arg)


class InvalidArgumentException(BaseError):

    def __init__(self, arg):
        errorString = "Invalid Argument: {}".format(arg)
        errorCode = 410
        arg = {"code": errorCode, "Description": errorString}
        super(InvalidArgumentException, self).__init__(arg)


class IDNeededException(BaseError):

    def __init__(self):
        errorString = "Unique id needed:"
        errorCode = 410
        arg = {"code": errorCode, "Description": errorString}
        super(IDNeededException, self).__init__()
