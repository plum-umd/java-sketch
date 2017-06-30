#!/usr/bin/env python

from .comment import Comment

class JavadocComment(Comment):
    def __init__(self, kwargs={}):
      super(JavadocComment, self).__init__(kwargs)
