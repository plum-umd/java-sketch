# http://code.activestate.com/recipes/65207

class _const:
  class ConstError(TypeError): pass
  def __setattr__(self, name, v):
    if self.__dict__.has_key(name):
      raise self.ConstError, "Can't rebind const(%s)" % name
    self.__dict__[name] = v

import sys
sys.modules[__name__] = _const()

"""
# that's all -- now any client-code can
import const
# and bind an attribute ONCE:
const.magic = 23
# but NOT re-bind it:
const.magic = 88      # raises const.ConstError
# you may also want to add the obvious __delattr__
"""
