import click


@click.command()
@click.option(
    "--mcp-selected",
    type=click.Choice(["file-handler"], case_sensitive=False),
    help="Select the MCP implementation to run.",
)
def main(mcp_selected: str):
    if mcp_selected == "file-handler":
        from .file_handler import mcp

        mcp.run()


if __name__ == "__main__":
    main()
