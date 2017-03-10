import os.path, re, urlparse, urllib2

def get_file_name(url):
    return os.path.split(urlparse.urlparse(url).path)[1]

def get_content_from_url(url, key):
    file_name = 'nfc_'+get_file_name(url)+key
    if os.path.exists('/tmp/'+file_name):
        return open('/tmp/'+file_name).read()
    else:
        user_agent = 'Wget/1.16'
        req = urllib2.Request(url, headers={'User-Agent': user_agent})
        content = urllib2.urlopen(req).read()
        f = open('/tmp/'+file_name, 'w')
        f.write(content)
        f.close()
        return content

def make_domain_group():
    res = {}
    dre = re.compile(r'\s*<tr[^<>]+><td class="first"><[^<>]+>([^<>]+)</a>.+?<td class="blocked"[^<>]+>(\d+)%</td>.*')
    for page in xrange(211):
        url = 'https://en.greatfire.org/search/domains?page='+str(page)
        try:
            content = get_content_from_url(url, str(page)).split('\n')
        except:
            print 'get_content_from_url error: ', url
            try:
                content = get_content_from_url(url, str(page)).split('\n')
            except:
                print 'get_content_from_url error again: ', url
                raise

        for line in content:
            #<tr class="odd"><td class="first"><a href="/toonel.net">toonel.net</a></td><td>May 2011</td><td class="blocked" style="background-size: 100%;">100%</td><td class="tags"><a href="/search/blocked" class="tag">Blocked</a>, <a href="/search/domains" class="tag active">Domains</a>, <a href="/search/urls" class="tag">URLs</a></td> </tr>
            r = dre.match(line)
            if r:
                domain = r.group(1)
                blocked = int(r.group(2))
                if domain.startswith('http://') or domain.startswith('https://'):
                    domain = domain[domain.index('//')+2:]
                res[domain] = blocked
    
    res = list(res)

    def sort_fun(o):
        x = o.split('.')
        if x[-2] in ('com', 'co') and len(x)>=3:
            return x[-3]
        else:
            return x[-2]

    res.sort(key=sort_fun)
    
    with open('bdc.txt', 'w') as f:
        for item in res:
            f.write('.'+item+'\n')

if __name__=='__main__':
    make_domain_group()

