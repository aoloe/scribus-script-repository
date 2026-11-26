# Create a foldable fanzine

Create a foldable fanzine by putting the eight A7 pages from a Scribus document on one side of an A4 sheet.

The A7 pages are imposed in the following way:

```
--- --- --- ---
 7 | 6 | 5 | 4 |
 ↻ | ↻ | ↻ | ↻ |
--- --- --- ---
 8 | 1 | 2 | 3 |
   |   |   |   |
--- --- --- ---
```

The _upper_ pages being rotated by 180°.

If there are more than eight pages, only the first pages are imposed.

## Installing pypdf

The script uses the pypdf library. You need to install it in a virtual environment inside of the folder where this script is placed.

On Linux or Mac you can do:

```
cd fanzine/
python3 -m venv venv
source venv/bin/activate
pip install pypdf
```

On Windows, you have to replace the `source` command by:

```
source venv/Scripts/activate
```

with Git Bash or with the Microsoft own shells:

```
venv\Scripts\activate
```

You only need to do it once, before starting the script for the first time in Scribus.

## Running the fanzine script

The script can be launched from inside of Scribus and will load pypdf from the venv.
