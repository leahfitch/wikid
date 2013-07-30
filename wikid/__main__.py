import argparse
parser = argparse.ArgumentParser(description="Run a wikid wiki.")
parser.add_argument('--src', metavar="PATH", default="./docs", help="The path where the wiki files can be found. The default value is './docs'.")
parser.add_argument('--dst', metavar="OUT", default="./docs-html", help="The path where the html files will be written. The default value is './docs-html'.")
parser.add_argument('--port', metavar="PORT", type=int, default="3001", help="The port on which to start the server. The default value is 3001.")
parser.add_argument('--serve', action="store_true", help="Start a wiki server.")
args = parser.parse_args()

if args.serve:
    print "Not implemented."
else:
    from wikid.buildmd import MarkdownBuilder
    from wikid.project import Project
    builder = MarkdownBuilder(Project(args.src), args.dst)
    builder.run()