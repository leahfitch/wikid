if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run a wikid wiki.")
    parser.add_argument('--path', metavar="PATH", default="./docs", help="The path where the wiki files can be found.")
    parser.add_argument('--output', metavar="OUT", default="./docs-html", help="The path where the html files will be written.")
    parser.add_argument('--port', metavar="PORT", type=int, default="3001", help="The port on which to start the server.")
    parser.add_argument('--serve', action="store_true", help="Start a server that converts the wiki files dynamically.")
    args = parser.parse_args()
    
    if args.serve:
        from wsgiref.simple_server import make_server
        from wikid.wsgi import WikidApp
        app = WikidApp(args.path)
        server = make_server('', args.port, app)
        print "Serving %s on port %s" % (args.path, args.port)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
    else:
        from wikid.build import build_wiki
        build_wiki(args.path, args.output)