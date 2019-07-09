from django.urls import reverse
from menu import Menu, MenuItem

Menu.add_item(
    "main",
    MenuItem(
        "Add presentation",
        reverse("presentation-manager:presentation-add"),
        weight=1000,
        check=lambda request: request.user.is_authenticated
        and request.user.has_perm("presentation_manager.add_presentation"),
    ),
)

Menu.add_item(
    "main",
    MenuItem(
        "List presentations",
        reverse("presentation-manager:presentation-list"),
        weight=1000,
        check=lambda request: request.user.is_authenticated
        and request.user.has_perm("presentation_manager.view_presentation"),
    ),
)

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
