#!/usr/bin/env python

# -*- coding: utf-8 -*-

import os
import aiml

os.chdir('./src/alice')
alice = aiml.Kernel()
alice.learn("startup.xml")
print alice.respond('LOAD ALICE')
print alice.respond('hello')
while True:
    print alice.respond(raw_input("Enter your message >> "))
