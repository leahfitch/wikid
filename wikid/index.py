from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
import math
import json

stop_words = set("a,able,about,above,abst,accordance,according,accordingly,across,act,actually,added,adj,affected,affecting,affects,after,afterwards,again,against,ah,all,almost,alone,along,already,also,although,always,am,among,amongst,an,and,announce,another,any,anybody,anyhow,anymore,anyone,anything,anyway,anyways,anywhere,apparently,approximately,are,aren,arent,arise,around,as,aside,ask,asking,at,auth,available,away,awfully,b,back,be,became,because,become,becomes,becoming,been,before,beforehand,begin,beginning,beginnings,begins,behind,being,believe,below,beside,besides,between,beyond,biol,both,brief,briefly,but,by,c,ca,came,can,cannot,can't,cause,causes,certain,certainly,co,com,come,comes,contain,containing,contains,could,couldnt,d,date,did,didn't,different,do,does,doesn't,doing,done,don't,down,downwards,due,during,e,each,ed,edu,effect,eg,eight,eighty,either,else,elsewhere,end,ending,enough,especially,et,et-al,etc,even,ever,every,everybody,everyone,everything,everywhere,ex,except,f,far,few,ff,fifth,first,five,fix,followed,following,follows,for,former,formerly,forth,found,four,from,further,furthermore,g,gave,get,gets,getting,give,given,gives,giving,go,goes,gone,got,gotten,h,had,happens,hardly,has,hasn't,have,haven't,having,he,hed,hence,her,here,hereafter,hereby,herein,heres,hereupon,hers,herself,hes,hi,hid,him,himself,his,hither,home,how,howbeit,however,hundred,i,id,ie,if,i'll,im,immediate,immediately,importance,important,in,inc,indeed,index,information,instead,into,invention,inward,is,isn't,it,itd,it'll,its,itself,i've,j,just,k,keep,keeps,kept,kg,km,know,known,knows,l,largely,last,lately,later,latter,latterly,least,less,lest,let,lets,like,liked,likely,line,little,'ll,look,looking,looks,ltd,m,made,mainly,make,makes,many,may,maybe,me,mean,means,meantime,meanwhile,merely,mg,might,million,miss,ml,more,moreover,most,mostly,mr,mrs,much,mug,must,my,myself,n,na,name,namely,nay,nd,near,nearly,necessarily,necessary,need,needs,neither,never,nevertheless,new,next,nine,ninety,no,nobody,non,none,nonetheless,noone,nor,normally,nos,not,noted,nothing,now,nowhere,o,obtain,obtained,obviously,of,off,often,oh,ok,okay,old,omitted,on,once,one,ones,only,onto,or,ord,other,others,otherwise,ought,our,ours,ourselves,out,outside,over,overall,owing,own,p,page,pages,part,particular,particularly,past,per,perhaps,placed,please,plus,poorly,possible,possibly,potentially,pp,predominantly,present,previously,primarily,probably,promptly,proud,provides,put,q,que,quickly,quite,qv,r,ran,rather,rd,re,readily,really,recent,recently,ref,refs,regarding,regardless,regards,related,relatively,research,respectively,resulted,resulting,results,right,run,s,said,same,saw,say,saying,says,sec,section,see,seeing,seem,seemed,seeming,seems,seen,self,selves,sent,seven,several,shall,she,shed,she'll,shes,should,shouldn't,show,showed,shown,showns,shows,significant,significantly,similar,similarly,since,six,slightly,so,some,somebody,somehow,someone,somethan,something,sometime,sometimes,somewhat,somewhere,soon,sorry,specifically,specified,specify,specifying,still,stop,strongly,sub,substantially,successfully,such,sufficiently,suggest,sup,sure,t,take,taken,taking,tell,tends,th,than,thank,thanks,thanx,that,that'll,thats,that've,the,their,theirs,them,themselves,then,thence,there,thereafter,thereby,thered,therefore,therein,there'll,thereof,therere,theres,thereto,thereupon,there've,these,they,theyd,they'll,theyre,they've,think,this,those,thou,though,thoughh,thousand,throug,through,throughout,thru,thus,til,tip,to,together,too,took,toward,towards,tried,tries,truly,try,trying,ts,twice,two,u,un,under,unfortunately,unless,unlike,unlikely,until,unto,up,upon,ups,us,use,used,useful,usefully,usefulness,uses,using,usually,v,value,various,'ve,very,via,viz,vol,vols,vs,w,want,wants,was,wasn't,way,we,wed,welcome,we'll,went,were,weren't,we've,what,whatever,what'll,whats,when,whence,whenever,where,whereafter,whereas,whereby,wherein,wheres,whereupon,wherever,whether,which,while,whim,whither,who,whod,whoever,whole,who'll,whom,whomever,whos,whose,why,widely,willing,wish,with,within,without,won't,words,world,would,wouldn't,www,x,y,yes,yet,you,youd,you'll,your,youre,yours,yourself,yourselves,you've,z,zero".split(','))

