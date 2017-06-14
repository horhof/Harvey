#!/usr/bin/env python3

import habits
import argparse

if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument("habit", help="Which habit to do")
    args = arg.parse_args()
    
    habits = habits.Habits()
    habits.do(args.habit)
