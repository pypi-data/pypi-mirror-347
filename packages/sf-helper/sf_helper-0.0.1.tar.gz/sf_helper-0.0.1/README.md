A small repo dedicated to desigining a CLI tool with Python via Click and built by the Poetry.
For details, see:

- [Click](https://click.palletsprojects.com/en/stable/)
- [Poetry](https://python-poetry.org/docs/)

### Instructions

1. `pip install poetry` | `pip install click` - install poetry module
2. `poetry install` - install project dependencies
3. `poetry run sf-helper "hello world"` - test the cli
4. `poetry build` - build the /dist folder
5. `pip install dist/sf_helper-0.0.1.tar.gz` - install the cli locally
6. Open a new terminal window and try the cli: `sf-helper --help`
7. Open a new terminal window.
   Run the following command(s):

    | Command                               | Description                             |
    |---------------------------------------|-----------------------------------------|
    | `sf-helper return_pokemon --pokemon charizard` | Returns data or details about the Pokémon named "charizard". |
    | `sf-helper greet --name ian`              | Prints a greeting message for the name "ian". |

### Testing

To run the test files in `/tests`, from the root directory execute the following command:
```bash
poetry run pytest
```
- Todo: possible to use runner.py to test cli commands more effectively? 

### Tagging 

To add a tag to a branch, use `git tag v0.0.1`.

To trigger a test build, add a tag matching the `v0.0.0` naming convention:

```
git checkout main
git tag v0.0.1
git push origin refs/tags/v0.0.1
```

Optionally:

```
git tag -f v0.0.1 HEAD
```
