def RISE_Check(price_series):
    if price_series[-1]/price_series[-2] > 1:
        RiseFlag = True
    else:
        RiseFlag = False

    return RiseFlag


def RS_T0_Check(price_series):
    if price_series[1]/price_series[0] > 1.5:
        GrowthFlag = True
    else:
        GrowthFlag = False

    return GrowthFlag


def RS_T1_Pre_Check(price_series):
    # Check 3 days growth
    flag_a = False
    flag_b = False
    if price_series[1] / price_series[0] > 1.2:
        flag_a = True
    if price_series[2] / price_series[1] > 1.05:
        flag_b = True
    AlwaysIncreaseFlag = flag_a and flag_b

    return AlwaysIncreaseFlag


def RS_T1_Check(price_series):
    # Check 3 days growth
    AlwaysIncreaseFlag = True
    for i in range(len(price_series) - 1):
        # Consecutive growth with a growth rate no less than 20% for three days
        if price_series[i + 1] > price_series[i]:
            pass
        else:
            AlwaysIncreaseFlag = False
            break
        if price_series[i + 1] / price_series[i] > 1.2:
            pass
        else:
            AlwaysIncreaseFlag = False
            break

    #  End closing price at least 50% increase compared to Start closing price
    if price_series[-1]/price_series[0] > 1.5:
        GrowthFlag = True
    else:
        GrowthFlag = False

    return AlwaysIncreaseFlag and GrowthFlag


def RS_T2_Check(price_series):
    # Check 5 days growth
    AlwaysIncreaseFlag = True
    for i in range(len(price_series) - 1):
        # Consecutive growth with a growth rate no less than 5% for three days
        if price_series[i + 1] > price_series[i]:
            pass
        else:
            AlwaysIncreaseFlag = False
            break
        if price_series[i + 1] / price_series[i] > 1.05:
            pass
        else:
            AlwaysIncreaseFlag = False
            break

    #  End closing price at least 90% increase compared to Start closing price
    if price_series[-1]/price_series[0] > 1.9:
        GrowthFlag = True
    else:
        GrowthFlag = False

    return AlwaysIncreaseFlag and GrowthFlag


def RS_T3_Check(price_series):
    if price_series[1]/price_series[0] > 1.3:
        GrowthFlag = True
    else:
        GrowthFlag = False

    return GrowthFlag


def RS_T4_Check(price_series):
    # 3 days growth in a row
    AlwaysIncreaseFlag = True
    for i in range(len(price_series) - 1):
        # Consecutive growth with a growth rate no less than 5% for three days
        if price_series[i + 1] > price_series[i]:
            pass
        else:
            AlwaysIncreaseFlag = False
            break
        if price_series[i + 1] / price_series[i] > 1.05:
            pass
        else:
            AlwaysIncreaseFlag = False
            break

    #  End closing price at least 20% increase compared to Start closing price
    if price_series[-1]/price_series[0] > 1.3:
        GrowthFlag = True
    else:
        GrowthFlag = False

    return AlwaysIncreaseFlag and GrowthFlag
