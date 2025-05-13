from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.structure.pages import Page
from mkdocs.structure.nav import Navigation


class RoleFilterPlugin(BasePlugin):
    config_scheme = (("allowed_roles", config_options.Type(list, default=["public"])),)

    def __init__(self):
        self.allowed_paths = set()

    def on_page_markdown(self, markdown, page: Page, config, files, **kwargs):
        role = page.meta.get("role", "public")
        if role in self.config["allowed_roles"]:
            self.allowed_paths.add(page.file.src_path)
            return markdown
        return ""  # Hide content for unauthorized pages

    def on_nav(self, nav: Navigation, config, files, **kwargs):
        def filter_items(items):
            filtered = []
            for item in items:
                if hasattr(item, "children") and item.children:
                    item.children = filter_items(item.children)
                    if item.children:
                        filtered.append(item)
                elif hasattr(item, "page"):
                    if item.page and item.page.file.src_path in self.allowed_paths:
                        filtered.append(item)
                else:
                    filtered.append(item)
            return filtered

        nav.items = filter_items(nav.items)
        return nav
