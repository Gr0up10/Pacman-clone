import os


class ScoreBoard:

    def __init__(self):
        self.data = []

        try:
            data_file = open("binaries/data.score", "r")
            raw_data = data_file.readlines()
            initials = raw_data[0].split(' ')
            scores = list(map(int, raw_data[1].split(' ')))

        except FileNotFoundError:
            os.mkdir("binaries/")
            data_file = open("binaries/data.score", "w+")
            initials = ["---"]*10
            scores = [0]*10
            data_file.write("--- --- --- --- --- --- --- --- --- ---" + '\n' +
                            "0 0 0 0 0 0 0 0 0 0")

        i = 0
        for initial in initials:
            self.data.append((initial, scores[i]))
            i += 1

            self.data.sort(key=lambda a: a[1], reverse=True)

            data_file.close()

    def update_data(self, initial, score):
        self.data.append((initial, score))
        self.data.sort(key=lambda a: a[1], reverse=True)
        self.data.pop(10)

        with open("binaries/data.score", "w") as data_file:
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
    SB = ScoreBoard()

    SB.update_data("ABC", 100)
    SB.update_data("KEK", 10)


if __name__ == '__main__':
    main()