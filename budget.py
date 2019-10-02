# The budget calculation program for the hardware team
# Fuhu Xiao <fuhu@umich.edu>

import json

def show_components():
    for i in MENU:
        if type(MENU[i]) is int or type(MENU[i]) is float:
            print(f"{i} = {MENU[i]}")
        else:
            print(f"{i} = High Quality: {MENU[i]['H']}, Low Quality: {MENU[i]['L']}")

class Budget():
    def __init__(self):
        self.total = 0
        self.details = [[],[]]
        self.add_Parts()
    def add_Parts(self):
        self.add_Part("rc_car")
        self.add_Part("accessories") # screws and wires
        self.add_Part("battery")
        self.add_Part("pi")
        self.add_Part("sd_card")
        self.add_Part("camera")
        self.add_Part("servo_driver")
        self.add_Part("frame")
    def add_Part(self, part_name):
        response = input(f"Can we get the {part_name} without purchasing? Y/N  ")
        if response in ["Y","y","Yes","yes","YES","Yeah","Yea","Yup","Yep"]:
            print("OK.")
            return
        if part_name in ["rc_car", "accessories", "pi", "servo_driver", "frame"]:
            self.total += MENU[f"{part_name}"]
            return
        if part_name in ["battery", "sd_card", "camera"]:
            resp = input(f"Choose the class of our {part_name}. H for high, L for low  ")
            if resp in ["H","h","High","high","HIGH"]:
                self.total += MENU[f"{part_name}"]["H"]
                self.details[0].append(part_name)
            else:
                self.total += MENU[f"{part_name}"]["L"]
                self.details[1].append(part_name)
    def get_total(self):
        return self.total
    def get_details(self):
        return self.details

def show_total(budget):
    print("\n\n")
    print("======================================================")
    print(f">> Total: {budget.get_total()} plus tax and delivery <<")
    print(f"High Quality Parts: {budget.get_details()[0]}")
    print(f"Low Quality Parts:  {budget.get_details()[1]}")
    print("Others are in standard quality")
    print("======================================================")
    print("\n\n")

MENU = {
    "rc_car": 110,
    "accessories": 19,
    "battery": {"L": 8, "H": 17,},
    "pi": 38,
    "sd_card": {"L": 8, "H": 19,},
    "camera": {"L": 10, "H": 25,},
    "servo_driver": 10,
    "frame": 50, 
}

if __name__ == "__main__":
    show_components()
    budget = Budget()
    show_total(budget)