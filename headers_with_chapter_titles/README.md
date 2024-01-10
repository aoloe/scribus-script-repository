# Headers with chapter titles

- The text frames for the titles are added to the master pages where they should show up (and, for now, left empty).
- The text frames should be named 'running_title_...' (they need to be unique, so a good name is 'running_title_Normal' for the one in the 'Normal' master page).
- The frame can be made _non printable_ (at the time of writing, there is a bug and the items on the master pages are _printed_ whatever the setting in the master page: https://bugs.scribus.net/view.php?id=17117).
- In the document use the style 'h1' for the titles.
- Run this script.
- The first h1 on the same page or the latest found before are used for the heading of the page (if there are multiple h1 on a page, only the first one is retained).
- Only the pages with a master page containing a 'running_title_' frame get the titles.

## Todo

- [ ] Keep / apply the correct paragraph style for the text in the header.
- [ ] If multiple h1 are defined on a page, the current page should get the first one, the following pages the last one.

