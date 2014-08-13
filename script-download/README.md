this script will be created during

http://www.coactivate.org/projects/zurich-sprint/project-home

# plans


since the new scripter currently does not run, i'll be creating python / pyqt program that will be listing and downloading scripts from the same github repository mentioned above.

it should be easy to get that script to run inside of scribus, once scribus itself will be ready.

the plan is to:

- define a metadata file for each script (directory) and (possibly) one for the full repository
- define and create dialogs for managing the (list of ) repository(ies) and the local storage.
- write the code that downloads the scripts (through http or git?),
- and to detect which scripts should be updated.


# The downloader settings

- list of repositories:
  - url
  - type (github, ...)
- where you want the scripts to be placed
 
# The repository's structure

- manifest.json
- README.md
- the-script/
  - the-script.py
  - README.md
  - other-files/

Remarks:
- the names are case sensitive

# Metadata

## The repository's manifest

    {
        "name" : {
            "en" : "The GitHub scripts collection",
        },
        "scripts" : [
            "typographic-grid",
            "document-scrambling"
        ]
    }

## The script's manifest

    {
        "name" : {
            "en" : "Typographic grid"
        }
        "web" : "https://github.com/aoloe/scribus-script-repository/",
        "repository" : "https://github.com/aoloe/scribus-script-repository/",
        "tickets" : "https://github.com/aoloe/scribus-script-repository/issues/",
        "license" : "MIT",
        "authors" : [
            {
                "name" : "Ale Rimoldi",
                "email" : "ale@graphicslab.org"
            }
        ]
        "script_version" : "1.0",
        "min_scripter_version" : "1.0",
        "max_scripter_version" : "1.0",
        "min_scribus_version" : "1.4.0",
        "max_scribus_version" : "",
        "description" : {
            "en" : "Create the typographic grid and the baseline grid based on some parameters for the current page.",
        }
        "readme" : "https://github.com/aoloe/scribus-script-repository/README.md",
        "status" : "stable",
        "files" : [
            "typographic-grid.py"
        ]
    }

## The local preferences

    [
        {
            "repository" : "https://github.com/aoloe/scribus-script-repository/",
            "name" : "The GitHub scripts collection",
            "script" : [
                {
                    "path" : "document-scrambling/document-scrambling.py",
                    "name" : "Document scrambling"
                }
            ]
        }
    ]

# Dialogs

    [ Repository url       ] [ Type |v] [ Add ]

    [ The GitHub script collection          |v]

    Search: [                                 ]

    +---------------------------------------+-+
    |> Typographic grid                     |^|
    |  Document scrambling                i | |
    |                                       | |
    |                                       | |
    |                                       |v|
    +---------------------------------------+-+
    +-----------------------------------------+
    | Create the typographic grid and the     |
    | baseline grid based on some parameters  |
    | for the current page.                   |
    +-----------------------------------------+
    [ More ] [ Add ]


    [ Repository url       ] [ Type |v] [ Add ]

    [ The GitHub script collection          |v]

    Search: [                                 ]

    +---------------------------------------+-+
    |  Typographic grid                     |^|
    |> Document scrambling               ✓ <| |
    |                                       | |
    |                                       | |
    |                                       |v|
    +---------------------------------------+-+
    +-----------------------------------------+
    | Create the typographic grid and the     |
    | baseline grid based on some parameters  |
    | for the current page.                   |
    +-----------------------------------------+
    [ Run ] [ More ] [ Delete ]
