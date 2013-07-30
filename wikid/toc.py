import json

class TOCIndexer(object):
    
    def __init__(self, documents):
        self.documents = documents
        self.headers = []
        self.build()
        
    def build(self):
        self.headers = []
        for doc in self.documents:
            if not doc['root']:
                continue
            for elm in doc['root'].iter():
                if elm.tag in ['h1','h2','h3','h4','h5','h6'] and elm.attrib['id']:
                    self.headers.append({
                        'path': doc['path'],
                        'text': elm.text,
                        'depth': int(elm.tag[1])
                    })
        
    def to_js(self):
        return u'var wikid_toc = ' + json.dumps(self.headers)