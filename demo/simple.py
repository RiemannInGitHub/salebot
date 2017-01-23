#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import sys
sys.path.insert(0, "../third_party")

import aiml

# The Kernel object is the public interface to
# the AIML interpreter.
k = aiml.Kernel()

# Use the 'learn' method to load the contents
# of an AIML file into the Kernel.
print os.getcwd()

# k.learn("alice/*.aiml")
k.learn("load_aiml.xml")

# Use the 'respond' method to compute the response
# to a user's input string.  respond() returns
# the interpreter's response, which in this case
# we ignore.
k.respond("load aiml cnask")

# Loop forever, reading user input from the command
# line and printing responses.
print("你好，欢迎使用demo")
while True:
    print k.respond(raw_input("> "))
