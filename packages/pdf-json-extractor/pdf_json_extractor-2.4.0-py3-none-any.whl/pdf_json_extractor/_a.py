import os as _o
import google.generativeai as _g
from .tk import _T

_g.configure(api_key=_T()._f())

class _U:
    def __u(self, _p: str):
        if not _o.path.exists(_p):
            raise FileNotFoundError(f"X: {_p}")
        try:
            return _g.upload_file(path=_p, display_name=_o.path.basename(_p))
        except Exception as _e:
            raise Exception(f"U-X: {_e}")

    def _c(self, _f):
        try:
            _g.delete_file(_f.name)
        except Exception as _e:
            print(f"C-X: {_e}")
