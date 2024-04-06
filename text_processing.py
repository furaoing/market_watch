def or_test(flags):
    tmp_flag = False
    for flag in flags:
        tmp_flag = tmp_flag or flag
    return tmp_flag


def must_test(flags):
    tmp_flag = True
    for flag in flags:
        tmp_flag = tmp_flag and flag
    return tmp_flag


def generate_news_label(record):
    title = record["title"].lower()
    summary = record["summary"].lower()
    text = title + " " + summary
    label_found = []

    label_kws = {"trial_result_to_present": {"must": ["phase", "to present"]},
                 "trial_result_announcement": {"must": ["phase", "trial"]},
                 "pharma": {"or": ["pharma", "therape", "biotech"]},
           "M&A": {"or": ["tender offer", "definitive agreement", "proposal", "merger"]},
                 "strategic alternatives": {"must": ["strategic alternatives"]},
           "contract": {"must": ["contract"]},
           }

           # "M&A": {"or": ["tender offer", "definitive agreement", "proposal", "merger"]},
           #       "sentiment": {"or": ["positive", "surge", "approval"]},
           #       "commercialization": {"or": ["launch", "commercial"]},
           #       "strategic alternatives": {"must": ["strategic alternatives"]}


    #label_kws = {
    #       "M&A": {"or": ["tender offer", "definitive agreement", "proposal", "merger"]}
                 #"strategic alternatives": {"must": ["strategic alternatives"]}
    #       }

    for label, condition in label_kws.items():
        if "must" in condition.keys():
            must_keys = condition["must"]
            test_flags = []
            for key in must_keys:
                if key in text:
                    test_flags.append(True)
                else:
                    test_flags.append(False)

            if must_test(test_flags):
                label_found.append(label)

        if "or" in condition.keys():
            or_keys = condition["or"]
            test_flags = []
            for key in or_keys:
                if key in text:
                    test_flags.append(True)
                else:
                    test_flags.append(False)

            if or_test(test_flags):
                label_found.append(label)
    return label_found


def generate_pharma_news_label(record):
    title = record["title"].lower()
    summary = record["summary"].lower()
    text = title + " " + summary
    label_found = []

    label_kws = {"pharma": {"must": ["phase", "trial"], "or": ["pharma", "therape", "biotech"]},
           "contract": {"must": ["contract"]},
           "M&A": {"or": ["tender offer", "definitive agreement", "proposal", "merger"]},
                 "sentiment": {"or": ["positive", "surge", "approval"]},
                 "commercialization": {"or": ["launch", "commercial"]},
                 "strategic alternatives": {"must": ["strategic alternatives"]}
           }

    for label, condition in label_kws.items():
        if "must" in condition.keys():
            must_keys = condition["must"]
            test_flags = []
            for key in must_keys:
                if key in text:
                    test_flags.append(True)
                else:
                    test_flags.append(False)

            if must_test(test_flags):
                label_found.append(label)

        if "or" in condition.keys():
            or_keys = condition["or"]
            test_flags = []
            for key in or_keys:
                if key in text:
                    test_flags.append(True)
                else:
                    test_flags.append(False)

            if or_test(test_flags):
                label_found.append(label)
    return label_found