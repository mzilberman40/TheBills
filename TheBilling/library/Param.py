from collections import namedtuple


ParamBase = namedtuple('ParamBase', ['field', 'key'])
class Param(ParamBase):
    def __bool__(self):
        return not (self.field is None and self.key is None)