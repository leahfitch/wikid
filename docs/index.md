# Wikid: The stupid-simple wiki

Hi there. This document is about *wikid* (pronounce how you like), a really simple [wiki](http://en.wikipedia.org/wiki/Wiki). This wiki is so simple, in fact, that I hesitate even to call it a wiki. You see, it doesn't use a database, or have authorization or even users. There's no history, no email notifications, no media uploading, no discussions, no metadata and no UI for managing pages.

So, you may ask, why the hell should anyone use it? That's a very good question that I will answer now. Even though *wikid* doesn't have any of those fine things listed in the last paragraph, there are some other tools that do and they work nicely with *wikid*. Those tools are a modern operating system, a text editor and a modern revision control system, like [git](http://git-scm.com/). A modern operating system provides loads of support for authoring different kinds of media files, a text editor let's you write [Markdown](http://daringfireball.net/projects/markdown/), the language of *wikid* and an rcs provides revision history and attribution of changes.

Harumph--I imagine you saying--that's all well and good for you, but what about regular users that like to have GUIs and cloud storage and whatnot? Well--I imagine me saying back to you--there are a lot of software packages like that and you should go find one. *Wikid* is especially made for developers.

## Developer documentation is ok, I guess

Ok, actually the state of developer documentation is pretty awful. There are lots of tools for generating API documentation which is super helpful if you already have a grasp on how a system works. Some languages/tools let you write more informal docs in comments and compile them into something book-like but this is stretching commenting a little far beyond its purpose, especially when you are trying to communicate high level design that doesn't necessarily make sense to put in one particular source code file.

And then there's the multimedia question. Where do we put our diagram, mp3 and DivX files? We can make a directory for it in the src tree but then we've got part of the documentation in comments in the code and they are linking to files in some other directory. This makes documentation harder to think about and therefore harder to maintain.

Then there's the approach where we use some kind of project-specific Wiki or CMS solution. Waaaaay better authoring capabilities but again, the docs are somewhere far from the code. Far away and out of sight. Think back to all those times you created a wiki and said "This time, I'm really going to update the docs every time I refactor." Did it happen? Reeeeeeeeally? Wouldn't it be more likely to happen if the docs folder was staring you in the face every time you looked at the project's source tree?

## Plain-text to the rescue!

Many developers have been using plain-text formats to document projects for awhile now. The reason is because it is very nice. The reason it is very nice is that unstructured text documents have unparalleled expressive power (for more, see [Books](http://en.wikipedia.org/wiki/Book)). There is really no substitute for good old plain text. For that reason there are bunches of other documentation generators that work similarly, soooo...

## Another one? Really?

Yeah. I don't have an excuse for writing this one except I felt like it. Also, *wikid* has search and I couldn't find one with search.

## Roadmap

I want to add or change some things:

* Multimedia support (embedd.ly, maybe?)
* Twitter support, so you can see a tweet box on a docs page
* Update the visual design
* Smaller search index size
* Finish this documentation

If you think of something that would make *wikid* work better for you [let me know](https://github.com/elishacook/wikid/issues).

# Documentation

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

That's what I said it would do plus there are some more files. The `js` and `css` directories are copied from the `wikid` source folder and `search-index.js` is the search index for your whole wiki. You can add your own styles and scripts too. That's covered in the section on [customization](#customize).

*wikid* is smart about paths inside links and `img` tags and stuff so you don't have to worry about it. If you have a link that works when you use the web server it will work in the static files too.

## Markdown flavor

*Wikid* uses [this Markdown package](http://packages.python.org/Markdown/). I'll just quote that page:

> This is a Python implementation of John Gruber's [Markdown](http://daringfireball.net/projects/markdown/). It is almost completely compliant 
> with the reference implementation, though there are a few very minor [differences](http://packages.python.org/Markdown/index.html#differences). See John's 
> [Syntax Documentation](http://daringfireball.net/projects/markdown/syntax) for the syntax rules.

In addition, several [extensions](http://packages.python.org/Markdown/extensions/) are enabled. These are extra, codehilite, headerid, toc and wikilinks.

## Customize
## Search
