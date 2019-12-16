class Settings:
    def __init__(self):
        self.settings = {}
        self.load()

    def load(self):
        settings = open("data/settings.txt", "r")
        for line in settings.readlines():
            name, value = line.split(" ")
            if value == "True":
                value = True
            elif value == "False":
                value = False
            self.settings[name] = value

    def __getattr__(self, item):
        if item == "settings":
            return object.__getattribute__(self, item)
        return self.settings[item]

    def __setattr__(self, key, value):
        if key == "settings":
            return object.__setattr__(self, key, value)
        self.settings[key] = value
        print(self.settings)
        settings = open("data/settings.txt", "w")
        settings.write("\n".join(["{} {}".format(n, str(v)) for n, v in self.settings.items()]))
