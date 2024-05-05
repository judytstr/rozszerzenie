import csv
import json
import pickle
import sys

class FileProcessor:
    def __init__(self, input_file_path):
        self._input_file_path = input_file_path
        self.data = self.read_file()

    def read_file(self):
        try:
            with open(self._input_file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print("File not found:", self._input_file_path)
            sys.exit(1)
        except Exception as e:
            print("Error reading file:", e)
            sys.exit(1)

    def apply_changes(self, changes):
        raise NotImplementedError("Subclasses must implement apply_changes method")

    def display_data(self):
        print(self.data)

    def save_to_file(self, output_file_path):
        try:
            with open(output_file_path, 'w') as file:
                file.write(self.data)
            print("Data saved to", output_file_path)
        except Exception as e:
            print("Error saving to file:", e)

class CSVFileProcessor(FileProcessor):
    def read_file(self):
        try:
            with open(self._input_file_path, 'r', newline='') as file:
                return list(csv.reader(file))
        except FileNotFoundError:
            print("File not found:", self._input_file_path)
            sys.exit(1)
        except Exception as e:
            print("Error reading file:", e)
            sys.exit(1)

    def apply_changes(self, changes):
        for change in changes:
            try:
                x, y, value = map(str.strip, change.split(','))
                x, y = int(x), int(y)
                data_lines = self.data.split('\n')
                if y < len(data_lines):
                    row = list(csv.reader([data_lines[y]]))[0]
                    if x < len(row):
                        row[x] = value
                        data_lines[y] = ",".join(row)
                        self.data = '\n'.join(data_lines)
                    else:
                        print("Index out of range for change:", change)
                        sys.exit(1)
                else:
                    print("Index out of range for change:", change)
                    sys.exit(1)
            except ValueError:
                print("Invalid change format:", change)
                sys.exit(1)

class JSONFileProcessor(FileProcessor):
    def read_file(self):
        try:
            with open(self._input_file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print("File not found:", self._input_file_path)
            sys.exit(1)
        except Exception as e:
            print("Error reading file:", e)
            sys.exit(1)

    def apply_changes(self, changes):
        for change in changes:
            try:
                x, y, value = map(str.strip, change.split(','))
                x, y = int(x), int(y)
                if y < len(self.data):
                    row = list(self.data[y])
                    if x < len(row):
                        self.data = self.data[:y] + value + self.data[y + 1:]
                    else:
                        print("Index out of range for change:", change)
                        sys.exit(1)
                else:
                    print("Index out of range for change:", change)
                    sys.exit(1)
            except ValueError:
                print("Invalid change format:", change)
                sys.exit(1)

    def save_to_file(self, output_file_path):
        try:
            with open(output_file_path, 'w') as file:
                json.dump(self.data, file)
            print("Data saved to", output_file_path)
        except Exception as e:
            print("Error saving to file:", e)

class TextFileProcessor(FileProcessor):
    def apply_changes(self, changes):
        lines = self.data.split('\n')
        for change in changes:
            try:
                x, y, value = map(str.strip, change.split(','))
                x, y = int(x), int(y)
                if y < len(lines):
                    line = lines[y]
                    if x < len(line):
                        self.data = self.data[:y * (len(line) + 1) + x] + value + self.data[y * (len(line) + 1) + x + 1:]
                    else:
                        print("Index out of range for change:", change)
                        sys.exit(1)
                else:
                    print("Index out of range for change:", change)
                    sys.exit(1)
            except ValueError:
                print("Invalid change format:", change)
                sys.exit(1)

class PickleFileProcessor(FileProcessor):
    def read_file(self):
        try:
            with open(self._input_file_path, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            print("File not found:", self._input_file_path)
            sys.exit(1)
        except Exception as e:
            print("Error reading file:", e)
            sys.exit(1)

    def apply_changes(self, changes):
        for change in changes:
            try:
                x, y, value = map(str.strip, change.split(','))
                x, y = int(x), int(y)
                if y < len(self.data):
                    row = list(self.data[y])
                    if x < len(row):
                        self.data = self.data[:y * (len(row) + 1) + x] + value + self.data[y * (len(row) + 1) + x + 1:]
                    else:
                        print("Index out of range for change:", change)
                        sys.exit(1)
                else:
                    print("Index out of range for change:", change)
                    sys.exit(1)
            except ValueError:
                print("Invalid change format:", change)
                sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python reader.py <input_file> <output_file> <change1> <change2> ... <changeN>")
        sys.exit(1)

    _input_file_path = sys.argv[1]
    _output_file_path = sys.argv[2]
    _changes = sys.argv[3:]

    processors = {
        '.csv': CSVFileProcessor,
        '.json': JSONFileProcessor,
        '.txt': TextFileProcessor,
        '.pickle': PickleFileProcessor
    }

    _input_file_extension = _input_file_path.split('.')[-1]
    if _input_file_extension not in processors:
        print("Unsupported file format")
        sys.exit(1)

    file_processor = processors[_input_file_extension](_input_file_path)
    file_processor.apply_changes(_changes)
    print("Modified data:")
    file_processor.display_data()
    file_processor.save_to_file(_output_file_path)
