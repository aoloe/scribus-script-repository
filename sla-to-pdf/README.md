# Create PDFs starting from  .sla files

> This folder used to contain a `sla-to-pdf.py` for imposing Scribus A5 or A6 documents to A4 PDFs. The script has been moved to the `imposition` folder and will be merged into `imposition.py`.

Calling the script with a document:

```
$ python3 sla-to-pdf.py document.sla
```

Calling the script with two documents and a config file

```
$ python3 sla-to-pdf.py -config shrink-images.json document.sla other-document.sla
```

Creates `document.pdf` and `other-document.pdf`

```
$ python3 sla-to-pdf.py -files files-list.json
```

where `file-list.json` is:

```json
[
    {"sla": "first.sla"},
    {"sla": "first-final.sla", "pdf": "second.pdf"}
]
```

creates `first.pdf` from `first.sla` and `second.pdf` from `first-final.sla`.

Config values:

<https://impagina.org/scribus-scripter-api/pdf-export/#savepdfoptions>

```
compress = True,
compressmtd = 0,  # automatic
quality = 1,      # high
resolution = 300,
downsample = 300,
```
