import Image, ImageDraw, math, random

class Alphabet:
    def __init__(self, run):
        self.symbols = {}
        self.symbols['F']  = run.forward
        self.symbols['+']  = run.rotate_left
        self.symbols['-']  = run.rotate_right
        self.symbols['[']  = run.push
        self.symbols[']']  = run.pop

class Axiom:    
    def __init__(self):
        self.axiom = 'F'

class Rules:
    def __init__(self):
        self.rules = {}
        self.rules['F'] = 'F[+F]F[-F]F'
        self.rules['+'] = '+'
        self.rules['-'] = '-'
        self.rules['['] = '['
        self.rules[']'] = ']'

class Run:
    #Put in changing width and color as well
    #Random numbers plants, random distances apart, random drawing
    ANGLE_STEP = 30
    PUSH_STEP = 10
    STEP = -3
    IM_SIZE = 500

    def __init__(self, recursions, number_plants):
        self.alphabet = Alphabet(self)
        a = Axiom()
        self.number_plants = number_plants
        self.string = a.axiom
        self.rules = Rules()
        self.stack = []
        self.recursions = recursions
        self.create_string()
        self.im = Image.new("RGBA", (self.IM_SIZE, self.IM_SIZE), (0,0,0,0))
        self.im_draw = ImageDraw.Draw(self.im)
        for i in range(1, number_plants+1):
            self.draw(i)
        self.im.save('l-system.png')

    def create_string(self):
        for times in range(self.recursions):
            new_string = ''
            for i in self.string:
                new_string += self.rules.rules[i]
            self.string = new_string
        print new_string

    def draw(self, number):
        self.angle = 0
        self.pos = (number*(float(self.IM_SIZE)/(1+self.number_plants)),self.IM_SIZE)
        for i in self.string:
            self.alphabet.symbols[i]()

    def forward(self):
        new_pos = (self.STEP*math.sin(math.radians(self.angle))+self.pos[0], self.STEP*math.cos(math.radians(self.angle))+self.pos[1])
        print new_pos
        self.im_draw.line([self.pos, new_pos], fill='green')
        self.pos = new_pos

    def rotate_right(self):
        self.angle += self.ANGLE_STEP*random.random()

    def rotate_left(self):
        self.angle -= self.ANGLE_STEP*random.random()

    def pop(self):
        new_state = self.stack.pop()
        self.pos = (new_state[0], new_state[1])
        self.angle = new_state[2]

    def push(self):
        self.stack.append((self.pos[0], self.pos[1], self.angle+self.PUSH_STEP*random.random()))

if __name__ == '__main__':
    RUN = Run(2, 125)
