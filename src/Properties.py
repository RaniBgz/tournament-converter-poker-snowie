# Static class reading properties file and then storing every elements as attributes to be used


class Properties:
    properties = {}

    @classmethod
    def init(cls):
        with open("conf.properties") as property_file:
            for line in property_file:
                k, v = line.split('=')
                if v[-1] == "\n":
                    v = v[:-1]
                cls.properties[k] = v


if __name__ == "__main__":
    Properties.init()
    print(Properties.properties)
