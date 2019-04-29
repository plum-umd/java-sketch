# http://code.activestate.com/recipes/65207

from __future__ import absolute_import
class _const:
  class ConstError(TypeError): pass
  def __setattr__(self, name, v):
    if name in self.__dict__:
      raise self.ConstError("Can't rebind const(%s)" % name)
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
