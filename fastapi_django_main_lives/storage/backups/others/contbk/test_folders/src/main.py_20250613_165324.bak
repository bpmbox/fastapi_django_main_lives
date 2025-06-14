import os

class FileReader:
    def __init__(self, file_path):
        """
        Initialize the FileReader with the file path.
        """
        self.file_path = file_path

    def read_file(self):
        """
        Read the file and return the content.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                content = file.read()
            return content
        else:
            return "File not found"

def main():
    file_reader = FileReader('/home/user/app/gpt-engineer/hist.txt')
    content = file_reader.read_file()
    print(content)

if __name__ == "__main__":
    main()