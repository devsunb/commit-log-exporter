import logging
import re
import subprocess

logger = logging.getLogger('LOGIT')


class Logit:
    @staticmethod
    def parse(commit_lines):
        commits = []
        commit = {}
        for line in commit_lines:
            if line == '' or line == '\n' or re.match('merge:', line, re.IGNORECASE):
                continue
            elif re.match('commit', line, re.IGNORECASE):
                if len(commit) != 0:
                    commits.append(commit)
                commit = {'hash': re.match('commit (.*)', line, re.IGNORECASE).group(1)}
            elif re.match('Author:', line, re.IGNORECASE):
                m = re.compile('Author: (.*) <(.*)>').match(line)
                commit['author'] = m.group(1)
                commit['email'] = m.group(2)
            elif re.match('Date:', line, re.IGNORECASE):
                m = re.compile('Date:   (.*)').match(line)
                commit['date'] = m.group(1)
            elif re.match('    ', line, re.IGNORECASE):
                if 'message' not in commit:
                    commit['message'] = line.strip()
                else:
                    commit['message'] += '\n' + line.strip()
            else:
                logger.error('Unexpected Line: ' + line)
        if len(commit) != 0:
            commits.append(commit)
        return commits

    def log(self, cwd, path):
        output = ''
        with subprocess.Popen(['git', 'log', '--', path], cwd=cwd, stdout=subprocess.PIPE, bufsize=1,
                              universal_newlines=True) as p:
            for line in p.stdout:
                output += line
        return self.parse(output.split('\n'))
