## Introduction

[`ng2web`](https://github.com/davep/ng2web) is one in a [long line of Norton
Guide tools I've written over the latest couple or so
decades](https://www.davep.org/norton-guides/). It is, in effect, a
replacement for [`w3ng`](https://github.com/davep/w3ng) and
[`ng2html`](https://github.com/davep/ng2html).

As for what it does: it will take a [Norton Guide
file](https://en.wikipedia.org/wiki/Norton_Guides) and turns the content
into a collection of HTML pages, which you can then incorporate into a web
site.

## Command line options

The command is called `ng2web` and all command line options can be found
with:

```sh
ng2web --help
```

giving output like this:

```bash exec="on" result="text"
ng2web --help
```

The key options are:

### `--index`

By default `ng2web` generates all pages with names that are prefixed with
the filename of the guide (minus the extension) and, for all pages relating
to short and long entries, including the byte offset of the entry in the
guide; this means that amongst the generated pages there's no obvious
starting location.

Add the `--index` switch to tell `ng2web` to always generate the first entry
in the guide as the file `index.html`.

### `--output`

Use this switch to optionally specify the output directory for the generated
HTML. By default all HTML files will be generated in the current directory.

### `--templates`

Use this switch to optionally specify a location to look for templates that
will override the default templates (see [the next section](#templates) in
this document for details on how to use templates to control the output of
`ng2web`).

## Templates

The output of `ng2web` is styled using a collection of templates. The
builtin templates are designed to give the output a bit of a classic Norton
Guide reader look.

![Default look of the output](images/default-output-look.png)

There are a number of templates that control each of the major types of
content inside a Norton Guide.

### The base template (`base.html`)

The base template is the base for the other templates that output a specific
type of page.

```jinja
--8<-- "src/ng2web/templates/base.html"
```

If you wish to change the look and feel of every page in the output, this is
probably the template you want to [override](#overriding-templates).

### The about page template (`about.html`)

This is the template for the "about" page of the output; typically this is
where the credits for the guide will be shown.

```jinja
--8<-- "src/ng2web/templates/about.html"
```

### The base entry template (`entry.html`)

This is the template that both [short](#the-short-entry-template-shorthtml)
and [long](#the-long-entry-template-longhtml) entry templates build upon.

```jinja
--8<-- "src/ng2web/templates/entry.html"
```

### The short entry template (`short.html`)

This is the template for creating pages from short entries in the guide.
Short entries typically have no "see also" section and also have lines that
link elsewhere.

```jinja
--8<-- "src/ng2web/templates/short.html"
```

### The long entry template (`long.html`)

This is the template for creating pages from long entries in the guide. Long
entries typically have an optional "see also" section and have lines that
don't link anywhere else; the text content of a long entry is simply text,
not links that go elsewhere.

```jinja
--8<-- "src/ng2web/templates/long.html"
```

### Link navigation include (`inc/nav-link.html`)

This is a utility include template that is used by [the base
template](#the-base-template-basehtml) to emit the navigation links that
appear at the top of the page: the *About*, *Previous*, *Up* and *Next*
links.

```jinja
--8<-- "src/ng2web/templates/inc/nav-link.html"
```

### The stylesheet template

The stylesheet for the site is generated using this template.

```css
--8<-- "src/ng2web/templates/base.css"
```

As you'll see: the bulk of this file is just static CSS; the only part
making use of templating being the `span` foreground and background colour
utility classes; the styles being `.bg0` through `.bg15` and `.fg0` through
`.fg15`. By default the expansion is a selection of web colours that best
match the colours common in text modes on PC/DOS systems.

The default selection is:

0. black
1. navy
2. green
3. teal
4. maroon
5. purple
6. olive
7. silver
8. gray
9. blue
10. lime
11. aqua
12. red
13. fuchsia
14. yellow
15. white

## Overriding templates

### Custom template locations

By default, when a template is needed, `ng2web` will look in the following
locations, in the following order. Once a template is found that one is
used.

1. The directory provided with [the `--templates` switch](#-templates).
2. `./templates/`, below the current working directory, if it exists.
3. `ng2web`'s own default templates.

!!! tip

    You only need to make a copy of a template you actually want to change.
    Overriding one template doesn't mean you need to make a copy of all of
    them. Each tamplet is individually looked for using these rules.

## Global values

The following global variables are available in the templates:

### `generator`

The generator name for `ng2web`, this will include the version number of
`ng2web` and of `ngdb` ([the library that `ng2web` is built
on](https://github.com/davep/ngdb.py)).

An example looks like:

```
ng2web v0.1.1 (ngdb v0.12.0)
```

### `guide`

A reference to the guide object that is being used to read the Norton Guide
file. This allows access to [any of the properties and methods of
`ngdb.NortonGuide`](https://blog.davep.org/ngdb.py/library-contents/guide/).

!!! warning

    It's best to restrict use of this to read-only properties; calling
    anything that may change the state of the underlying guide object could
    cause unexpected results.

### `about_url`

The URL for the about page that will be generated.

### `stylesheet`

The name of the stylesheet that will be generated.

## Available filters

The following filters are made available in the templates:

### `urlify`

Takes a particular linked option within a guide and turns it into a web
link. Most often used when generating links in entries; for example:

```jinja
<a class="line" href="{{ line|urlify }}">{{ line.text|toHTML }}</a>
```

### `toHTML`

Takes some text and makes it safe to use in a HTML document. This can also
be seen being used in the example given above.

### `title`

Takes a guide entry and emits a suitable title for it. For example:

```jinja
{% block title %}{{ entry|title }}{% endblock %}
```

The title will be rendered as path of sorts, which will include the title of
the guide, the title of the menu the entry relates to, and the prompt from
the menu that the entry relates to. For example:

```
MrDebug for CA-Clipper Ver 1.20.147ß » Reference » Menus
```

!!! tip

    As a special case, if you pass `None` as the entry `title` will simply
    output the title of the guide.

## Getting help

If you need some help using `ng2web`, or have ideas for improvements, please
feel free to drop by [the
discussions](https://github.com/davep/ng2web/discussions) and ask or
suggest. If you believe you've found a bug please feel free to [raise an
issue](https://github.com/davep/ng2web/issues).

[//]: # (index.md ends here)
