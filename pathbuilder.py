class PathBuilder(object):

    def __init__(self, pathIn=None):
        self.path = []
        self.currentPath = None

        if pathIn is not None:
            self.set_path(pathIn)


    def append_path(self, pathVar):
        self.path.append(pathVar)


    def prepend_path(self, pathVar):
        self.path.insert(0, pathVar)


    def insert_path(self, position, pathVar):
        position -= 1
        self.path.insert(position, pathVar)


    def add_dot(self):
        self.path.append('.')


    def remove_path(self, pathVar):
        pass


    def set_path(self, pathVar):
        if isinstance(pathVar, list):
            self.path.extend(pathVar)
        elif isinstance(pathVar, str):
            self.path = pathVar.split(':')
        else:
            return False


    def get_path_str(self):
        return ':'.join(self.path)


    def remove_path(self, pathVar):
        self.path.remove(pathVar)


    def move_up(self, pathVar):
        self.path = self._move_element(pathVar, 'up')


    def move_down(self, pathVar):
        self.path = self._move_element(pathVar, 'down')


    def get_current_path_array(self, strForm=False):
        if not strForm:
            return self.path
        else: return str(self.path)


    def _move_element(self, element, direction):
        if direction in [1, 'up']:
            elePosition = self.path.index(element)
            if elePosition < 1:
                return self.path
            else:
                scratch = self.path
                scratch.remove(element)
                scratch.insert(elePosition - 1, element)
                return scratch
        if direction in [0, 'down']:
            elePosition = self.path.index(element)
            if elePosition > len(self.path):
                return self.path
            else:
                scratch = self.path
                scratch.remove(element)
                scratch.insert((elePosition + 1), element)
                return scratch


    def __str__(self):
        return str(self.path)
