from bs4 import BeautifulSoup

import os
import codecs


MAPPING = {
    "code":2,
    "title":3,
    "people":4,
    "organization":5
}


def main():
    in_dir = r"/Users/liuyang/Desktop/nsfc" # html
    out_file = in_dir + os.sep + "out.csv" # csv
    htmls = get_all_html(in_dir)
    data = []
    for h in htmls:
        data.extend(get_proj_info_from_html(in_dir + os.sep + h))
    # data to csv
    write_to_csv(data, out_file)



def get_all_html(dir):
    files = os.listdir(dir)
    return filter(lambda f: f.endswith(".htm"), files)


def get_proj_info_from_html(h_file):
    with codecs.open(h_file, encoding="utf8", mode="r") as f:
        soup = BeautifulSoup(f.read())
        tables = soup.find_all("table", {"id":"dataGrid"})
        if len(tables) <= 0:
            return
        ret = []
        trs = tables[0].find_all("tr")
        for tr in trs[1:]:
            tds = tr.find_all("td")
            one_row = {}
            for k, v in MAPPING.items():
                one_row[k] = tds[v].string
            ret.append(one_row)
        return ret


def write_to_csv(data, o_file):
    titles = MAPPING.keys()
    with codecs.open(o_file, mode="w", encoding="utf8") as f:
        # first row
        f.write(",".join(titles))
        f.write("\n")
        for d in data:
            strs = []
            for t in titles:
                strs.append(d[t])
            f.write(",".join(strs))
            f.write("\n")
        f.close()


if __name__ == '__main__':
    main()