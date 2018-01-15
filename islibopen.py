from datetime import datetime
import re
import requests


BASE_URL = "http://libopac3-c.nagaokaut.ac.jp/opac/calendar/?kscode=055&countercd=&date="
#BASE_URL = "http://localhost:8000/test.html?date="


def get_todaydate():
    now = datetime.now()
    y = now.year
    m = now.month
    d = now.day
    return {"year": y, "month": m, "date": d} 


class IsLibOpen():
    def __init__(self, year=None, month=None):
        dd = get_todaydate()
        self.thismonth = "{0:04d}-{1:02d}".format(dd["year"], dd["month"])
        self.month = None
        if year and month:
            self.month = "{0:04d}-{1:02d}".format(year, month)
        self.table = []

        self._get_table()

    def _get_html(self):
        month = self.month
        if month == None:
            month = self.thismonth
        html = requests.get("{}{}".format(BASE_URL, month))
        res = html.text.split("\n")
        return res

    def _get_table(self):
        res = self._get_html()
        p_td = re.compile(r"\s*<td.*color:#([BCF]{6});.*td>")
        for row in res:
            td = p_td.search(row)
            if td is not None:
                self.table.append(td.group(1))

    def isopen(self, date=None):
        if date is None:
            dd = get_todaydate()
            if self.month is None or self.month == self.thismonth:
                date = dd["date"]

        status = ""
        try:
            t = self.table[date - 1]
            if t == "FFFFFF":
                status = "通常開館"
            elif t == "BBFFFF":
                status = "休日開館"
            elif t == "FFFFBB":
                status = "短縮開館"
            elif t == "FFCCCC":
                status = "休館"
        except:
            status = "取得できませんでした"
        return status


if __name__ == "__main__":
    """FORMAT:
    ilo = IsLibOpen({year}, {month}) # if empty: this month
    status = ilo.isopen({date}) # if empty: today(need instance for this month)
    """

    # today
    ilo = IsLibOpen()
    print("today: {}".format(ilo.isopen()))

    import code
    code.interact(local=locals())

