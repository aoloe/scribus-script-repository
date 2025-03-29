# Scribus Scripts Repository

If you want to extend the scripts in the repository you're welcome to clone it, fork it, send patches or make pull requests.

## Downlad of Scripts

- _Open_ the script in Github
- Click on the _Download raw file_ icon in the small toolbar at the top right of the script.

## Script basic skeleton

```py
"""Description of the script

© mit, ale rimoldi, 2023
"""

try:
    import scribus # pylint: disable=import-error
except ImportError:
    pass

def main():
    try:
        scribus
    except NameError:
        print('This script must be run from inside Scribus.')
        return

    if not scribus.haveDoc():
        scribus.messageBox('Export Error', 'You need an open document.', icon=scribus.ICON_CRITICAL)
        return

if __name__ == '__main__':
    main()
```
