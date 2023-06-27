class Item:
    '''Base Item Class for common list page'''
    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        self._file = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def abstract(self):
        return self._abstract
    
    @abstract.setter
    def abstract(self, value):
        self._abstract = value

    @property
    def addition(self):
        return self._addition
    
    @addition.setter
    def addition(self, value):
        self._addition = value

    @property
    def previous(self):
        return self._previous
    
    @previous.setter
    def previous(self, value):
        self._previous = value

    @property
    def next(self):
        return self._next
    
    @next.setter
    def next(self, value):
        self._next = value

