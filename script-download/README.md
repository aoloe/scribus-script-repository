This script will be created during

http://www.coactivate.org/projects/zurich-sprint/project-home

# plans


Since the new scripter currently does not run, i'll be creating python / pyqt program that will be listing and downloading scripts from the same github repository mentioned above.

It should be easy to get that script to run inside of scribus, once scribus itself will be ready.

The plan is to:

- define a metadata file for each script (directory) and (possibly) one for the full repository
- define and create dialogs for managing the (list of ) repository(ies) and the local storage.
- write the code that downloads the scripts (through http or git?),
- and to detect which scripts should be updated.


# The repository's structure

- manifest.json
- README.md
- the-script/
  - the-script.py
  - README.md
  - other-files/

Remarks:
- The names are case sensitive
- Only the main script file should be directly placed in the script's directory. All other files that are to be downloaded, should be in one sub-directory.

# Downloading the files

- When downloading a script, only the files listed in the manifest are downloaded.
- The list of files in the repository is queried through an HTTP request to the Github API.
- The single files are downloaded by HTTP through Github's RAW interface.

# Running the script

- The script should get into the official Scribus source code and appear in the Scripts menu entry.
- By default no repositories should be pre-configured (adding an official Scribus repository does not make much sense for now, since Scripts that could be in there, would be in the Scribus scripts directory anyway).

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

    {
        "name" : {
            "en" : "The GitHub scripts collection",
        },
        "scripts_ignore" : [
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
            "target_path" : "/usr/scribus/share/scribus/scripts/"
            "script" : [
                {
                    "path" : "document-scrambling/document-scrambling.py",
                    "name" : "Document scrambling"
                }
            ]
        }
    ]

# Dialogs

- An uninstalled script is selected

        [ "Repository url"   ] [ Github |v] [ Add ]

        [ The GitHub script collection          |v]

        Search: [                                 ]

        +---------------------------------------+-+
        |> Typographic grid                     |^|
        |  Document scrambling                ✓ | |
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

- An installed script is selected

        [ "Repository url"   ] [ Github |v] [ Add ]

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

- Alternative view with radio buttons instead of drop downs for the list of active repositories

        [ "Repository url"   ] [ Github |v] [ Add ]
        (o) The GitHub script collection
        ( ) Another repository

        Search: [                                 ]

        +---------------------------------------+-+
        |> Typographic grid                    <|^|
        |  Document scrambling                ✓ | |
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

We also need a settigns dialog:
- where to store the scripts
- add the repositories?

# Notes
- without introducing the github credentials, only 60 connections per hour and repository (or IP?)

# Todo

- show a ✓ in the script list (for isntalled script)
- how to store the script's settings (list of repositories, installed scripts, 
- find out how to close the dialog (where to place a close push botton)
- find out how to close the dialog by pressing ESC
- only show one row of buttons, switched according to the (installed) status of the selected script (add / run + remove)
- implement adding the repositories
- extend the repository manifest to allow the translation of the script names (as shown in the list of scripts)
- show the script description when a script is selected
- define where to put the scripts and how to avoid conflicht among scripts with the same name but from different repositories (refuse to install is an option... or renaming at install?)

# Development resources

- http://stackoverflow.com/questions/24111717/how-to-bind-buttons-in-qt-quick-to-python-pyqt-5
- a good example for a qml dialog: https://github.com/ioriayane/KanmusuMemory/blob/master/qml/KanmusuMemory/TimerSetting.qml
- lists:
  - https://qt-project.org/wiki/Selectable-list-of-Python-objects-in-QML
- further reading: [QML for desktop apps ](https://www.youtube.com/watch?v=kvWeE3kurEQ)
- a (for me too complicated) example on how to use a python model for qml lists: https://qt-project.org/wiki/Selectable-list-of-Python-objects-in-QML
- tableview:
  - how to make items editable: http://blog.qt.digia.com/blog/2011/05/26/table-view-with-qt-quick/

# Snippets

            Item {
                width: 50; height: 20
                ListModel {
                    id: fruitModel

                    ListElement {
                        name: "Apple"
                        cost: 2.45
                    }
                    ListElement {
                        name: "Orange"
                        cost: 3.25
                    }
                    ListElement {
                        name: "Banana"
                        cost: 1.95
                    }
                }

                ScrollView {
                     ListView {
                        id: lista
                        anchors.fill: parent
                        model: fruitModel
                        delegate: Row {
                             Text { text: "Fruit: " + name }
                             Text { text: "Cost: $" + cost }
                        }
                     }
                }

                ScrollBar {
                     id: vertical
                     flickableItem: lista
                     orientation: Qt.Vertical
                     anchors { right: lista.right; top: lista.top }
                 }
            }
