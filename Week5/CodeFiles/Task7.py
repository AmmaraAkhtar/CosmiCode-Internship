class FileHandler:
    def __init__(self,fileName):
        self.fileName=fileName

    def write_file(self,content):
        with open(self.fileName, "w") as f:
            f.write(content)
        print("File Written Successfully..")


    def append_file(self,content):
        with open(self.fileName,"a") as f:
            f.write(content)
        print("File written Successfully.")

    def read_file(self):
        try:
            with open(self.fileName, 'r') as f:
                data=f.read()
                print("File Content")
                print(data)
        except FileNotFoundError:
            print("File Not Found...")



f=FileHandler("example.txt")
f.write_file("Hlo I am Ammara\n")
f.append_file("My age is 19.")
f.read_file()