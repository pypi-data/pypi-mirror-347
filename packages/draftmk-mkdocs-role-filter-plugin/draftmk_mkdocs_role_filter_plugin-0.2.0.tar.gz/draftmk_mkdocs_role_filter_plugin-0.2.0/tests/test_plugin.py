import pytest
from role_filter_plugin.plugin import RoleFilterPlugin
from types import SimpleNamespace


@pytest.fixture
def plugin():
    plugin = RoleFilterPlugin()
    plugin.load_config({"allowed_roles": ["public"]})
    return plugin


def test_on_page_markdown_allows_public(plugin):
    page = SimpleNamespace(
        meta={"role": "public"}, file=SimpleNamespace(src_path="public.md")
    )
    result = plugin.on_page_markdown("**Hello**", page, None, None)
    assert result == "**Hello**"
    assert "public.md" in plugin.allowed_paths


def test_on_page_markdown_blocks_internal(plugin):
    page = SimpleNamespace(
        meta={"role": "internal"}, file=SimpleNamespace(src_path="internal.md")
    )
    result = plugin.on_page_markdown("**Secret**", page, None, None)
    assert result == ""
    assert "internal.md" not in plugin.allowed_paths


def test_on_nav_filters_properly(plugin):
    # Manually whitelist public.md
    plugin.allowed_paths.add("public.md")

    public_page = SimpleNamespace(file=SimpleNamespace(src_path="public.md"))
    internal_page = SimpleNamespace(file=SimpleNamespace(src_path="internal.md"))

    nav_item_public = SimpleNamespace(page=public_page)
    nav_item_internal = SimpleNamespace(page=internal_page)
    nav_item_folder = SimpleNamespace(children=[nav_item_public, nav_item_internal])

    nav = SimpleNamespace(items=[nav_item_folder])
    filtered_nav = plugin.on_nav(nav, None, None)

    # Only public.md should be retained
    assert len(filtered_nav.items) == 1
    assert len(filtered_nav.items[0].children) == 1
    assert filtered_nav.items[0].children[0].page.file.src_path == "public.md"
