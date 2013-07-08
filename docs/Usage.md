# Usage

*Wikid* is simple but there are still some things you'll want to know so that you can use it. This section goes over those things and explains a little bit about how *wikid* works at the same time.

## Installation

This is pretty easy if you already have python installed.

    :::bash
    pip install wikid

You can also install it from source.

    :::bash
    git clone git://github.com/elishacook/wikid.git
    cd wikid
    python setup.py install

Either way, you will get a script installed called `wikid`. Here's the help for it.

    :::bash
    $ wikid -h
    usage: __init__.py [-h] [--path PATH] [--output OUT] [--port PORT] [--serve]

    Run a wikid wiki.

    optional arguments:
      -h, --help    show this help message and exit
      --path PATH   The path where the wiki files can be found. The default value
                    is './docs'.
      --output OUT  The path where the html files will be written. The default
                    value is './docs-html'.
      --port PORT   The port on which to start the server. The default value is
                    3001.
      --serve       Start a wiki server.

## Built-in web server

*Wikid* can run a web server. The server reads your Markdown files on request so you can work on your docs and reload the page to see changes. This server is not high or even medium performance. It is a toy and it's only purpose is developing your wiki. To share the wiki files with a lot of people it is suggested that you send them the files directly, or use a medium-to-high performance web server and use it to medium-to-high-ly performance serve the statically generated HTML files you can learn about in the next section.

Here's how you start a server that will server all the files in the directory `./my-wiki-directory` on port 8000:

    :::bash
    wikid --serve --path=./my-wiki-directory --port=8000

## Building static files

*Wikid* can generate HTML files from your wiki. It will create a new output directory, copy all of the non-Markdown files from the input directory and generate one HTML file per Markdown file. So if we have a directory structure like this:

    my-project/
        docs/
            images/
                hairpiece-diagram.jpg
                unicorn-tank-action-shot.jpg
            index.md
            how-to-dance.md
            how-to-dance-crappy.md
        src/
        README
        LICENSE

and we run this command from the `my-project` directory:

    :::bash
    wikid --path=./docs --output=./docs-dist

we will end up with this:

    my-project/
        docs/
            images/
                hairpiece-diagram.jpg
                unicorn-tank-action-shot.jpg
            index.md
            how-to-dance.md
            how-to-dance-crappy.md
        docs-dist/
            css/
                styles.css
            images/
                hairpiece-diagram.jpg
                unicorn-tank-action-shot.jpg
            js/
                jquery.js
                search-index.js
                search.js
            index.html
            how-to-dance.html
            how-to-dance-crappy.html
        src/
        README
        LICENSE

That's what I said it would do plus there are some more files. The `js` and `css` directories are copied from the `wikid` source folder and `search-index.js` is the search index for your whole wiki. You can add your own styles and scripts too.

*wikid* is smart about paths inside links and `img` tags and stuff so you don't have to worry about it. If you have a link that works when you use the web server it will work in the static files too.

## Markdown flavor

*Wikid* uses [this Markdown package](http://packages.python.org/Markdown/). I'll just quote that page:

> This is a Python implementation of John Gruber's [Markdown](http://daringfireball.net/projects/markdown/). It is almost completely compliant 
> with the reference implementation, though there are a few very minor [differences](http://packages.python.org/Markdown/index.html#differences). See John's 
> [Syntax Documentation](http://daringfireball.net/projects/markdown/syntax) for the syntax rules.

In addition, several [extensions](http://packages.python.org/Markdown/extensions/) are enabled. These are extra, codehilite, headerid, toc and wikilinks.
