# Static Code Analyzer

import ast
import re
import os
import sys
from _ast import expr


class Issue:
    issues = []
    messages = {
        'S001': 'Too long',
        'S002': 'Indentation not a multiple of four',
        'S003': 'Unnecessary semicolon',
        'S004': 'At least two spaces required before inline comments',
        'S005': 'TODO found',
        'S006': 'More than two black lines used before this line',
        'S007': 'Too many spaces after {}',
        'S008': 'Class name {} should be written in CamelCase',
        'S009': 'Function name {} should be written in snake_case',
        'S010': 'Argument name {} should be written in snake_case',
        'S011': 'Variable {} should be written in snake_case',
        'S012': 'The default argument value is mutable'
    }

    def __init__(self, file, line, code, extra=''):
        self.file = file
        self.line = line
        self.code = code
        self.extra = extra
        Issue.issues.append(self)


def get_files():
    path = sys.argv[1]
    file_list = []
    if os.path.isdir(path):
        file_list = [file for file in os.listdir(path) if file[-3:] == '.py']
    elif os.path.isfile(path) and path[-3:] == '.py':
        file_list.append(path)
    return file_list


def get_file(file_name):
    with open(file_name, 'r') as f:
        program = f.readlines()
    return program


def is_empty_line(line):
    if re.match(r'^\s*$', line):
        return True


def check_line_length(file_name, n, line):
    if len(line) > 79:
        Issue(file_name, n, 'S001')


def check_indentation_four(file_name, n, line):
    if is_empty_line(line):
        return
    template = r'\s*'
    match = re.match(template, line)
    if len(match.group()) % 4:
        Issue(file_name, n, 'S002')


def check_semicolon_after(file_name, n, line: str):
    if is_empty_line(line):
        return
    start_comment = line.find('#')
    if start_comment == 0:
        return
    end_code = start_comment if start_comment > 0 else len(line)
    if line[0:end_code].rstrip()[-1] == ';':
        Issue(file_name, n, 'S003')


def check_two_spaces_inline_comment(file_name, n, line: str):
    if is_empty_line(line):
        return
    if line.lstrip()[0] == '#':
        return
    start_comment = line.find('#')
    if start_comment > 2:
        if line[start_comment - 1] != ' ' or line[start_comment - 2] != ' ':
            Issue(file_name, n, 'S004')


def check_todo(file_name, n, line: str):
    if is_empty_line(line):
        return
    start_comment = line.find('#')
    if start_comment == -1:
        return
    if line.lower().find('todo') > start_comment:
        Issue(file_name, n, 'S005')


def check_spaces_after_construction(file_name, n, line: str):
    if is_empty_line(line):
        return
    if line.lstrip().find('def') == 0:
        if line[line.find('def') + 4] == ' ':
            Issue(file_name, n, 'S007', 'def')
    if line.lstrip().find('class') == 0:
        if line[line.find('class') + 6] == ' ':
            Issue(file_name, n, 'S007', 'class')


def check_class_name(file_name, n, line):
    if is_empty_line(line):
        return
    if line.lstrip().find('class') == 0:
        class_index = line.find('class')
        parenthesis_index = line.find('(')
        class_name = line[class_index + 5:parenthesis_index].lstrip()
        template = r'([A-Z][a-z]*)+'
        if not re.match(template, class_name):
            Issue(file_name, n, 'S008', class_name)


def check_function_name(file_name, n, line):
    if is_empty_line(line):
        return
    if line.lstrip().find('def') == 0:
        func_index = line.find('def')
        parenthesis_index = line.find('(')
        func_name = line[func_index + 3:parenthesis_index].lstrip()
        template = r'(__)?([a-z_]+)+(__)?'
        if not re.match(template, func_name):
            Issue(file_name, n, 'S009', func_name)


class Analyzer(ast.NodeVisitor):

    def __init__(self, file_name):
        self.file_name = file_name
        super().__init__()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        args = [a.arg for a in node.args.args]
        for arg in args:
            template = r'(__)?([a-z_]+)+(__)?'
            if not re.match(template, arg):
                Issue(self.file_name, node.lineno, 'S010', arg)
        defs = [a for a in node.args.defaults]
        for value in defs:
            if isinstance(value, ast.List) or isinstance(value, ast.Set) or isinstance(value, ast.Dict):
                Issue(self.file_name, node.lineno, 'S012')
        for n in ast.walk(node):
            if isinstance(n, ast.Assign):
                self.visit_Assign(n)

    def visit_Assign(self, node: ast.Assign):
        # for alias in node:
        template = r'(__)?([a-z_]+)+(__)?'
        if isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
        else:
            var_name = node.targets[0].value.id
        if not re.match(template, var_name):
            Issue(self.file_name, node.lineno, 'S011', var_name)


def check_lines(file_name, program):
    consecutive_empty_lines = 0
    tree = ast.parse(''.join(program))
    analyzer = Analyzer(file_name)
    analyzer.visit(tree)
    for n, line in enumerate(program, start=1):
        check_line_length(file_name, n, line)
        check_indentation_four(file_name, n, line)
        check_semicolon_after(file_name, n, line)
        check_two_spaces_inline_comment(file_name, n, line)
        check_todo(file_name, n, line)
        if is_empty_line(line):
            consecutive_empty_lines += 1
        else:
            if consecutive_empty_lines > 2:
                Issue(file_name, n, 'S006')
            consecutive_empty_lines = 0
        check_spaces_after_construction(file_name, n, line)
        check_class_name(file_name, n, line)
        check_function_name(file_name, n, line)


def output_issues():
    for issue in Issue.issues:
        print(f'{issue.file}: Line {issue.line}: {issue.code} {Issue.messages[issue.code].format(issue.extra)}')


def main():
    file_list = get_files()
    for file in file_list:
        if sys.argv[1][-3:] != '.py':
            file_name = os.path.join(sys.argv[1], file)
        else:
            file_name = file
        program = get_file(file_name)
        check_lines(file_name, program)
    output_issues()


main()
