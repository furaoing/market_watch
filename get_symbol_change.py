import requests
import string
import re


def remove_whitespce(text):
    for c in string.whitespace:
        text = text.replace(c, "")
    return text


def reformat_date(date_text):
    sep = r"/"
    split_result = date_text.split(sep)
    month = split_result[0]
    date = split_result[1]
    year = split_result[2]
    return "%s-%s-%s" % (year, month, date)


def get_symbol_change():
    url = r"https://www.nasdaq.com/markets/stocks/symbol-change-history.aspx"

    content = requests.get(url).text
    html_content = remove_whitespce(content.lower())
    pattern = '<tr><tdclass="body2">(.+?)</td><tdclass="body2"><aid="two_column_main_content_rptsymbols_newsymbol_.*?"href=".+?">(.+?)</a></td><tdclass="body2">(.+?)</td>'

    pattern = remove_whitespce(pattern)
    result = re.findall(pattern, html_content)

    records = []
    for x in result:
        old_symbol = x[0]
        new_symbol = x[1]
        effective_date = x[2]
        reformat_effective_date = reformat_date(effective_date)
        records.append([old_symbol, new_symbol, reformat_effective_date])
    return records


print(get_symbol_change())

