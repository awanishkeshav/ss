from json import JSONEncoder


class SSJson(JSONEncoder):

    def default(self, o):
        return o