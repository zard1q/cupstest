import os
class Printer:
    def __init__(self, name, ip, protocol):
        self.name = name
        self.ip = ip
        self.protocol = protocol
    def mount(self):
        command = f"lpadmin -p {self.name} -E -v ipp://{self.ip}/ipp/print -m everywhere"
        os.system(command)

    def test_1_side_portrait(self):
        pass

    def test_2_side_portrait(self):
        pass

    def test_1_side_landscape(self):
        pass

    def test_2_side_landscape(self):
        pass

    def test_2_pages_portrait(self):
        pass

    def test_2_pages_landscape(self):
        pass

    def test_color_portrait(self):
        pass

    def test_color_landscape(self):
        pass

    def show(self):
        print(f"{self.ip} | {self.name} | {self.protocol}")
