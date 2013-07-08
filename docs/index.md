# Wikid

*The stupid-simple wiki*

To get started right away, see [[Usage]].

Hi there. This document is about *wikid* (pronounce how you like), a really simple [wiki](http://en.wikipedia.org/wiki/Wiki). This wiki is so simple, in fact, that I hesitate even to call it a wiki. You see, it doesn't use a database, or have authorization or even users. There's no history, no email notifications, no media uploading, no discussions, no metadata and no UI for managing pages.

So, you may ask, why the hell should anyone use it? That's a very good question that I will answer now. Even though *wikid* doesn't have any of those fine things listed in the last paragraph, there are some other tools that do and they work nicely with *wikid*. Those tools are a modern operating system, a text editor and a modern revision control system, like [git](http://git-scm.com/). A modern operating system provides loads of support for authoring different kinds of media files, a text editor let's you write [Markdown](http://daringfireball.net/projects/markdown/), the language of *wikid* and an rcs provides revision history and attribution of changes.

Harumph--I imagine you saying--that's all well and good for you, but what about regular users that like to have GUIs and cloud storage and whatnot? Well--I imagine me saying back to you--there are a lot of software packages like that and you should go find one. *Wikid* is especially made for developers.

## Simpler documentation

There are lots of tools for generating API documentation which is super helpful if you already have a grasp on how a system works. A lot of these tools also support building more guide-like docs. However, these systems tend to be pretty heavy and/or use are based directly on source code comments and there is often a need to start documenting ideas, todos, etc., well before code is written or an environment chosen.

And then there's the multimedia question. Where do we put our diagrams, audio and video files? We can make a directory for it in the src tree but then we've got part of the documentation in comments in the code and they are linking to files in some other directory. This makes documentation harder to think about and therefore harder to maintain.

Then there's the approach where we use some kind of project-specific Wiki or CMS solution. Waaaaay better authoring capabilities but again, the docs are somewhere far from the code. Far away and out of sight. Think back to all those times you created a wiki and said "This time, I'm really going to update the docs every time I refactor." Did it happen? Reeeeeeeeally? Wouldn't it be more likely to happen if the docs folder was staring you in the face every time you looked at the project's source tree?

## Plain-text to the rescue!

Many developers have been using plain-text formats to document projects for awhile now. The reason is because it is very nice. The reason it is very nice is that unstructured text documents are super easy to create and share and plain text has unparalleled expressive power (for more, see [Books](http://en.wikipedia.org/wiki/Book)). There is really no substitute for good old plain text. For that reason there are bunches of other documentation generators that work similarly, soooo...

## Why another one?

Yeah. I don't have an excuse for writing this one except I felt like it. Also, *wikid* has a unique search function that I couldn't find anywhere else.

## Roadmap

I want to add or change some things:

* Multimedia support (embedd.ly, maybe?)
* Twitter support, so you can see a tweet box on a docs page
* Update the visual design
* Smaller search index size
* Finish this documentation

If you think of something that would make *wikid* work better for you [let me know](https://github.com/elishacook/wikid/issues).
