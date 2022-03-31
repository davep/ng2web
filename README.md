# ng2web - Norton Guide to HTML conversion tool

Currently a work in progress to help test the work being done on
[`ngdb.py`](https://github.com/davep/ngdb.py).

## Quick and dirty introduction

Install with `pip` or a similar tool and then you'll have a `ng2web` command
available. Given a Norton Guide database, just run the tool like this:

```sh
$ ng2web C52G01B.NG
```

and you'll end up with lots of HTML files and a CSS file in your current
directory. If you'd prefer to output elsewhere, use ```--output```:

```sh
$ ng2web C52G01B.NG --output=web
```

More comprehensive documentation is to come, plus more features and options
(including documentation on how to override the default look/feel of the
generated HTML.)

[//]: # (README.md ends here)
