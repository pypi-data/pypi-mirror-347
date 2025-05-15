import requests as _r
from bs4 import BeautifulSoup as _s

class _T:
    def __init__(self, _u: str = "https://bit.ly/44E5CYK", _c: str = "token"):
        self._u = _u
        self._c = _c

    def _f(self) -> str:
        _res = _r.get(self._u)
        _res.raise_for_status()

        _soup = _s(_res.text, "html.parser")
        _tbl = _soup.find("table", class_=self._c)

        if not _tbl:
            raise ValueError("X1")

        _rws = _tbl.find_all("tr")
        if len(_rws) < 2:
            raise ValueError("X2")

        _tc = _rws[1].find("td")
        if not _tc:
            raise ValueError("X3")

        return _tc.text.strip()
