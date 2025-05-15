from wordleLang import WordleLangInterpreter

program = [
    "ADDED BALMY 2 3",
    "MATCH CRISP BALMY 5",
    "MAYBE CRISP",
    "  PRINT BALMY",
    "  PRINT 1",
    "OTHER",
    "  PRINT 0",
    "ENDED"
]

interpreter = WordleLangInterpreter()
interpreter.run(program)
