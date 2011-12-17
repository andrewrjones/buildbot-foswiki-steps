import re
from twisted.python import log

from buildbot.status.results import SUCCESS, FAILURE, WARNINGS, SKIPPED
from buildbot.steps.shell import Test

class FoswikiSuite(Test):
    command="cd core/test/unit ; perl ../bin/TestRunner.pl FoswikiSuite.pm"

    def evaluateCommand(self, cmd):
        # Get stdio, stripping pesky newlines etc.
        lines = map(
            lambda line : line.replace('\r\n','').replace('\r','').replace('\n',''),
            self.getLog('stdio').readlines()
            )

        total = 0
        passed = 0
        failed = 0
        rc = SUCCESS
        if cmd.rc > 0:
            rc = FAILURE

        re_test_pass = re.compile("^All tests passed \((\d+)\)")

        mos = map(lambda line: re_test_pass.search(line), lines)
        test_pass_lines = [mo.groups() for mo in mos if mo]

        if test_pass_lines:
            test_pass_line = test_pass_lines[0]
            
            total = int(test_pass_line[0])
            passed = total
                
        else:
            rc = FAILURE
            
            re_test_failures = re.compile("^(\d+) failures")
            mos = map(lambda line: re_test_failures.search(line), lines)
            test_failure_lines = [mo.groups() for mo in mos if mo]
            test_failure_line = test_failure_lines[0]
            
            failed = int(test_failure_line[0])
            
            re_test_passed = re.compile("(\d+) of (\d+) test cases passed")
            mos = map(lambda line: re_test_passed.search(line), lines)
            test_passed_lines = [mo.groups() for mo in mos if mo]
            test_passed_line = test_passed_lines[0]
            
            passed = int(test_passed_line[0])
            total = int(test_passed_line[1])

        warnings = 0
        if self.warningPattern:
            wre = self.warningPattern
            if isinstance(wre, str):
                wre = re.compile(wre)

            warnings = len([l for l in lines if wre.search(l)])

            if rc == SUCCESS and warnings:
                rc = WARNINGS

        self.setTestResults(total=total, failed=failed, passed=passed,
                            warnings=warnings)

        return rc
