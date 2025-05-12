uv build --no-sources --package OfficeMCP
uv publish --token pypi-AgEIcHlwaS5vcmcCJDAwOWNmZDZiLTYxZTYtNDE4ZS04ZjI4LTI4ZmNhZjFmNGUxNwACKlszLCIzMTY3ZDdhYS0xOWQ1LTRlM2UtYTRiZC02OTE0NTMzN2VmYjUiXQAABiAreu3da9VkpCS4o8ALPH1eDJaqo3TcUe-EZ3E-ROpQfA
uv run --with OfficeMCP --no-project --refresh-package OfficeMCP -- python -c "import excelmcp"
uvx OfficeMCP