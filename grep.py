import re

class Grep():
    """
    Nearly equivalent to Linux grep
    """
    def __init__(self):
        self.pattern = ""
        self.options = []
        self.subject = ""

    def search(self):
        matches = []
        lines = self.subject.split("\n")

        for l in lines:
            if self.pattern in l:
                matches.append(l)
        
        return matches
    
    def searchRE(self):
        pass

    def run(self, options: list, PATTERN: str, subject: str):

        self.options = options
        self.subject = subject

        if '-e' in options:
            self.pattern = re.compile(PATTERN)
            self.searchRE()
        else:
            self.pattern = PATTERN
            self.search()

        