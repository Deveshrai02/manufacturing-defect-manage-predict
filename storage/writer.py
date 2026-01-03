import json
from pathlib import Path


class JSONWriter:
    def __init__(self, filepath=None):
        """JSON writer.

        Args:
            filepath: optional default path. write() may override by passing a filepath.
        """
        self.filepath = filepath

    def write(self, data, filepath=None):
        """Write `data` as pretty JSON to `filepath` or the instance default.

        Ensures parent directories exist.
        """
        target = filepath or self.filepath
        if target is None:
            raise ValueError("No filepath provided to JSONWriter.write() and no default set")

        Path(target).parent.mkdir(parents=True, exist_ok=True)
        with open(target, 'w') as file:
            json.dump(data, file, indent=4)