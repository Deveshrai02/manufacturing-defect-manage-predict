class MappingError(Exception):
    def __init__(self , row , message):
        self.row = row
        self.message = message
        super().__init__(f"MappingError in row {row}: {message}")

        