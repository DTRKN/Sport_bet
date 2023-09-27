class Data_handling:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, lst_pub=None,
                       dict_pub=None):

        if lst_pub is None:
            self.lst_pub = []
        else:
            self.lst_pub = lst_pub

        if dict_pub is None:
            self.dict_pub = {}
        else:
            self.dict_pub = dict_pub

    async def append(self, mess_body):
        self.lst_pub.append(mess_body)
        print(mess_body)
        return self.lst_pub


    async def format(self) -> dict:

        strings = str(self.lst_pub).split('Event(')[1:]
        j = 0
        for item in strings:
            item = item.strip().rstrip(", ").split(", ")
            temp_dict = {}
            for i in item:
                if '=' in i:
                    key, value = i.split("=")
                    if key == 'coefficient':
                        value = value.split("'")
                        temp_dict[key] = value[1]
                    else:
                        temp_dict[key] = value

                    if len(temp_dict) == 4:
                        j += 1
                        self.dict_pub[str(j)] = temp_dict
        return self.dict_pub

    async def clear(self):
        self.lst_pub.clear()

    async def get_dict(self):
        return self.dict_pub