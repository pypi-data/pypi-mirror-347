import csv
import time


class CSVFileReader:
    """Reads csv file and processes the content further"""

    def __init__(self, header: bool, delimeter=",", batch_size=100) -> None:
        self.header = header
        self.header_data = None
        self.delimeter = delimeter
        self.batch_size = batch_size

    def read(self, file_path: str):
        with open(file_path, "r", newline="") as file:
            reader = csv.reader(file, delimiter=self.delimeter)

            if self.header:
                if not self.header_data:
                    # Store header
                    self.header_data = next(reader)
                    yield self.header_data
                else:
                    # Skip header
                    next(reader)

            # Process rows with batch
            batch = []
            sleep_interval = 0.001
            for row in reader:
                batch.append(row)
                if len(batch) >= self.batch_size:
                    yield batch
                    batch = []
                    # CPU relax
                    time.sleep(sleep_interval)

            if batch:
                yield batch
