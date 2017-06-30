#!/usr/bin/env python

from .comment import Comment

class BlockComment(Comment):
    def __init__(self, kwargs={}):
        super(BlockComment, self).__init__(kwargs)
