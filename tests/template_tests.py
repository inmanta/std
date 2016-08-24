"""
    Copyright 2016 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
from inmanta import test
from nose.tools import assert_equal, assert_in


class testTemplates(test.ModuleTestCase):

    def testIsDefined(self):
        self.add_mock_file("templates", "testtemplate.tmpl",
                           """{% if other is defined %} {{name}} : {{ other.name }} "
                           "{% if other.other is defined %} sub: {{ other.other.name }} {% endif %} "
                           "{% else %} {{name}} is not defined {% endif %}""")

        self.compile("""
import std
import unittest

entity Test1:
    string name
end

Test1 prev [0:1] -- [0:1] Test1 other

implementation tt for Test1:
    content=std::template("unittest/testtemplate.tmpl")
    std::print(content)
end

implement Test1 using tt when not(self.prev is defined)
implement Test1 using std::none when self.prev is defined

Test1(name="t1",other=Test1(name="t11"))
Test1(name="t2")
Test1(name="t3",other=Test1(name="t31",other=Test1(name="t32")))
        """)

        assert_in("t3 : t31  sub: t32", self.get_stdout())
        assert_in("t1 : t11", self.get_stdout())
        assert_in("t2 is not defined", self.get_stdout())

    def testTemplate(self):
        """
            Test the evaluation of a template
        """
        self.add_mock_file("templates", "test.tmpl", "{{ value }}")
        self.compile("""import unittest
value = "1234"
std::print(std::template("unittest/test.tmpl"))
        """)

        assert_equal("1234\n", self.get_stdout())

