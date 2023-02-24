"""Python Class for handling the Movies endpoint"""
from tor import base

class Movies(base._TORResource):
    
    RESOURCE = 'movie'
    SUB_RESOURCES = ['quote']

    def __init__(self, quotes=False, **kwargs):
        super().__init__(**kwargs)
        if quotes:
            self.sub_resource = 'quote'