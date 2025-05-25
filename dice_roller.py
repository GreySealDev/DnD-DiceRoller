import random, sys, re

# The main class of the program, the dice rolling logic is found here
class DiceRoller:
    # When an object is initiated, a history of the rolls is created; up to 10 rolls can be saved for memory reasons
    def __init__(self):
        self.__rolls_history = []

    # Once the command is parsed, this function rolls the selected dice, applying any existing modifier and
    # returning the sum of the dice rolls and a list that includes the result of each roll and the modifier. Finally,
    # appends the roll to the rolls history
    def roll_dice(self, roll_type: str, amount: int, die: int, modifier: int=0):
        rolls = []
        for i in range(amount):
            result = random.randint(1, die)
            rolls.append(result)
        total = sum(rolls) + modifier
        if modifier > 0:
            rolls.append(f"{modifier:+}")
        elif modifier < 0:
            rolls.append(f"{modifier:-}")
        self.__rolls_history.append((total, rolls, roll_type))
        self.__check_history_limit()
        return total, rolls
    
    # Prints the rolls showing the total, each roll, and the modifier (if present), in this order
    def print_roll(self, total: int, rolls: list):
        rolls_strings = []
        for roll in rolls:
            rolls_strings.append(str(roll))
        print(f"{total} ({", ".join(rolls_strings)})")
    
    # Prints each roll present in history using the print_roll method, starting with the most recent
    def print_history(self):
        if len(self.__rolls_history) == 0:
            print("No rolls in history!")
            return
        i = 1
        for entry in self.__rolls_history[::-1]:
            print(str(i) + ". " + entry[2] + ":", end=" ")
            self.print_roll(entry[0], entry[1])
            i += 1

    # Uses regex to make sure that inputs are valid and follow the [number of dice]d[value of dice] structure,
    # positive or negative modifier included: returns True if the input is valid, False otherwise
    def verify_command(self, command: str):
        if re.fullmatch(r"^[0-9]+[d][0-9]+((\+*|-*)[0-9]+){0,1}$", command):
            return True
        else:
            return False
    
    # Parses the command: tests if there's modifiers and splits the command string in three integers, the amount of dice,
    # the type of die, the modifier, returning the three elements
    def parse_command(self, command: str):
        if command.find("+") != -1:
            mod_index = command.find("+")
            modifier = int(command[mod_index:])
        elif command.find("-") != -1:
            mod_index = command.find("-")
            modifier = int(command[mod_index:])
        else:
            mod_index = len(command) + 1
            modifier = 0
        roll = command[:mod_index].split("d")
        amount = int(roll[0])
        die = int(roll[1])
        return amount, die, modifier
    
    # Private method called at every dice roll to clear the oldest roll from history if len exceeds 10
    def __check_history_limit(self):
        if len(self.__rolls_history) > 10:
            self.__rolls_history.pop(0)


# This class contains the user interface: its functions refer to the DiceRoller class
class App:
    # Creates an instance of the roller
    def __init__(self):
        self.roller = DiceRoller()

    # Series of helper methods for execution
    def get_input(self):
        command = input("> ")
        return command
    
    def quit(self):
        sys.exit()

    def wrong_input(self):
        print("That's not a valid input!")

    def invalid_roll(self):
        print("Invalid roll!")

    # Series of methods to interface the app with the DiceRoller
    def verify_command(self, command: str):
        return self.roller.verify_command(command)
    
    def parse_command(self, command: str):
        return self.roller.parse_command(command)
    
    def roll_dice(self, roll_type: str, amount: int, die: int, modifier: int):
        return self.roller.roll_dice(roll_type, amount, die, modifier)
    
    def print_roll(self, total: int, rolls: list):
        self.roller.print_roll(total, rolls)

    def history(self):
        self.roller.print_history()

    # The main program loop is found here
    def execute(self):
        print("""Welcome to the Dice Roller!
        
Type in the dice you want to roll (ex.: 3d6) and, optionally,
a modifier (ex.: +1). Type 'history' to check the most recent
10 rolls starting with the most recent; type 'quit' to exit
the program.
        
Examples of valid rolls:
3d6
5d8+4
2d20-2"""
        )
        while True:
            command = self.get_input()
            if command.lower() == "quit":
                self.quit()
            elif command.lower() == "history":
                self.history()
                continue
            else:
                input_correct = self.verify_command(command)

            if input_correct == True:
                amount, die, modifier = self.parse_command(command)
            else:
                self.wrong_input()
                continue

            if amount == 0 or die == 0:
                self.invalid_roll()
                continue

            total, rolls = self.roll_dice(command, amount, die, modifier)
            self.print_roll(total, rolls)



if __name__ == "__main__":
    app = App()
    app.execute()
