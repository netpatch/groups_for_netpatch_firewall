import os, urlparse, urllib2, math, urllib

domain_source_urls = [
    ('https://pgl.yoyo.org/as/serverlist.php?hostformat=nohtml&showintro=0', 'root_domain'),
    ('http://www.abclite.cn/Abclite_ADB.conf', 'surge'),
    ('https://raw.githubusercontent.com/BeliefanX/surge/master/surge_rules_09.02.conf', 'surge'),
    ('https://raw.githubusercontent.com/BurpSuite/CloudGate-Surge/master/Surge.Conf', 'surge'),
]

def get_file_name(url):
    return os.path.split(urlparse.urlparse(url).path)[1]

def get_content_from_url(url):
    file_name = get_file_name(url)
    if os.path.exists('/tmp/'+file_name) and False:
        return open('/tmp/'+file_name).read()
    else:
        content = urllib2.urlopen(url).read()
        f = open('/tmp/'+file_name, 'w')
        f.write(content)
        f.close()
        return content
  
def make_domain_group(urls):
    res = set()
    for url, type in urls:
        content = get_content_from_url(url).split('\n')
        for line in content:
            i = line.find('#')
            if i!=-1:
                line = line[0:i]

            line = line.strip()
            if not line:
                continue
            
            if type=='surge':
                if (line.startswith('DOMAIN-SUFFIX,') or line.startswith('- DOMAIN-SUFFIX,')) and line.endswith('REJECT'):
                    domain = line.split(',')[1]
                    if '.' in domain:
                        res.add('.'+domain)
            elif type=='host':
                if line.startswith('127.0.0.1') or line.startswith('0.0.0.0'):
                    domain = line.split()[1]
                    if '.' in domain:
                        res.add(domain)
            elif type=='root_domain':
                domain = line
                if '.' in domain:
                    res.add('.'+domain)

    res = list(res)
    res.sort(key=lambda o: o.split('.')[-2])
    
    with open('amt.txt', 'w') as f:
        for item in res:
            f.write(item+'\n')

if __name__=='__main__':
    make_domain_group(domain_source_urls)

