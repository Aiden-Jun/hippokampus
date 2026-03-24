from notion_client import Client


class NotionClient:
    def __init__(self, token):
        self.notion = Client(auth=token)
        self.cache = {}
        self._counter = 0
        self._id_map = {}

    @staticmethod
    def _blocks_to_markdown(blocks: list) -> str:
        lines = []
        for block in blocks:
            btype = block["type"]
            rich = block.get(btype, {}).get("rich_text", [])
            text = "".join(t["plain_text"] for t in rich)

            if btype == "heading_1":
                lines.append(f"# {text}")
            elif btype == "heading_2":
                lines.append(f"## {text}")
            elif btype == "heading_3":
                lines.append(f"### {text}")
            elif btype == "to_do":
                checked = block["to_do"].get("checked", False)
                lines.append(f"- [{'x' if checked else ' '}] {text}")
            elif btype == "bulleted_list_item":
                lines.append(f"- {text}")
            elif btype == "numbered_list_item":
                lines.append(f"1. {text}")
            elif btype == "quote":
                lines.append(f"> {text}")
            elif btype == "code":
                lang = block["code"].get("language", "")
                lines.append(f"```{lang}\n{text}\n```")
            elif btype == "divider":
                lines.append("---")
            elif btype == "child_page":
                pass
            else:
                lines.append(text)

        return "\n\n".join(lines)

    @staticmethod
    def _get_title(page: dict) -> str:
        props = page.get("properties", {})
        title_prop = props.get("title") or props.get("Name")
        if title_prop:
            rich = title_prop.get("title", [])
            return "".join(t["plain_text"] for t in rich) or "Untitled"
        return "Untitled"

    def _add_to_cache(self, page, parent_int):
        pid = page["id"]
        simple_id = self._counter
        self._counter += 1
        self._id_map[pid] = simple_id

        blocks = self.notion.blocks.children.list(block_id=pid)["results"]
        content = self._blocks_to_markdown(blocks)
        child_blocks = [b for b in blocks if b["type"] == "child_page"]

        self.cache[simple_id] = {
            "id": pid,
            "title": self._get_title(page),
            "content": content,
            "parent": parent_int,
            "children": []
        }

        for child_block in child_blocks:
            child_page = self.notion.pages.retrieve(child_block["id"])
            child_simple_id = self._add_to_cache(child_page, parent_int=simple_id)
            self.cache[simple_id]["children"].append(child_simple_id)

        return simple_id

    def sync(self):
        self.cache = {}
        self._counter = 0
        self._id_map = {}

        resp = self.notion.search(filter={"property": "object", "value": "page"})
        for page in resp["results"]:
            if page["parent"]["type"] == "workspace":
                self._add_to_cache(page, parent_int=None)

    def get_notes(self) -> dict:
        return self.cache
