# Introduction

[`ng2web`](https://github.com/davep/ng2web) is one in a [long line of Norton
Guide tools I've written over the latest couple or so
decades](https://www.davep.org/norton-guides/). It is, in effect, a
replacement for [`w3ng`](https://github.com/davep/w3ng) and
[`ng2html`](https://github.com/davep/ng2html).

As for what it does: it will take a [Norton Guide
file](https://en.wikipedia.org/wiki/Norton_Guides) and turn the content into
a collection of HTML pages, which you can then incorporate into a web site.

# Usage

The command is called `ng2web` and all command line options can be found
with:

```sh
ng2web --help
```

giving output like this:

```bash exec="on" result="text"
ng2web --help
```

## `--index`

By default `ng2web` generates all pages with names that are prefixed with
the filename of the guide (minus the extension) and, for all pages relating
to short and long entries, including the byte offset of the entry in the
guide; this means that amongst the generated pages there's no obvious
starting location.

Add the `--index` switch to tell `ng2web` to always generate the first entry
in the guide as the file `index.html`.

## `--output`

Use this switch to optionally specify the output directory for the generated
HTML. By default all HTML files will be generated in the current directory.

## `--templates`

Use this switch to optionally specify a location to look for templates that
will override the default templates (see later in this document for details
on how to use templates to control the output of `ng2web`).

[//]: # (index.md ends here)
