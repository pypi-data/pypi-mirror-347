import json
import google.generativeai as _g

class _B:
    def __init__(self):
        self._m = _g.GenerativeModel(model_name="gemini-1.5-flash")

    def _y(self, _f, _p: str) -> dict:
        try:
            _r = self._m.generate_content([_f, _p])
            _t = _r.text.replace("\n", ' ').replace("```json", '').replace("```", '').strip()
            return json.loads(_t)
        except Exception as _e:
            raise Exception(f"Parsing failed: {_e}")
