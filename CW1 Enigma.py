# Creating class rotor to store the 5 rotors and their settings like turnover and notch

class Rotor:
    
    def __init__(self, settings, turnover = False):
    

        #all rotors settings where u can add or remove rotors

        #Rotor : [Wiring, turn over position, Notch]
        self.settings_rotors = {
                "I":    ["PEZUOHXSCVFMTBGLRINQJWAYDK", ["R"], ["Q"]],
                "II":   ["ZOUESYDKFWPCIQXHMVBLGNJRAT", ["F"], ["E"]],
                "III":  ["EHRVXGAOBQUSIMZFLYNWKTPDJC", ["W"], ["V"]],
                "IV":   ["IMETCGFRAYSQBZXWLHKDVUPOJN", ["K"], ["J"]],
                 "V":    ["QWERTZUIOASDFGHJKPYXCVBNML", ["A"], ["Z"]],
                }
        self.setting = settings[0]
        self.ringoffset = settings[1]
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.turnovers = self.settings_rotors[self.setting][1]
        self.notch = self.settings_rotors[self.setting][2]
        self.sequence = None
        self.turnover = turnover
        self.reset_alphabet_settings()
    # Function for rotating the rotor after
    def rotate_alphabet_settings(self):
        self.alphabet = self.alphabet[1:] + self.alphabet[:1]
        self.sequence = self.sequence[1:] + self.sequence[:1]
        if(self.alphabet[0] in self.turnovers):
            self.turnover = True
    # Function for resettting the alphabet after the rotation
    def reset_alphabet_settings(self):

        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.sequence = self.settings_rotors[self.setting][0]
        for _ in range(self.ringoffset):
            self.rotate_alphabet_settings()

    def get_index(self, index):
        """get index of sequence from alphabet

        Args:
            index (integer): index of sequence

        Returns:
            integer: index of sequence from alphabet
        """
        return self.alphabet.index(self.sequence[index])

    
    def get_alphabet_index(self, index):
        return self.sequence.index(self.alphabet[index])


class Reflector:
    def __init__(self, setting):
        self.setting = setting
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        #alphabet settings where all the settings are  stored to choose from. you can add setting.
        self.settings = {"A":   "EJMZALYXVBWFCRQUONTSPIKHGD",
                         "B":    "YRUHQSLDPXNGOKMIEBFZCWVJAT", 
                         "C":    "FVPJIAOYEDRZXWGCTKUQSBNMHL"}
        self.sequence = self.settings[self.setting]

    def get_index(self, index):
        return self.sequence.index(self.alphabet[index])


class Board:
    """alphabet board class
    """
    def __init__(self, map):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.map = {}

        for m in self.alphabet:
            self.map[m] = m
        for m in map:
            self.map[m[0]] = m[1]
            self.map[m[1]] = m[0]

    def get_index(self, c):
        """get index of character from the alphabet

        Args:
            c (string): the char we want to get the index of

        Returns:
            integer: the index
        """
        return self.alphabet.index(self.map[c])

    def get_alphabet_index(self, index):
        return self.map[self.alphabet[index]]


