class Signal(object):
    RS_T0 = "RS_T0"
    RS_T1 = "RS_T1"
    RS_T1_Pre_Check = "RS_T1_Pre_Check"
    RS_T2 = "RS_T2"
    RS_T3 = "RS_T3"
    RS_T4 = "RS_T4"

    DS_T0 = "DS_T0"
    DS_T1 = "DS_T1"
    DS_T2 = "DS_T2"
    DS_T3 = "DS_T3"

    RISE = "RISE"
    DROP = "DROP"

    VOLUME_T0 = "VOLUME_T0"


class DataRequestType(object):
    HistoryPrice = "HistoryPrice"
    IntraDayPrice = "IntraDayPrice"
    PreviousDayPrice = "PreviousDayPrice"
    Quote = "Quote"
    Stat = "Stat"
    EarningRelease = "EarningRelease"


class ValidationResultType(object):
    UnknownSymbol = "UnknownSymbol"
    Normal = "Normal"
    InValidJson = "InValidJson"


class TickerType(object):
    Pharma = "Pharma"
    NonPharmaGeneral = "NonPharmaGeneral"
    General = "General"
    NonPharmaChinaGeneral = "NonPharmaChinaGeneral"


class TimeConversion(object):
    SEC = 1
    MIN = SEC*60
    HOUR = MIN*60
    DAY = HOUR*24


class ImportantLevel(object):
    IMPORTANT = "IMPORTANT"


class NewsSource(object):
    GlobalNewswire = "GlobalNewswire"
    PRNewswire = "PR Newswire"
    BaiduNews = "BaiduNews"


MillisecondsPerSecond = 1000


if __name__ == "__main__":
    print(TimeConversion.HOUR)