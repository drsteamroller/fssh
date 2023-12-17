# Author: Andrew McConnell

import argparse
import paramiko
from getpass import getpass
import re

class Grep():

    def __init__(self):
        self.pattern = ""
        self.options = []
        self.subject = ""

    def search(self):
        pass

    def run(self, options: list, PATTERN: str, subject: str):

        self.options = options

        if '-e' in options:
            self.pattern = re.compile(PATTERN)
        else:
            self.pattern = PATTERN
        self.subject = subject


        
