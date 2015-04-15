from pytest import mark
from proclib.api import spawn


@mark.parametrize('cmd', (
    'echo hello | cat',
    [['echo', 'hello'], 'cat'],
    ['echo hello', 'cat'],
    ['echo hello | cat'],
))
def test_spawn_parses_all_argtypes(cmd):
    assert spawn(cmd).stdout == 'hello\n'