LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'



class Substitution(object):
    " Classic enigma machine reflector. "
    __slots__ = ('wiring','pos')
    def __init__(self, filename=None, wiring=None):
        " Takes as input reflector style input file. "
        self.pos = 0
        try:
            if wiring is not None:
                cont = [LETTERS.index(c) if c in LETTERS else c \
                                for c in wiring]
                self.wiring = cont[:26]
            elif filename is not None:
                with open(filename, 'r') as f:
                    cont = [LETTERS.index(c) if c in LETTERS else c \
                                for c in f.read()]
                    self.wiring = cont[:26]
            else:
                raise IOError('No wiring system provided. Please provide\
either a filename or a wiring specifications')
        except:
            raise IOError('Unable to read input')
    def translate(self, key):
        " Translates the input signal according to settings"
        i = LETTERS.index(key)
        j = (i + self.pos) % len(LETTERS)
        k = self.wiring[j]
        j = (k - self.pos) % len(LETTERS)
        i = LETTERS[j]
        return i
    def converse_translate(self, key):
        " Translates the input signal backwards according to settings"
        i = LETTERS.index(key)
        j = (i + self.pos) % len(LETTERS)
        k = self.wiring.index(j)
        j = (k - self.pos) % len(LETTERS)
        i = LETTERS[j]
        return i

class Rotor(Substitution):
    " Classic enigma machine rotor. "
    __slots__ = ('pos', 'wiring', 'notch', 'rachet_engaged')
    def __init__(self, filename=None, wiring=None):
        " Takes as input rotor style input file. "
        self.pos = 0
        self.rachet_engaged = False
        try:
            if wiring is not None:
                cont = [LETTERS.index(c) if c in LETTERS else c \
                                for c in wiring]
                self.wiring = cont[:26]
                self.notch = cont[27:29]
            elif filename is not None:
                with open(filename, 'r') as f:
                    cont = [LETTERS.index(c) if c in LETTERS else c \
                                for c in f.read()]
                    self.wiring = cont[:26]
                    self.notch = cont[27:29]
            else:
                raise IOError('No wiring system provided. Please provide\
either a filename or a wiring specifications')
        except:
            raise IOError('Unable to read input')
    def step(self, prevRotor):
        " Steps this rotor. "
        if prevRotor is None: # fast rotor always steps
            self.rachet_engaged = True
        if self.rachet_engaged:
            self.rachet_engaged = False
            self.pos += 1; self.pos %= len(LETTERS) # move
            if prevRotor is not None:
                prevRotor.rachet_engaged = True # double step
        if prevRotor is not None and \
           prevRotor.pos == prevRotor.notch[0]: # previous rotor in rachet pos
            self.rachet_engaged = True

class Reflector(Substitution):
    pass

class Plugboard(Substitution):
    pass
        
        
def test(plugboard, rotors, settings, reflector):
    " Runs a classic enigma simulation with specified rotors, reflectors, \
and settings (rotor positions).\n Rotors in order of fastest to slowest. "
    # set rotors according to settings
    for i in range(len(rotors)):
        rotors[i].pos = settings[i]
    # get letter to translate
    m = input('  > ').upper()
    while not m.upper().startswith('Q'):
        c = LETTERS
        print(' '.join(c), 'Input')
        print('-'*len(LETTERS)*2)
        # plugboard
        c = [plugboard.translate(l) for l in c]
        print(' '.join(c), 'Plugboard')
        print('-'*len(LETTERS)*2)
        # step
        rotors[-1].step(None)
        for i in range(len(rotors)-1, 0, -1):
            rotors[i-1].step(rotors[i])
        # translate up to reflector
        for r in rotors[::-1]: # slowest/leftmost is last
            c = [r.translate(l) for l in c]
            print(' '.join(c), 'Rotors')
        print('-'*len(LETTERS)*2)
        c = [reflector.translate(l) for l in c]
        print(' '.join(c), 'Reflector')
        print('-'*len(LETTERS)*2)
        # translate down from reflector
        for r in rotors: # fastest/rightmost is last
            c = [r.converse_translate(l) for l in c]
            print(' '.join(c), 'Rotors')
        # plugboard
        c = [plugboard.converse_translate(l) for l in c]
        print('-'*len(LETTERS)*2)
        print(' '.join(c), 'Plugboard')
        # display and wait for next letter
        print('-'*len(LETTERS)*2)
        print(' '.join(c), 'Output')
        print(
              'slow', rotors[0].pos,
              'middle', rotors[1].pos,
              'fast', rotors[2].pos)
        m = input('  > ').upper()

def enigma_convert_message(plugboard, rotors, settings, reflector, intext):
    for i in range(len(rotors)):
        rotors[i].pos = settings[i]
    outtext = ''
    for m in intext.upper():
        if m not in LETTERS:
            continue
        # plugboard
        m = plugboard.translate(m)
        # step
        rotors[-1].step(None)
        for i in range(len(rotors)-1, 0, -1):
            rotors[i-1].step(rotors[i])
        # translate up to reflector
        for r in rotors[::-1]:
            m = r.translate(m)
        # reflect
        m = reflector.translate(m)
        # translate down from reflector
        for r in rotors:
            m = r.converse_translate(m)
        # plugboard
        m = plugboard.converse_translate(m)
        outtext += m
    return outtext

def enigma_convert_message_no_reflector(plugboard,
                                        rotors, settings, intext):
    for i in range(len(rotors)):
        rotors[i].pos = settings[i]
    outtext = ''
    for m in intext.upper():
        if m not in LETTERS:
            continue
        # plugboard
        m = plugboard.translate(m)
        # step
        rotors[-1].step(None)
        for i in range(len(rotors)-1, 0, -1):
            rotors[i-1].step(rotors[i])
        # translate up to reflector
        for r in rotors[::-1]:
            m = r.translate(m)
        outtext += m
    return outtext


        

if __name__ == '__main__':
    plugboard = Plugboard(wiring='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    rotors = (Rotor('Rotors\RotorI.txt'),
              Rotor('Rotors\RotorII.txt'),
              Rotor('Rotors\RotorIII.txt'))
    settings = (0,0,0)
    reflector = Reflector('Rotors\Reflector.txt')
    test(plugboard,rotors,settings,reflector)
