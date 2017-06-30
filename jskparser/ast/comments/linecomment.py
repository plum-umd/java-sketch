#!/usr/bin/env python

from .comment import Comment

class LineComment(Comment):
    def __init__(self, kwargs={}):
      super(LineComment, self).__init__(kwargs)
