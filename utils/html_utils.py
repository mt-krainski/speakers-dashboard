from django.utils.html import format_html


def render_link(url, text=None):
    if text is None:
        text = url
    return format_html("<a href='{url}'>{text}</a>", url=url, text=text)


def render_button(url, text, *, disabled=False):
    _class = "class='button'"
    disabled_param = ""
    if disabled:
        disabled_param = f"disabled"
    additional_params = f"{_class} {disabled_param}"
    return format_html(
        "<a href='{url}' %s >{text}</a>" % additional_params,
        url=url if not disabled else "",
        text=text,
    )
