import re

class Grep():
    """
    Nearly equivalent to Linux grep
    """
    def __init__(self):
        self.pattern = ""
        self.options = {}
        self.subject = ""

    def search(self):
        matches = []
        lines = self.subject.split("\n")

        before = self.options.get('-B', 0)
        after = self.options.get('-A', 0) + 1
        if "-C" in self.options.keys():
            before = after = self.options['-C']
            after += 1

        for e, l in enumerate(lines):
            if self.pattern in l:
                if e >= before and (len(lines)-e) >= after:
                    matches.extend(lines[e-before:e+after])
                else:
                    if e >= before:
                        matches.extend(lines[e-before:])
                    else:
                        matches.extend(lines[:e+after])
        
        return matches
    
    def searchRE(self):
        pass

    def spliceOptions(self, command):
        components = command.split(" ")
        for e, comp in enumerate(components):
            if '-A' in comp:
                try:
                    self.options['-A'] = int(components[e+1])
                except ValueError:
                    print(f"grep command not formatted correctly. '-A' option expects an int following it.\n\tGot '{components[e+1]}'")
                except IndexError:
                    print(f"Incomplete grep command")
            elif '-B' in comp:
                try:
                    self.options['-B'] = int(components[e+1])
                except ValueError:
                    print(f"grep command not formatted correctly. '-B' option expects an int following it.\n\tGot '{components[e+1]}'")
                except IndexError:
                    print(f"Incomplete grep command")
            elif '-C' in comp:
                try:
                    self.options['-C'] = int(components[e+1])
                except ValueError:
                    print(f"grep command not formatted correctly. '-C' option expects an int following it.\n\tGot '{components[e+1]}'")
                except IndexError:
                    print(f"Incomplete grep command")
            elif '-e' in comp:
                self.options[comp] = True
        
        
        return components[-1]

    def run(self, command: str, subject: str):

        p = self.spliceOptions(command)
        self.subject = subject
        out = []

        if '-e' in self.options:
            self.pattern = re.compile(p)
            out = self.searchRE()
        else:
            self.pattern = p
            out = self.search()
        
        return out

if __name__ == "__main__":

    lines = "config system interface\nedit mgmt\nset type static\nset ip 10.0.0.1/24\nex1\nex2\nex3\nconfig secondaryip\nedit 1\nset ip 10.1.0.1/24\nnext\nend\nnext\nend"
    
    gr = Grep()

    command = "show system interface | grep -C 2 secondaryip"

    grep_comm = command.split("|")[1].strip()

    print(gr.run(grep_comm, lines))