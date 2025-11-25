from data.classes import User


def test_surname_change() -> None:
    user = User(1, "user", "user", "user@user.user.user", 73495021832)
    old_surname = user.last_name
    new_surname = user.surname_change("test")
    assert old_surname != new_surname
