import foswiki

from twisted.trial import unittest
from buildbot.status.results import SKIPPED, SUCCESS, WARNINGS, FAILURE
from buildbot.test.util import steps, compat

class FakeLogFile:
    def __init__(self, text):
        self.text = text

    def getText(self):
        return self.text

class FakeCmd:
    def __init__(self, stdout, stderr, rc=0):
        self.logs = {'stdout': FakeLogFile(stdout),
                     'stderr': FakeLogFile(stderr)}
        self.rc = rc

class FoswikiSuite(steps.BuildStepMixin, unittest.TestCase):

    def setUp(self):
        return self.setUpBuildStep()

    def tearDown(self):
        return self.tearDownBuildStep()
        
    def test_foswikiPass(self):
        step = self.setupStep(foswiki.FoswikiSuite())
        
        log = """Options: 
exporting FOSWIKI_ASSERTS=1 for extra checking; disable by exporting FOSWIKI_ASSERTS=0
Assert checking on 1
Starting CWD is /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit 
Looking for InterwikiPlugin...
	Found InterwikiPlugin/InterwikiPluginSuite.pm
	Found InterwikiPlugin/InterwikiPluginTests.pm
Found 2 tests, favoring InterwikiPlugin/InterwikiPluginSuite.pm
Running InterwikiPluginSuite
Running InterwikiPluginTests
	InterwikiPluginTests::test_link_from_local_rules_topic
	InterwikiPluginTests::test_link_with_parentheses
	InterwikiPluginTests::test_link_with_topic_name
	InterwikiPluginTests::test_bold_link
	InterwikiPluginTests::test_italic_link
	InterwikiPluginTests::test_link_from_default_rules_topic
	InterwikiPluginTests::test_link_format
	InterwikiPluginTests::test_strong_code_link
	InterwikiPluginTests::test_link_from_inherted_rules_topic
	InterwikiPluginTests::test_link_with_quoted_string
	InterwikiPluginTests::test_link_in_parentheses
	InterwikiPluginTests::test_link_with_url
	InterwikiPluginTests::test_code_link
	InterwikiPluginTests::test_cant_view_rules_topic
	InterwikiPluginTests::test_link_with_complex_url

Unit test run Summary:
All tests passed (15)
1..195
"""
        step.addCompleteLog('stdio', log)

        rc = step.evaluateCommand(FakeCmd("", ""))
        
        self.assertEqual(rc, SUCCESS)
        self.assertEqual(self.step_statistics, {
            'tests-total' : 15,
            'tests-failed' : 0,
            'tests-passed' : 15,
            'tests-warnings' : 0,
        })
        
    def test_foswikiFailure(self):
        step = self.setupStep(foswiki.FoswikiSuite())
        
        log = """Unit test run Summary:
5 expected failures:
PasswordTests::test_ApacheHtpasswdUser_md5
ERROR:  Missing CPAN Module Apache::Htpasswd - Can't locate Apache/Htpasswd.pm in @INC  - Consider using Foswiki::Users::HtpasswdUser for password manager at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Foswiki/Users/ApacheHtpasswdUser.pm line 39.

PasswordTests::test_ApacheHtpasswdUser_crypt
ERROR:  Missing CPAN Module Apache::Htpasswd - Can't locate Apache/Htpasswd.pm in @INC  - Consider using Foswiki::Users::HtpasswdUser for password manager at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Foswiki/Users/ApacheHtpasswdUser.pm line 39.

PasswordTests::test_htpasswd_auto
AUTO TESTS WILL FAIL: missing Crypt::PasswdMD5
Failure for bat at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/PasswordTests.pm line 208
	PasswordTests::test_htpasswd_auto('PasswordTests=HASH(0x7fdcf01e2118)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 395
	Unit::TestRunner::__ANON__() called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 379
	eval {...} called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 371
	Error::subs::try('CODE(0x7fdcf0138b48)', 'HASH(0x7fdcf0262658)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 414
	Unit::TestRunner::runOne('PasswordTests=HASH(0x7fdcf01e2118)', 'PasswordTests', undef) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 147
	Unit::TestRunner::start('Unit::TestRunner=HASH(0x7fdcda209ed8)', 'FoswikiSuite.pm') called

PasswordTests::test_htpasswd_apache_md5
Can't locate Crypt/PasswdMD5.pm in @INC (@INC contains: /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib /Users/buildbot/oss-slave/foswiki-psgi/build/core/bin /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit /Users/buildbot/perl5/perlbrew/perls/perl-5.10.1/lib/5.10.1/darwin-2level /Users/buildbot/perl5/perlbrew/perls/perl-5.10.1/lib/5.10.1 /Users/buildbot/perl5/perlbrew/perls/perl-5.10.1/lib/site_perl/5.10.1/darwin-2level /Users/buildbot/perl5/perlbrew/perls/perl-5.10.1/lib/site_perl/5.10.1 . /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/arch /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/5.10.1/darwin-2level /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/5.10.1 /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/CommentPlugin /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/EditTablePlugin /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/EmptyPlugin /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/HistoryPlugin /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/InterwikiPlugin /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/MailerContrib /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/TablePlugin /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/TwistyPlugin /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/PreferencesPlugin /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/SpreadSheetPlugin /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/WysiwygPlugin /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/TopicUserMappingContrib /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/TWikiCompatibilityPlugin /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/UnitTestContrib) at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Foswiki/Users/HtPasswdUser.pm line 73.

QueryTests::verify_versions_on_other_topic_fail_BruteForceQuery

Expected ARRAY ARRAY(0x7fdcf101c710), got [[99,String,n
n t	t s\s q'q o#o h#h X~X \b \a \e \f \r \cX,1,%RED%,Some text (really) we have text,Diesel],[99,String,n
n t	t s\s q'q o#o h#h X~X \b \a \e \f \r \cX,1,%RED%,Some text (really) we have text,Petroleum],[99,String,n
n t	t s\s q'q o#o h#h X~X \b \a \e \f \r \cX,1,%RED%,Some text (really) we have text,Petrol]] for 'AnotherTopic'/versions.META:FIELD[name='SillyFuel'].value in QueryTests /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/QueryTests.pm 784 at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestCase.pm line 225
	Unit::TestCase::assert_equals('QueryTests=HASH(0x7fdcf064e8f8)', 'Diesel', 'ARRAY(0x7fdcdf402fc0)', 'Expected ARRAY ARRAY(0x7fdcf101c710), got [[99,String,n{a}n t{9}t...') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestCase.pm line 442
	Unit::TestCase::assert_deep_equals('QueryTests=HASH(0x7fdcf064e8f8)', 'Diesel', 'ARRAY(0x7fdcdf402fc0)', 'Expected ARRAY ARRAY(0x7fdcf101c710), got [[99,String,n{a}n t{9}t...', 'HASH(0x7fdcf10b8ec0)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestCase.pm line 419
	Unit::TestCase::assert_deep_equals('QueryTests=HASH(0x7fdcf064e8f8)', 'ARRAY(0x7fdcf101c710)', 'ARRAY(0x7fdcf07d2840)', 'Expected ARRAY ARRAY(0x7fdcf101c710), got [[99,String,n{a}n t{9}t...') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/QueryTests.pm line 235
	QueryTests::check('QueryTests=HASH(0x7fdcf064e8f8)', '\'AnotherTopic\'/versions.META:FIELD[name=\'SillyFuel\'].value', 'eval', 'ARRAY(0x7fdcf101c710)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/QueryTests.pm line 784
	QueryTests::verify_versions_on_other_topic_fail('QueryTests=HASH(0x7fdcf064e8f8)') called at (eval 943498) line 4
	Unit::TestCase::__ANON__('QueryTests=HASH(0x7fdcf064e8f8)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 395
	Unit::TestRunner::__ANON__() called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 379
	eval {...} called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 371
	Error::subs::try('CODE(0x7fdcf1024f20)', 'HASH(0x7fdcf0748310)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 414
	Unit::TestRunner::runOne('QueryTests=HASH(0x7fdcf064e8f8)', 'QueryTests', undef) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 147
	Unit::TestRunner::start('Unit::TestRunner=HASH(0x7fdcda209ed8)', 'FoswikiSuite.pm') called

12 failures:
ConfigureTests::test_Package_loadInstaller

Unexpected number of files in EmptyPlugin manifest at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestCase.pm line 311
	Unit::TestCase::assert_num_equals('ConfigureTests=HASH(0x7fdcda2595d0)', 3, 4, 'Unexpected number of files in EmptyPlugin manifest') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/ConfigureTests.pm line 1779
	ConfigureTests::test_Package_loadInstaller('ConfigureTests=HASH(0x7fdcda2595d0)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 395
	Unit::TestRunner::__ANON__() called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 379
	eval {...} called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 371
	Error::subs::try('CODE(0x7fdcdd337100)', 'HASH(0x7fdcdd3be2d8)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 414
	Unit::TestRunner::runOne('ConfigureTests=HASH(0x7fdcda2595d0)', 'ConfigureTests', undef) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 147
	Unit::TestRunner::start('Unit::TestRunner=HASH(0x7fdcda209ed8)', 'FoswikiSuite.pm') called at ../bin/TestRunner.pl line 126
 at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/FoswikiTestCase.pm line 40
	FoswikiTestCase::__ANON__('{a}Unexpected number of files in EmptyPlugin manifest at /Users...') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestCase.pm line 212
	Unit::TestCase::assert('ConfigureTests=HASH(0x7fdcda2595d0)', '', 'Unexpected number of files in EmptyPlugin manifest') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestCase.pm line 311
	Unit::TestCase::assert_num_equals('ConfigureTests=HASH(0x7fdcda2595d0)', 3, 4, 'Unexpected number of files in EmptyPlugin manifest') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/ConfigureTests.pm line 1779
	ConfigureTests::test_Package_loadInstaller('ConfigureTests=HASH(0x7fdcda2595d0)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 395
	Unit::TestRunner::__ANON__() called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 379
	eval {...} called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 371
	Error::subs::try('CODE(0x7fdcdd337100)', 'HASH(0x7fdcdd3be2d8)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 414
	Unit::TestRunner::runOne('ConfigureTests=HASH(0x7fdcda2595d0)', 'ConfigureTests', undef) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 147
	Unit::TestRunner::start('Unit::TestRunner=HASH(0x7fdcda209ed8)', 'FoswikiSuite.pm') called

---------------------------
ConfigureTests::test_Util_createArchive_shellTar

 does not appear to exist - Create tar archive at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/ConfigureTests.pm line 1640
	ConfigureTests::test_Util_createArchive_shellTar('ConfigureTests=HASH(0x7fdcda2595d0)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 395
	Unit::TestRunner::__ANON__() called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 379
	eval {...} called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 371
	Error::subs::try('CODE(0x7fdcdd3494c0)', 'HASH(0x7fdcdd4ace48)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 414
	Unit::TestRunner::runOne('ConfigureTests=HASH(0x7fdcda2595d0)', 'ConfigureTests', undef) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 147
	Unit::TestRunner::start('Unit::TestRunner=HASH(0x7fdcda209ed8)', 'FoswikiSuite.pm') called at ../bin/TestRunner.pl line 126
 at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/FoswikiTestCase.pm line 40
	FoswikiTestCase::__ANON__('{a} does not appear to exist - Create tar archive at /Users/bui...') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestCase.pm line 212
	Unit::TestCase::assert('ConfigureTests=HASH(0x7fdcda2595d0)', undef, ' does not appear to exist - Create tar archive') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/ConfigureTests.pm line 1640
	ConfigureTests::test_Util_createArchive_shellTar('ConfigureTests=HASH(0x7fdcda2595d0)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 395
	Unit::TestRunner::__ANON__() called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 379
	eval {...} called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 371
	Error::subs::try('CODE(0x7fdcdd3494c0)', 'HASH(0x7fdcdd4ace48)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 414
	Unit::TestRunner::runOne('ConfigureTests=HASH(0x7fdcda2595d0)', 'ConfigureTests', undef) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 147
	Unit::TestRunner::start('Unit::TestRunner=HASH(0x7fdcda209ed8)', 'FoswikiSuite.pm') called

---------------------------
PasswordTests::test_htpasswd_crypt_md5

HASH(0x7fdcf020e5c8) at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestCase.pm line 294
	Unit::TestCase::assert_str_not_equals('PasswordTests=HASH(0x7fdcf01e2118)', '$1PjZv7zUdhlw', '$1PjZv7zUdhlw', 'HASH(0x7fdcf020e5c8)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/PasswordTests.pm line 108
	PasswordTests::doTests('PasswordTests=HASH(0x7fdcf01e2118)', 'Foswiki::Users::HtPasswdUser=HASH(0x7fdcf01c9118)', 1) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/PasswordTests.pm line 363
	PasswordTests::test_htpasswd_crypt_md5('PasswordTests=HASH(0x7fdcf01e2118)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 395
	Unit::TestRunner::__ANON__() called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 379
	eval {...} called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 371
	Error::subs::try('CODE(0x7fdcf0217cc8)', 'HASH(0x7fdcf0226f38)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 414
	Unit::TestRunner::runOne('PasswordTests=HASH(0x7fdcf01e2118)', 'PasswordTests', undef) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 147
	Unit::TestRunner::start('Unit::TestRunner=HASH(0x7fdcda209ed8)', 'FoswikiSuite.pm') called

---------------------------
PasswordTests::test_htpasswd_plain

Assertion failed at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/PasswordTests.pm line 69
	PasswordTests::doTests('PasswordTests=HASH(0x7fdcf01e2118)', 'Foswiki::Users::HtPasswdUser=HASH(0x7fdcf019d930)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/PasswordTests.pm line 401
	PasswordTests::test_htpasswd_plain('PasswordTests=HASH(0x7fdcf01e2118)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 395
	Unit::TestRunner::__ANON__() called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 379
	eval {...} called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 371
	Error::subs::try('CODE(0x7fdcf030f4e8)', 'HASH(0x7fdcf01d3ef0)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 414
	Unit::TestRunner::runOne('PasswordTests=HASH(0x7fdcf01e2118)', 'PasswordTests', undef) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 147
	Unit::TestRunner::start('Unit::TestRunner=HASH(0x7fdcda209ed8)', 'FoswikiSuite.pm') called

---------------------------
RenameTests::test_renameWeb_10990
OopsException(attention/rename_web_exists web=>RenamedTemporaryRenameTestsTestWebRenameTests topic=>WebPreferences params=>[RENAMEDTemporaryRenameTestsTestWebRenameTests,WebPreferences])
---------------------------
RenameTests::test_renameTopic_find_referring_topics_when_renamed_topic_is_not_a_WikiWord

expected but missing: TemporaryRenameTestsTestWebRenameTests.Random TemporaryRenameTestsTestWebRenameTests.ranDom at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestCase.pm line 225
	Unit::TestCase::assert_equals('RenameTests=HASH(0x7fdcf1599e08)', 0, 2, 'expected but missing: TemporaryRenameTestsTestWebRenameTests....') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/RenameTests.pm line 377
	RenameTests::checkReferringTopics('RenameTests=HASH(0x7fdcf1599e08)', 'TemporaryRenameTestsTestWebRenameTests', 'random', 0, 'ARRAY(0x7fdcf3138310)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/RenameTests.pm line 692
	RenameTests::test_renameTopic_find_referring_topics_when_renamed_topic_is_not_a_WikiWord('RenameTests=HASH(0x7fdcf1599e08)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 395
	Unit::TestRunner::__ANON__() called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 379
	eval {...} called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 371
	Error::subs::try('CODE(0x7fdcf228a548)', 'HASH(0x7fdcf30b2838)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 414
	Unit::TestRunner::runOne('RenameTests=HASH(0x7fdcf1599e08)', 'RenameTests', undef) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 147
	Unit::TestRunner::start('Unit::TestRunner=HASH(0x7fdcda209ed8)', 'FoswikiSuite.pm') called

---------------------------
RenameTests::test_renameTemplateThisWeb

expected but missing: TemporaryRenameTestsTestWebRenameTests.TmplRefTopic2 TemporaryRenameTestsTestWebRenameTests.TmplRefMeta1 TemporaryRenameTestsTestWebRenameTests.TmplRefMeta2 TemporaryRenameTestsTestWebRenameTests.TmplRefMeta3 TemporaryRenameTestsTestWebRenameTests.TmplRefTopic at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestCase.pm line 225
	Unit::TestCase::assert_equals('RenameTests=HASH(0x7fdcf1599e08)', 0, 5, 'expected but missing: TemporaryRenameTestsTestWebRenameTests....') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/RenameTests.pm line 377
	RenameTests::checkReferringTopics('RenameTests=HASH(0x7fdcf1599e08)', 'TemporaryRenameTestsTestWebRenameTests', 'NewViewTemplate', 0, 'ARRAY(0x7fdcf3107578)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/RenameTests.pm line 454
	RenameTests::test_renameTemplateThisWeb('RenameTests=HASH(0x7fdcf1599e08)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 395
	Unit::TestRunner::__ANON__() called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 379
	eval {...} called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 371
	Error::subs::try('CODE(0x7fdcf3019b38)', 'HASH(0x7fdcf2f6b308)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 414
	Unit::TestRunner::runOne('RenameTests=HASH(0x7fdcf1599e08)', 'RenameTests', undef) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 147
	Unit::TestRunner::start('Unit::TestRunner=HASH(0x7fdcda209ed8)', 'FoswikiSuite.pm') called

---------------------------
RenameTests::test_referringTemplateThisWeb

expected but missing: TemporaryRenameTestsTestWebRenameTests.TmplRefTopic2 TemporaryRenameTestsTestWebRenameTests.TmplRefMeta1 TemporaryRenameTestsTestWebRenameTests.TmplRefMeta2 TemporaryRenameTestsTestWebRenameTests.TmplRefMeta3 TemporaryRenameTestsTestWebRenameTests.TmplRefTopic at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestCase.pm line 225
	Unit::TestCase::assert_equals('RenameTests=HASH(0x7fdcf1599e08)', 0, 5, 'expected but missing: TemporaryRenameTestsTestWebRenameTests....') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/RenameTests.pm line 377
	RenameTests::checkReferringTopics('RenameTests=HASH(0x7fdcf1599e08)', 'TemporaryRenameTestsTestWebRenameTests', 'OldViewTemplate', 0, 'ARRAY(0x7fdcf31d11a8)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/RenameTests.pm line 405
	RenameTests::test_referringTemplateThisWeb('RenameTests=HASH(0x7fdcf1599e08)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 395
	Unit::TestRunner::__ANON__() called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 379
	eval {...} called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 371
	Error::subs::try('CODE(0x7fdcf2f33168)', 'HASH(0x7fdcf31d1148)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 414
	Unit::TestRunner::runOne('RenameTests=HASH(0x7fdcf1599e08)', 'RenameTests', undef) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 147
	Unit::TestRunner::start('Unit::TestRunner=HASH(0x7fdcda209ed8)', 'FoswikiSuite.pm') called

---------------------------
RenameTests::test_renameTopic_with_lowercase_first_letter

Expect 100: [[UpperCase]]
Actual 100: [[lowercase]]
RenameTests,/Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/RenameTests.pm,1281 at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestCase.pm line 277
	Unit::TestCase::assert_str_equals('RenameTests=HASH(0x7fdcf1599e08)', '100: [[UpperCase]]', '100: [[lowercase]]', 'Expect 100: [[UpperCase]]{a}Actual 100: [[lowercase]]{a}RenameTes...') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/RenameTests.pm line 330
	RenameTests::check('RenameTests=HASH(0x7fdcf1599e08)', 'TemporaryRenameTestsTestWebRenameTests', 'UpperCase', 'Foswiki::Meta=HASH(0x7fdcf31a53d0)', 'One lowercase{a}Twolowercase{a}[[UpperCase]]{a}', 100) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/RenameTests.pm line 1281
	RenameTests::test_renameTopic_with_lowercase_first_letter('RenameTests=HASH(0x7fdcf1599e08)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 395
	Unit::TestRunner::__ANON__() called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 379
	eval {...} called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 371
	Error::subs::try('CODE(0x7fdcf30de6e8)', 'HASH(0x7fdcf3237c90)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 414
	Unit::TestRunner::runOne('RenameTests=HASH(0x7fdcf1599e08)', 'RenameTests', undef) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 147
	Unit::TestRunner::start('Unit::TestRunner=HASH(0x7fdcda209ed8)', 'FoswikiSuite.pm') called

---------------------------
RenameTests::test_referringTopicsThisWeb

expected but missing: TemporaryRenameTestsTestWebRenameTests.Random TemporaryRenameTestsTestWebRenameTests.ranDom at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestCase.pm line 225
	Unit::TestCase::assert_equals('RenameTests=HASH(0x7fdcf1599e08)', 0, 2, 'expected but missing: TemporaryRenameTestsTestWebRenameTests....') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/RenameTests.pm line 377
	RenameTests::checkReferringTopics('RenameTests=HASH(0x7fdcf1599e08)', 'TemporaryRenameTestsTestWebRenameTests', 'OldTopic', 0, 'ARRAY(0x7fdcf3267360)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/RenameTests.pm line 559
	RenameTests::test_referringTopicsThisWeb('RenameTests=HASH(0x7fdcf1599e08)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 395
	Unit::TestRunner::__ANON__() called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 379
	eval {...} called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 371
	Error::subs::try('CODE(0x7fdcf30328d8)', 'HASH(0x7fdcf328b670)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 414
	Unit::TestRunner::runOne('RenameTests=HASH(0x7fdcf1599e08)', 'RenameTests', undef) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 147
	Unit::TestRunner::start('Unit::TestRunner=HASH(0x7fdcda209ed8)', 'FoswikiSuite.pm') called

---------------------------
VCStoreTests::verify_NoHistory_implicitSave_VCStoreTests_RcsWrap

Expected:'1324143034'
 But got:'1324143035'
 at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestCase.pm line 311
	Unit::TestCase::assert_num_equals('VCStoreTests=HASH(0x7fdcf5536820)', 1324143034, 1324143035) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/test/unit/VCStoreTests.pm line 264
	VCStoreTests::verify_NoHistory_implicitSave('VCStoreTests=HASH(0x7fdcf5536820)') called at (eval 1196918) line 4
	Unit::TestCase::__ANON__('VCStoreTests=HASH(0x7fdcf5536820)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 395
	Unit::TestRunner::__ANON__() called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 379
	eval {...} called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/CPAN/lib/Error.pm line 371
	Error::subs::try('CODE(0x7fdcf5cb8ea8)', 'HASH(0x7fdcf5e38870)') called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 414
	Unit::TestRunner::runOne('VCStoreTests=HASH(0x7fdcf5536820)', 'VCStoreTests', undef) called at /Users/buildbot/oss-slave/foswiki-psgi/build/core/lib/Unit/TestRunner.pm line 147
	Unit::TestRunner::start('Unit::TestRunner=HASH(0x7fdcda209ed8)', 'FoswikiSuite.pm') called

3537 of 3554 test cases passed
1..72469
"""
        step.addCompleteLog('stdio', log)
        
        rc = step.evaluateCommand(FakeCmd("", ""))
        
        self.assertEqual(rc, FAILURE)
        self.assertEqual(self.step_statistics, {
            'tests-total' : 3554,
            'tests-failed' : 12,
            'tests-passed' : 3537,
            'tests-warnings' : 0,
        })
