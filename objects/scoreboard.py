def sortsecond(val):
    return val[1]


class scoreboard:

    def __init__(self):
        self.data = []
        with open("objects/data.scr", "r") as data_file:
            raw_data = data_file.readlines()
            initials = raw_data[0].split(' ')
            scores = raw_data[1].split(' ')

            i = 0
            for initial in initials:
                self.data.append((initial, int(scores[i])))
                i += 1

            self.data.sort(key=sortsecond, reverse=True)

    def update_data(self, initial, score):
        self.data.append((initial, score))
        self.data.sort(key=sortsecond, reverse=True)
        self.data.pop(10)

        with open("data.scr", "w") as data_file:
            raw_initials = ""
            raw_scores = ""
            for instance in self.data:
                raw_initials += instance[0] + " "
                raw_scores += str(instance[1]) + " "
            raw_initials += "\n"

            data_file.write(raw_initials + raw_scores)

    def get_instance(self, index):
        try:
            return self.data[index]
        except IndexError:
            return -1


def main():
    SB = scoreboard()
    print(SB.data)

    print(SB.get_instance(-2))

    SB.update_data("ABC", 100)
    SB.update_data("KEK", 10)
    print(SB.data)


if __name__ == '__main__':
    main()