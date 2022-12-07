import re
from dataclasses import dataclass


@dataclass
class File:
    size: int


class Directory:
    def __init__(self, parent=None):
        self.parent = parent
        self.children = {}

    @property
    def size(self):
        return sum(child.size for child in self.children.values())

    # recursively find directory with property
    def find(self, property, result):
        if property(self):
            result.append(self)
        for child in self.children.values():
            if isinstance(child, Directory):
                child.find(property, result)
        return result


class FileSystem:
    def __init__(self, terminal_text):
        self.root = Directory()
        self.cwd = self.root
        self.available_space = 70000000

        for command_string in self.get_commands_list(terminal_text):
            self.parse_command_and_result(command_string)

    @staticmethod
    def get_commands_list(text):
        # Regex to find a command and its results: a $ followed by any number of
        # characters other than $
        pattern = re.compile(r'\$ ([^$]+)')
        return pattern.findall(text)

    @property
    def free_space(self):
        return self.available_space - self.root.size

    def find(self, property):
        return self.root.find(property, [])

    def execute_cd(self, str):
        if str == "/":
            self.cwd = self.root
        elif str == "..":
            self.cwd = self.cwd.parent
        else:
            self.cwd = self.cwd.children[str]

    def process_ls_result(self, result):
        # Regex to match "dir <dirname>"
        dir_pattern = re.compile(r'dir ([^\n]+)')
        # Regex to match "<size> <filename>"
        file_pattern = re.compile(r'(\d+) ([^\n]+)')

        for line in result.splitlines():
            if match := dir_pattern.match(line):
                dirname = match.group(1)
                self.cwd.children[dirname] = Directory(self.cwd)
            elif match := file_pattern.match(line):
                size, filename = match.groups()
                self.cwd.children[filename] = File(int(size))

    def parse_command_and_result(self, command_string):
        # Regex to match command of form "cd x"
        cd_pattern = re.compile(r'cd ([^\n]+)')
        # Regex to match command of form "ls, followed by result"
        ls_pattern = re.compile(r'ls\n([^$]+)')

        if match := cd_pattern.match(command_string):
            self.execute_cd(match.group(1))
        elif match := ls_pattern.match(command_string):
            self.process_ls_result(match.group(1))
        else:
            raise ValueError(f"Invalid command: {command_string}")