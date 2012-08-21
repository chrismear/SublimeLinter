# -*- coding: utf-8 -*-
# sass.py - sublimelint package for checking Sass files

import re
# import subprocess

from base_linter import BaseLinter

CONFIG = {
    'language': 'Sass',
    'executable': 'sass',
    'lint_args': '-c'
}


class Linter(BaseLinter):
    SASS_WARNING_START_RE = re.compile(r'^WARNING on line (?P<line>\d+) of.+?')
    SASS_WARNING_NEXT_RE = re.compile(r'^(?P<error>.+?)$')
    SASS_ERROR_START_RE = re.compile(r'^Syntax error: (?P<error>.+?)$')
    SASS_ERROR_NEXT_RE = re.compile(r'^.+?on line (?P<line>\d+) of.+?')

    SCSS_FILE_NAME_RE = re.compile(r'css$')

    def __init__(self, config):
        super(Linter, self).__init__(config)
        self.linter = None

    # def get_executable(self, view):
    #     view_file_name = view.file_name()
    #     if self.SCSS_FILE_NAME_RE.match(view_file_name):
    #         linter = 'scss'
    #     else:
    #         linter = 'sass'
    #     try:
    #         path = self.get_mapped_executable(view, linter)
    #         subprocess.call([path, '-v'], startupinfo=self.get_startupinfo())
    #         return (True, path, 'using {0}'.format(linter))
    #     except OSError:
    #         return (False, '', '{0} is required'.format(linter))

    def parse_errors(self, view, errors, lines, errorUnderlines, violationUnderlines, warningUnderlines, errorMessages, violationMessages, warningMessages):
        current_warning_lineno = 0
        current_error_message = None
        for line in errors.splitlines():
            if current_warning_lineno != 0:
                warning_match = self.SASS_WARNING_NEXT_RE.match(line)
                if warning_match:
                    error = warning_match.group('error')
                    self.add_message(current_warning_lineno, lines, error, errorMessages)
                    current_warning_lineno = 0
                    continue
                else:
                    current_warning_lineno = 0
                    continue
            elif current_error_message is not None:
                error_match = self.SASS_ERROR_NEXT_RE.match(line)
                if error_match:
                    lineno = int(error_match.group('line'))
                    self.add_message(lineno, lines, current_error_message, errorMessages)
                    current_error_message = None
                    continue
                else:
                    current_error_message = None
                    continue
            warning_match = self.SASS_WARNING_START_RE.match(line)
            if warning_match:
                current_warning_lineno = int(warning_match.group('line'))
                continue
            error_match = self.SASS_ERROR_START_RE.match(line)
            if error_match:
                current_error_message = error_match.group('error')
                continue
