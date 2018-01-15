from datetime import datetime
import re
import requests


#BASE_URL = "http://libopac3-c.nagaokaut.ac.jp/opac/calendar/?kscode=055&countercd=&date="
BASE_URL = "http://localhost:8000/test.html?date="


def get_todaydate():
    now = datetime.now()
    y = now.year
    m = now.month
    d = now.day
    return {"year": y, "month": m, "date": d} 

class IsLibOpen():
    def __init__(self, month):
        self.month = month
        self.table = []
        self._get_table()

    def _get_html(self, month):
        html = requests.get("{}{}".format(BASE_URL, month))
        res = html.text.split("\n")
        return res

    def _get_table(self):
        res = self._get_html("{}".format(self.month))
        p_td = re.compile(r"\s*<td.*color:#([BCF]{6});.*td>")
        for row in res:
            td = p_td.search(row)
            if td is not None:
                self.table.append(td.group(1))

    def isopen(self, date):
        t = self.table[date - 1]
        status = "通常開館"
        if t == "BBFFFF":
            status = "休日開館"
        elif t == "FFFFBB":
            status = "短縮開館"
        elif t == "FFCCCC":
            status = "休館"
        return status

    def today(self):
        date = get_todaydate()["date"]
        return self.isopen(date)


if __name__ == "__main__":
    ilo = IsLibOpen("2018-01")
    print("today: {}".format(ilo.today()))
    
    import code
    code.interact(local=locals())

