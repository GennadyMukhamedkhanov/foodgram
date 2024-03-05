from api.views.users.views import UserListCreateView


def test_user_list_create():
    assert UserListCreateView.x == 1

