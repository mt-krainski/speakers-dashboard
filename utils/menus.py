from django.urls import reverse
from menu import Menu, MenuItem

Menu.add_item(
    "main",
    MenuItem(
        "Login",
        reverse("login"),
        weight=1000,
        check=lambda request: not request.user.is_authenticated,
    ),
)

Menu.add_item(
    "main",
    MenuItem(
        "Logout",
        reverse("logout"),
        weight=1000,
        check=lambda request: request.user.is_authenticated,
    ),
)
