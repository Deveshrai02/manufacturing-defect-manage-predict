class CSVReader:
    def __init__(self , filepath):
        self.filepath = filepath
    def __iter__(self):
        with open(self.filepath, 'r') as file:
            header = next(file)  # Skip header
            for line in file:
                yield line.strip().split(',')