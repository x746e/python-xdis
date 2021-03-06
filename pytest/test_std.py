# std
import sys
from contextlib import closing
# compat
import six
# 3rd party
import pytest
# local
import xdis.std as dis
from xdis import PYTHON3, IS_PYPY


# just a simple bit of code that should be the same across python versions,
# we are testing the api here really, leave it to the other tests to perform
# more complicated implementation verification.


TEST_SOURCE_CODE = 'a = 10'
TEST_CODE = compile(TEST_SOURCE_CODE, '<disassembly>', 'single')


TEST_BRANCH_SOURCE_CODE = 'a = 0 if 1 else 2'
TEST_BRANCH_CODE = compile(TEST_BRANCH_SOURCE_CODE, '<disassembly>', 'single')


EXPECTED_CODE_INFO = ("""\
# Method Name:       <module>
# Filename:          <disassembly>
# Argument count:    0
"""
+ ("# Kw-only arguments: 0" if PYTHON3 else "") +
"""# Number of locals:  0
# Stack size:        1
# Flags:             {flags}
# Constants:
#    0: 10
#    1: None
# Names:
#    0: a""").format(flags='0x00000000 (0x0)' if IS_PYPY else '0x00000040 (NOFREE)')


EXPECTED_DIS = """\
  1           0 LOAD_CONST               0 (10)
              3 STORE_NAME               0 (a)
              6 LOAD_CONST               1 (None)
              9 RETURN_VALUE
"""


@pytest.fixture
def bytecode_fixture():
    return dis.Bytecode(TEST_SOURCE_CODE)


@pytest.fixture
def traceback_fixture():
    try:
        raise Exception
    except:
        _, _, tb = sys.exc_info()
        return tb


@pytest.yield_fixture
def stream_fixture():
    with closing(six.StringIO()) as s:
        yield s


def test_bytecode_from_traceback(traceback_fixture):
    assert len(list(dis.Bytecode.from_traceback(traceback_fixture))) > 0


def test_bytecode_codeobj(bytecode_fixture):
    assert bytecode_fixture.codeobj is not None


def test_bytecode_first_line(bytecode_fixture):
    assert bytecode_fixture.first_line is not None


def test_bytecode_dis(bytecode_fixture):
    assert bytecode_fixture.dis() == EXPECTED_DIS


def test_bytecode_info(bytecode_fixture):
    assert bytecode_fixture.info() == EXPECTED_CODE_INFO


def test_bytecode__iter__(bytecode_fixture):
    assert len(list(bytecode_fixture)) > 0


def test_code_info():
    assert dis.code_info(TEST_SOURCE_CODE) == EXPECTED_CODE_INFO


def test_show_code(stream_fixture):
    dis.show_code(TEST_SOURCE_CODE, file=stream_fixture)
    actual = stream_fixture.getvalue()
    assert actual == EXPECTED_CODE_INFO + '\n'


def test_pretty_flags():
    assert dis.pretty_flags(1) == '0x00000001 (OPTIMIZED)'


def test_dis(stream_fixture):
    dis.dis(TEST_SOURCE_CODE, file=stream_fixture)
    actual = stream_fixture.getvalue()
    assert actual == EXPECTED_DIS + '\n'


def test_distb(traceback_fixture, stream_fixture):
    dis.distb(traceback_fixture, file=stream_fixture)
    actual = stream_fixture.getvalue()
    actual_len = len(actual)
    assert actual_len > 0


def test_disassemble(stream_fixture):
    dis.disassemble(TEST_CODE, file=stream_fixture)
    actual = stream_fixture.getvalue()
    expected = EXPECTED_CODE_INFO + '\n' + EXPECTED_DIS + '\n'
    assert actual == expected


def test_get_instructions():
    actual = list(dis.get_instructions(TEST_SOURCE_CODE))
    actual_len = len(actual)
    assert actual_len > 0


def test_findlinestarts():
    actual = list(dis.findlinestarts(TEST_CODE))
    actual_len = len(actual)
    assert actual_len > 0


def test_findlabels():
    actual = list(dis.findlabels(TEST_BRANCH_CODE))
    actual_len = len(actual)
    assert actual_len > 0

