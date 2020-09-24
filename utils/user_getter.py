from utils.getter_setter import rgetattr, rsetattr


class UserGetter:
    def __init__(self, user_data):
        self.user_data = DotDict(user_data)

    def get_entity(self, entity):
        val = self.user_data.get(entity)
        if not val:
            val = rgetattr(self.user_data, entity, None)
        return val

    def set_entity(self, entity):
        # return self.user_data.set(entity)
        rsetattr(self, self.user_data, entity)
        return self.user_data


class DotDict(dict):
    """
    a dictionary that supports dot notation
    as well as dictionary access notation
    usage: d = DotDict() or d = DotDict({'val1':'first'})
    set attributes: d.val2 = 'second' or d['val2'] = 'second'
    get attributes: d.val2 or d['val2']
    """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, dct):
        for key, value in dct.items():
            if hasattr(value, 'keys'):
                value = DotDict(value)
            self[key] = value