class Enigma:
    """the Enigma machine class that manages all the classes
    and includes the encoding and decoding methods
    """
    def __init__(self, rotorsettings, reflectorsetting):
        self.rotors = []
        #self.rotorsettings = [("II", 0), ("I", 0)]
        self.rotorsettings = rotorsettings
        self.reflectorsetting = reflectorsetting
        self.plugboardsetting = []
        self.plugboard = Board(self.plugboardsetting)
        
        for i in range(len(self.rotorsettings)):
            self.rotors.append(Rotor(settings = self.rotorsettings[i], turnover = False))

        self.reflector = Reflector(self.reflectorsetting)

    def reset_all_alphabet_settings(self):
        """reset the alphabet setting using the reset_alphabet_settings in the rotor class
        must be used after using the encoding and decoding to reset the machine for any further encryptions or decryptions.
        """
        for r in self.rotors:
            r.reset_alphabet_settings()

    def encode(self, c):
        """encode character using the engima machine

        Args:
            c (string): character to be encoded

        Returns:
            string: encoded character
        """
        lower = False
        if c.islower():
            lower = True
        c = c.upper()

        #check if the character is alpha or not
        if (not c.isalpha()):
            return c
        #rotate the map of the alphabet settings map
        self.rotors[0].rotate_alphabet_settings()
        if self.rotors[1].alphabet[0] in self.rotors[1].notch:
            self.rotors[1].rotate_alphabet_settings()

        for i in range(len(self.rotors) - 1):
            if(self.rotors[i].turnover):
                self.rotors[i].turnover = False
                self.rotors[i + 1].rotate_alphabet_settings()

        index = self.plugboard.get_index(c)
        for r in self.rotors:
            index = r.get_index(index)

        index = self.reflector.get_index(index)
        for r in reversed(self.rotors):
            index = r.get_alphabet_index(index)

        c = self.plugboard.get_alphabet_index(index)
        if lower == True:
            return c.lower()
        else:
            return c

    def decode(self,c):
        """decode character

        Args:
            c (string): character to be decoded

        Returns:
            string: decoded character
        """
        return self.encode(c)
    
    #functinon to encode full text
    def encode_text(self, text):
        out = ""
        for char in text:
            out += machine.encode(char)
        return out
    
    #functinon to decode full text
    def decode_text(self, text):
        out = ""
        for char in text:
            out += machine.decode(char)
        return out

#Rotor input settings
position = ["First", "Second", "Third"]
rotorinputs = ["I", "II", "III", "IV", "V"]
correct = 0
incorrect = 0


#Starting of inputs the user will add to run the machine
rotor_input = 0
for i in range(3):
    while True:
        try:
            rotor_input = (input(("Please select your {} Rotor: From I to V: ".format(position[i]))))
            if rotor_input in rotorinputs:
                break;
            else:
                print("Invalid input")
        except:
                continue 

reflector_setting = input("I", "II", "III", "IV", "V")
rotor_movement = [0, 5, 7]
reflector_settings = ["A", "B", "C"]

while True:
    try: 
        reflectorsetting = input("Please enter a letter from the given [A,B,C]: ")
        if reflectorsetting in reflector_settings:
            break;
        else:
            print("Invalid Input")
    except:
            continue
              


machine = Enigma(rotor_input,rotor_movement, reflector_settings)
encrypted_text = machine.enconding(input("Please enter your text: "))
print("Encrypted text: ", encrypted_text)
machine.reset_all_alphabet_settings()
print("Decrypted text: ",machine.encoding(encrypted_text))                    







#Tests on the machine to explore possibilities and finding error


#test 2 
#enigma = Enigma(rotorsettings = [("III", 0), ("II", 0), ("I", 0)], reflectorsetting = "B")
#encoded_text = enigma.encode_text("Enigma")
#print("encoded text : ",  encoded_text)
#enigma.reset_all_alphabet_settings()
#print("decoded text : ", enigma.decode_text(encoded_text) )


#test 3 
#enigma = Enigma(rotorsettings = [("III", 0), ("II", 0), ("I", 0)], reflectorsetting = "C")
#encoded_text = enigma.encode_text("Enigma")
#print("encoded text : ",  encoded_text)
#enigma.reset_all_alphabet_settings()
#print("decoded text : ", enigma.decode_text(encoded_text) )


#test 4 
#enigma = Enigma(rotorsettings = [("V", 0),("IV", 0),("III", 0), ("II", 0), ("I", 0)], reflectorsetting = "A")
#encoded_text = enigma.encode_text("What is your name?")
#print("encoded text : ",  encoded_text)
#enigma.reset_all_alphabet_settings()
#print("decoded text : ", enigma.decode_text(encoded_text) )


#test 5 
#enigma = Enigma(rotorsettings = [("V", 0),("IV", 0),("III", 0), ("II", 0), ("I", 0)], reflectorsetting = "B")
#encoded_text = enigma.encode_text("What is your name?")
#print("encoded text : ",  encoded_text)
#enigma.reset_all_alphabet_settings()
#print("decoded text : ", enigma.decode_text(encoded_text) )
