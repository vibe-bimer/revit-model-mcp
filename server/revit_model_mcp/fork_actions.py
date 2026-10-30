"""The fork's own action tools.

Fork actions register here instead of inside ``actions.py``, so upstream changes cannot
collide with them. The empty registry adds no tools and changes no surface; see
``adr/0005`` for the seam and ``adr/0001`` for the base.
"""


def register_fork_actions(mcp, send) -> None:
    """Registers the fork's extra action tools onto the shared MCP server.

    ``send`` is the same coroutine ``actions.py`` uses after its policy gate. Fork tools
    must go through it rather than around it. With an empty registry this registers nothing.
    """
