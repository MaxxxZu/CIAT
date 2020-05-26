import csv


class Output:
    def __init__(self, values):
        self.values = values

    def to_csv(self):
        with open('ciat_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.values)
