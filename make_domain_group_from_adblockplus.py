import os, urlparse, urllib2, math, urllib, re

adblockplus_urls = [
    'https://easylist-downloads.adblockplus.org/easylist.txt',
    'https://easylist-downloads.adblockplus.org/easylistgermany.txt',
    'https://easylist-downloads.adblockplus.org/fanboy-social.txt',
    'https://easylist-downloads.adblockplus.org/easyprivacy.txt',
    'https://easylist-downloads.adblockplus.org/fanboy-annoyance.txt',
    'https://secure.fanboy.co.nz/r/fanboy-complete.txt',
    'https://secure.fanboy.co.nz/r/fanboy-ultimate.txt',
    'https://raw.githubusercontent.com/Hubird-au/Adversity/master/Adversity.txt', 
    'https://raw.githubusercontent.com/Hubird-au/Adversity/master/Antisocial.txt',
]

def get_file_name(url):
    return os.path.split(urlparse.urlparse(url).path)[1]

def get_content_from_url(url):
    file_name = get_file_name(url)
    if os.path.exists('/tmp/'+file_name) and False:
        return open('/tmp/'+file_name).read()
    else:
        req = urllib2.Request(url, headers={'User-Agent': 'Wget/1.16'})
        content = urllib2.urlopen(req).read()
        f = open('/tmp/'+file_name, 'w')
        f.write(content)
        f.close()
        return content

def get_all_contents(urls):
    content = ''
    for url in urls:
        content += get_content_from_url(url)+'\n'

    return content

def make_domain_group(urls):
    pass_re = re.compile('[\$\%\*=|\#&@\/\?\+,;:]')
    ip_pattern = re.compile(r"^(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|2[0-4]\d|25[0-5])$")

    res = set()
    content = get_all_contents(urls).split('\n')
    for line in content:
        line = line.strip()
        if not line:
            continue

        if line.startswith('||') and not pass_re.search(line[2:]): 
            line = line[2:]
            if line[-1] in ('.', '-', '_'):
                continue
            line = line[:-1]
            if line[-1] in ('.', '-', '_'):
                continue

            if ip_pattern.match(line):
                continue
            
            if '.' in line:
               res.add('.'+line)

    res = list(res)
    res.sort(key=lambda o: o.split('.')[-2])

    with open('amt2.txt', 'w') as f:
        for item in res:
            f.write(item+'\n')

if __name__=='__main__':
    make_domain_group(adblockplus_urls)

