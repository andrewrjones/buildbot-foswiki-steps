buildbot-foswiki-steps
======================

Buildbot build steps optimised for building the Fosiwiki project.

Usage
-----

Firstly, download or clone the code and put it somewhere near your buildmaster.

Then add the following (or similar):

    from foswiki import FoswikiSuite

### FoswikiSuite()

You can use this as follows:

    factory.addStep(FoswikiSuite())

It will run `cd core/test/unit ; perl ../bin/TestRunner.pl -clean FoswikiSuite.pm` in the build directory. The output is then parsed to get the test results, which are then displayed in your waterfall.

It is a subclass of `Test`, and takes the same arguments.
