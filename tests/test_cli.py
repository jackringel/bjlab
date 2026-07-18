import pytest

from bjlab.cli import main


def test_help_exits_zero():
    with pytest.raises(SystemExit) as e:
        main(["--help"])
    assert e.value.code == 0


def test_version_exits_zero():
    with pytest.raises(SystemExit) as e:
        main(["--version"])
    assert e.value.code == 0


def test_no_command_is_an_error():
    with pytest.raises(SystemExit) as e:
        main([])
    assert e.value.code == 2


@pytest.mark.parametrize("command", [["strategy"], ["deviations"], ["sim"], ["session"]])
def test_stub_commands_report_not_implemented(command, capsys):
    assert main(command) == 2
    assert "not implemented" in capsys.readouterr().err


def test_ev_stub(capsys):
    assert main(["ev", "--hand", "A,7", "--upcard", "6"]) == 2
    assert "not implemented" in capsys.readouterr().err
