from data.classes import User


def test_new_email() -> None:
    user = User(1, "user", "user", "user@user.user.user", 73495021832)
    old_email = user.email_address
    new_email = user.new_email("newuser@user.user.user")
    assert old_email != new_email
