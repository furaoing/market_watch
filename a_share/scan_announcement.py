kw_list = ["白酒"]  # 战略入股
def scan_kw(content):
    span = 30
    for kw in kw_list:
        result = content.find(kw)
        if result > -1:
            return content[result-span:result+span]
    return None

def clean_content(content):
    kws = ["\s", "\r", "\n"]
    for kw in kws:
        content = content.replace(kw, "")
    return content

def load_stock_list(f_name):
    stock_code_list = []
    content = read(f_name,encoding = 'utf-8')
    lines = content.split("\r\n")
    for line in lines:
        line = line.strip()
        stock_code_list.append(line)
    return stock_code_list

def sec_name_lookup(stock_code):
    s = DataAPI.EquGet(secID=u"",ticker=stock_code,equTypeCD=u"A",listStatusCD=u"",exchangeCD="",ListSectorCD=u"",field=u"secShortName",pandas="1")
    return s.iloc[0]["secShortName"]

def process_one_stock(stock_code, beginDate):
    d = DataAPI.ReportContentGet(ticker=stock_code,beginDate=beginDate,endDate=u"",field=u"",pandas="1")
    results = []
    for i in d.index:
        one_record = d.iloc[i]
        content = str(one_record["txtContent"])
        content = clean_content(content)
        title = str(one_record["title"])
        reportType = str(one_record["reportType"])
        kw_found = scan_kw(content)
        if kw_found:
            stock_name = sec_name_lookup(stock_code)
            result = [stock_code, stock_name, title, kw_found, reportType]
            results.append(result)
    return results

def process_one_stock_abstract(stock_code, beginDate):
    d = DataAPI.ReportAbstractGet(beginDate=beginDate,endDate=u"",ticker=stock_code,reportID=u"",field=u"",pandas="1")
    results = []
    for i in d.index:
        one_record = d.iloc[i]
        abstract = str(one_record["abstract"])
        title = str(one_record["title"])
        if title == u"nan":
            continue
        zsAutoCategory = str(one_record["zsAutoCategory"])
        kw_found = scan_kw(abstract)
        if kw_found:
            stock_name = sec_name_lookup(stock_code)
            result = [stock_code, stock_name, title, kw_found, zsAutoCategory]
            results.append(result)
    return results

stock_code_list = load_stock_list("stock_code_list.txt")
begin_date = u"20210709"
for stock_code in stock_code_list:
    results = process_one_stock(stock_code, begin_date)
    for result in results:
        print("公司名称：%s，     公告标题：%s，      摘要： %s" % (result[1], result[2], result[-2]))
print("------------")
print("运行完毕")


