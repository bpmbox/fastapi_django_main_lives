import subprocess

class PlantUML:
    def processes_file(self, filename, code):
        with open(filename, "w") as f:
            f.write("@startuml\n")
            f.write(code)
            f.write("@enduml\n")
        subprocess.run(["plantuml", "-tpng", filename])