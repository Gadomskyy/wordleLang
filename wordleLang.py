import datetime
import requests

class WordleLangInterpreter:
    def __init__(self, valid_words_file="valid-wordle-words.txt"):
        with open(valid_words_file, "r") as f:
            self.valid_words = set(word.strip().upper() for word in f)
        self.reserved_keywords = {
            "PRINT", "ADDED", "MINUS", "TIMES", "SPLIT",
            "MATCH", "ABOVE", "BELOW", "MAYBE", "OTHER", "ENDED"
        }
        self.vars = {}
        self.lines = []
        self.pc = 0
        self.stack = []

    def get_today_wordle_answer(self):
        date = datetime.date.today()
        url = f"https://www.nytimes.com/svc/wordle/v2/{date:%Y-%m-%d}.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data['solution'].upper()
        except requests.RequestException as e:
            raise RuntimeError("Failed to fetch today's Wordle answer.") from e

    def ensure_wordle_answer_used(self, answer, program_lines):
        joined_code = " ".join(program_lines).upper()
        if answer.upper() not in joined_code:
            raise ValueError(f"The Wordle answer must appear somewhere in your program. Go solve it!")

    def validate_var_name(self, name):
        upper_name = name.upper()
        if upper_name in self.reserved_keywords:
            raise ValueError(f"Invalid variable name: '{name}' is a reserved keyword.")
        if upper_name not in self.valid_words:
            raise ValueError(f"Invalid variable name: '{name}' is not a valid Wordle word.")

    def get_value(self, token):
        try:
            return int(token)
        except ValueError:
            self.validate_var_name(token)
            return self.vars.get(token.upper(), 0)

    def run(self, code_lines):
        self.lines = code_lines
        self.pc = 0

        today_answer = self.get_today_wordle_answer()
        self.ensure_wordle_answer_used(today_answer, code_lines)

        print("Program:")
        for i, line in enumerate(self.lines):
            print(f"{line.strip()}")
        print("Output:")

        while self.pc < len(self.lines):
            line = self.lines[self.pc].strip()
            if not line or line.startswith("#"):
                self.pc += 1
                continue

            parts = line.split()
            cmd = parts[0].upper()

            if cmd == "PRINT":
                val = self.get_value(parts[1])
                print(val)

            elif cmd == "ADDED":
                self.validate_var_name(parts[1])
                self.vars[parts[1].upper()] = self.get_value(parts[2]) + self.get_value(parts[3])

            elif cmd == "MINUS":
                self.validate_var_name(parts[1])
                self.vars[parts[1].upper()] = self.get_value(parts[2]) - self.get_value(parts[3])

            elif cmd == "TIMES":
                self.validate_var_name(parts[1])
                self.vars[parts[1].upper()] = self.get_value(parts[2]) * self.get_value(parts[3])

            elif cmd == "SPLIT":
                self.validate_var_name(parts[1])
                divisor = self.get_value(parts[3])
                if divisor == 0:
                    raise ZeroDivisionError("Division by zero")
                self.vars[parts[1].upper()] = self.get_value(parts[2]) // divisor

            elif cmd == "MATCH":
                self.validate_var_name(parts[1])
                self.vars[parts[1].upper()] = int(self.get_value(parts[2]) == self.get_value(parts[3]))

            elif cmd == "ABOVE":
                self.validate_var_name(parts[1])
                self.vars[parts[1].upper()] = int(self.get_value(parts[2]) > self.get_value(parts[3]))

            elif cmd == "BELOW":
                self.validate_var_name(parts[1])
                self.vars[parts[1].upper()] = int(self.get_value(parts[2]) < self.get_value(parts[3]))

            elif cmd == "MAYBE":
                condition = self.get_value(parts[1])
                if condition:
                    self.stack.append(('MAYBE', True))
                else:
                    self.stack.append(('MAYBE', False))
                    self.skip_block()

            elif cmd == "OTHER":
                if not self.stack or self.stack[-1][0] != 'MAYBE':
                    raise SyntaxError("Unexpected OTHER")
                if self.stack[-1][1]:
                    self.skip_block()
                else:
                    self.stack[-1] = ('OTHER', True)

            elif cmd == "ENDED":
                if self.stack:
                    self.stack.pop()

            else:
                raise SyntaxError(f"Unknown command: {cmd}")

            self.pc += 1

    def skip_block(self):
        nested = 0
        self.pc += 1
        while self.pc < len(self.lines):
            line = self.lines[self.pc].strip()
            if not line:
                self.pc += 1
                continue
            cmd = line.split()[0].upper()
            if cmd in ("MAYBE", "OTHER"):
                nested += 1
            elif cmd == "ENDED":
                if nested == 0:
                    break
                nested -= 1
            self.pc += 1