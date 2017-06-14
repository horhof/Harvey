#!/usr/bin/env python3

import re
import ast
import json
import textwrap

class Habits:
    
    filename = "log"
    sheetname = "sheet.json"
    habits = {}
    
    def __init__(self):
        """
        Assembles habits from log
        """
        with open(self.filename) as f:
            for line in f:
                h = self.parseLine(line)
                name = h.pop("name", None)
                self.habits[name] = h
        with open(self.sheetname) as s:
            self.sheet = json.load(s)
    
    def parseLine(self, line):
        """
        Parses given line into a dictionary
        """
        grammar = "^(.+): (do|repeat) (\d+) per (\d+),? worth (\d+),? did (\d+) over (\d+)$"
        m = re.search(grammar, line)
        repeat = False
        if (m.group(1) == "repeat"):
            repeat = True
        habit = {
            "name": m.group(1),
            "weight": ast.literal_eval(m.group(5)),
            "repeat": repeat,
            "times": ast.literal_eval(m.group(3)),
            "perDay": ast.literal_eval(m.group(4)),
            "done": ast.literal_eval(m.group(6)),
            "span": ast.literal_eval(m.group(7))
        }
        return habit
    
    def save(self):
        """
        Write habits back out to simple text form
        """
        outfile = open(self.filename, "w")
        for name in self.habits:
            h = self.habits[name]
            action = "do"
            if h["repeat"]:
                action = "repeat"
            line = "{}: {} {} per {}, worth {}, did {} over {}".format(name, action, h["times"], h["perDay"], h["weight"], h["done"], h["span"])
            print(line, file=outfile)
    
    def do(self, name):
        """
        Accomplish a habit, adjust log and perform player adjustments
        """
        if name in self.habits:
            self.good(name)
        else:
            print("Couldn't find habit [{}]".format(name))
        self.save()
    
    def good(self, name):
        s = self.sheet
        
        h = self.habits[name]
        h["done"] += 1
        rarity = h["done"] / h["span"]
        goldGain = rarity * h["weight"] / s["experience"]
        xpGain = rarity / s["experience"]
        
        status = """
        | Habit [{:}] has been increased
        | Rarity [{:>5}] Weight [{:>5}] Done [{:>5}]
        |
        | Earned:
        |   Gold [{:>5.2}] Exp.   [{:>5.0}]
        |
        | Health [{:>5}] Gold   [{:>5}] Experience [{:>5}]
        """.format(
                name,
                rarity, h["weight"], h["done"],
                goldGain, xpGain,
                s["health"], s["gold"], s["experience"]
            )
        
        print(textwrap.dedent(status))
