from utils.getter_setter import rgetattr, rsetattr


class UserGetter:
    def __init__(self, user_data):
        self.user_data = user_data

    def get_entity(self, entity):
        return rgetattr(self.user_data, entity, None)

    def set_entity(self, entity):
        rsetattr(self, self.user_data, entity)
        return self.user_data