class TextCollectingTreeprocessor(Treeprocessor):
    
    def __init__(self, *args, **kwargs):
        Treeprocessor.__init__(self, *args, **kwargs)
        self.last_header_id = ""
        self.text = {
            "": {
                "text": []
            }
        }
    
    def run(self, root):
        for elm in root.iter():
            if elm.tag in ['h1','h2','h3','h4','h5','h6']:
                self.last_header_id = elm.attrib['id']
                self.text[self.last_header_id] = {
                    'title': elm.text,
                    'text': []
                }
            elif elm.text:
                self.text[self.last_header_id]['text'].append(elm.text)


class TextCollectingExtension(Extension):

    def __init__(self, *args, **kwargs):
        Extension.__init__(self, *args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        self.treeprocessor = TextCollectingTreeprocessor(md)
        md.treeprocessors.add('textcollector', self.treeprocessor, '<toc')

illegal_start_chars = '\'"({['
illegal_end_chars = '.?!,:;\'")}]'
def remove_illegal_chars(term):
    if term[-1] in illegal_end_chars:
        term = term[:-1]
    if not term:
        return term
    if term[0] in illegal_start_chars:
        term = term[1:]
    return term


def clean_term(term):
    return remove_illegal_chars(term.strip().lower())

def split_terms(text):
    return text.split()

def get_terms(text):
    terms = {}
    raw_terms = split_terms(text)

    for i,t in enumerate(raw_terms):
        t = clean_term(t)
        if len(t) < 3 or t in stop_words:
            continue
        if t not in terms:
            start_index = max(i-3, 0)
            end_index = min(i+4, len(raw_terms))
            context = ' '.join(raw_terms[start_index:end_index])
            context = remove_illegal_chars(context)

            if start_index > 0:
                context = '...' + context
            if end_index < len(raw_terms):
                context = context + '...'

            terms[t] = {
                'context': context,
                'count': 1
            }
        else:
            terms[t]['count'] += 1
    return terms


def get_annotated_docs(raw_docs):
    term_totals = {}
    docs = []

    for path, text in raw_docs.items():
        doc = {'path': path}
        raw_terms = ' '.join(text['text'])
        if 'title' in text:
            doc['title'] = text['title']
            raw_terms += ' '+text['title']
            title_terms = [clean_term(t) for t in split_terms(text['title'])]
        else:
            title_terms = None
        terms = get_terms(raw_terms)
        for t,info in terms.items():
            if t in term_totals:
                term_totals[t] += 1
            else:
                term_totals[t] = 1
            if title_terms and t in title_terms:
                del info['context']
        doc['terms'] = terms
        docs.append(doc)

    for doc in docs:
        for t,info in doc['terms'].items():
            info['relevance'] = float(info['count']) * math.log(float(len(docs)) / term_totals[t])

    return docs


def insert_into_trie(trie, key, value):
    for c in key:
        if 'c' not in trie:
            trie['c'] = {}
        if c in trie['c']:
            trie = trie['c'][c]
        else:
            new_trie = {'c':{}}
            trie['c'][c] = new_trie
            trie = new_trie
    if 'v' not in trie:
        trie['v'] = []
    trie['v'].append(value)


def compress_trie(trie, parent, key):
    if trie.get('c', 0) == 0:
        return
    for c, child in trie['c'].items():
        compress_trie(child, trie, c)
    if len(trie['c']) == 1 and 'v' not in trie:
        child_key, child = trie['c'].items()[0]
        if child.get('v'):
            trie['v'] = child['v']
        if 'c' in child:
            trie['c'] = child.get('c')
        else:
            del trie['c']
        parent['c'][key + child_key] = trie
        del parent['c'][key]
    if 'c' in trie and len(trie['c']) == 0:
        del trie['c']


def make_index(raw_docs):
    """Create an inverted index for all the documents. The index is returned as a radix trie.

    `raw_docs` -- a dict from {doc_path} -> {doc_text}
    """
    docs = get_annotated_docs(raw_docs)
    trie = {}

    for doc in docs:
        for term, info in doc['terms'].items():
            value = {
                'p': doc['path'],
                'r': info['relevance']
            }

            if 'context' in info:
                value['c'] = info['context']

            if 'title' in doc:
                value['t'] = doc['title']

            insert_into_trie(trie, term, value)
    
    for c in trie['c']:
        compress_trie(trie['c'][c], trie, c)

    return 'wikid_search_trie = ' + json.dumps(trie) + ';'
