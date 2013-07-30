html_template = u"""<!DOCTYPE html>
<html>
    <head>
        <title>%(title)s</title>
        <link rel="stylesheet" type="text/css" href="/css/styles.css">
    </head>
    <body>
        <div id="wikid-content">
            <aside id="wikid-sidebar">
                <div id="wikid-toc"></div>
                <div id="wikid-search">
                    <input type="text" placeholder="Search...">
                    <div class="results"></div>
                    <a href="#" class="cancel">X</a>
                </div>
            </aside>
            <div id="wikid-body">
            %(body)s
            </div>
        </div>
        <script src="/js/jquery.js"></script>
        <script src="/js/index.js"></script>
        <script src="/js/toc.js"></script>
        <script src="/js/main.js"></script>
    </body>
</html>"""