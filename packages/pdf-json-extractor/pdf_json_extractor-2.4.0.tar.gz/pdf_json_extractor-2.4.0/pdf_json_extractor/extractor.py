from ._a import _U
from ._b import _B
from ._c import _P

class _X:
    def __init__(self, _p: str = _P):
        self._p = _p
        self._u = _U()
        self._g = _B()

    def _z(self, _f: str) -> dict:
        _d = self._u._x(_f)
        try:
            return self._g._y(_d, self._p)
        finally:
            self._u._z(_d)
