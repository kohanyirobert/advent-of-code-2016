import re
from sys import stdin

VAL_RXP = re.compile(r'''(?x)
    ^
    value\s
    (?P<chip>\d+)
    \sgoes\sto\sbot\s
    (?P<serial>\d+)
    $
''')

BOT_RXP = re.compile(r'''(?x)
    ^
    bot\s
    (?P<serial>\d+)
    \sgives\slow\sto\s
    (?P<low_target>\w+)
    \s
    (?P<low_serial>\d+)
    \sand\shigh\sto\s
    (?P<high_target>\w+)
    \s
    (?P<high_serial>\d+)
    $
''')


class Instruction:

    def __init__(self, string):
        self.string = string

    def __str__(self):
        return self.string

    def __repr__(self):
        return str(self)

    def apply(self, factory):
        pass


class ValInstruction(Instruction):

    @classmethod
    def fromstring(cls, string):
        m = VAL_RXP.match(string)
        return cls(
            string,
            int(m.group('chip')),
            int(m.group('serial'))
        )

    def __init__(self, string, chip, serial):
        super(ValInstruction, self).__init__(string)
        self.chip = chip
        self.serial = serial

    def apply(self, factory):
        bot = factory.get_target('bot', self.serial)
        if len(bot.chips) >= 2:
            return False
        bot.add(self.chip)
        return True


class BotInstruction(Instruction):

    @classmethod
    def fromstring(cls, string):
        m = BOT_RXP.match(string)
        return cls(
            string,
            int(m.group('serial')),
            m.group('low_target'),
            int(m.group('low_serial')),
            m.group('high_target'),
            int(m.group('high_serial')),
        )

    def __init__(self, string, serial, low_target, low_serial, high_target, high_serial):
        super(BotInstruction, self).__init__(string)
        self.serial = serial
        self.low_target = low_target
        self.low_serial = low_serial
        self.high_target = high_target
        self.high_serial = high_serial

    def apply(self, factory):
        bot = factory.get_target('bot', self.serial)
        if len(bot.chips) < 2:
            return False

        high_dst = factory.get_target(self.high_target, self.high_serial)
        high_dst.add(bot.get())

        low_dst = factory.get_target(self.low_target, self.low_serial)
        low_dst.add(bot.get())
        return True


class Instructions:

    @classmethod
    def fromstring(_, string):
        if string.startswith('value'):
            return ValInstruction.fromstring(string)
        return BotInstruction.fromstring(string)

    @classmethod
    def frominput(cls):
        s = stdin.read().strip().split('\n')
        return [cls.fromstring(x) for x in s]


class Target:

    def __init__(self, serial):
        self.serial = serial
        self.chips = []

    def __str__(self):
        return '{}{}{{{}}}'.format(
            type(self).__name__,
            self.serial,
            ','.join([str(x) for x in self.chips]),
        )

    def __repr__(self):
        return str(self)

    def add(self, chip):
        self.chips.append(chip)
        self.chips.sort()

    def get(self):
        return self.chips.pop()


class Bot(Target):

    def is_cmp(self, low, high):
        return low in self.chips and high in self.chips


class Out(Target):
    pass


class Targets:

    @classmethod
    def fromargs(_, target, serial):
        if target == 'bot':
            return Bot(serial)
        return Out(serial)


class Factory:

    def __init__(self, instructions):
        self.instructions = instructions
        self.all_dsts = {
            'bot': {},
            'output': {},
        }

    def __str__(self):
        return 'Bots: {}, Outs: {}'.format(
            ', '.join([str(x) for x in self.all_dsts['bot'].values()]),
            ', '.join([str(x) for x in self.all_dsts['output'].values()]),
        )

    def __repr__(self):
        return str(self)

    def tick(self):
        if len(self.instructions) > 0:
            instruction = self.instructions.pop(0)
            if instruction.apply(self):
                print('ok', instruction.string)
            else:
                print('no', instruction.string)
                self.instructions.append(instruction)
            return True
        return False

    def get_target(self, target, serial):
        target_dsts = self.all_dsts[target]
        if serial not in target_dsts:
            target_dsts[serial] = Targets.fromargs(target, serial)
        return target_dsts[serial]

    def get_cmp_bot(self, low, high):
        bots = self.all_dsts['bot']
        for bot in bots.values():
            if bot.is_cmp(low, high):
                return bot
        return None


def main():
    factory = Factory(Instructions.frominput())
    while factory.tick():
        bot = factory.get_cmp_bot(17, 61)
        if bot:
            print(bot)
            break

main()
