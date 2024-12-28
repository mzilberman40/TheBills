from collections import namedtuple


ParamBase = namedtuple('ParamBase', ['field_name', 'key'])
class Param(ParamBase):
    def __bool__(self):
        return bool(self.field_name and self.key)