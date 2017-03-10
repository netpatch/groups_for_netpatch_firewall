import os.path, re, urlparse, urllib2

domain_source_urls = [
    ('https://pgl.yoyo.org/as/serverlist.php?hostformat=nohtml&showintro=0', 'root_domain'),

    ('https://easylist-downloads.adblockplus.org/easylist.txt', 'adblock'),
    ('https://raw.githubusercontent.com/ABPindo/indonesianadblockrules/master/subscriptions/abpindo.txt', 'adblock'),
    ('http://stanev.org/abp/adblock_bg.txt', 'adblock'),
    ('https://easylist-downloads.adblockplus.org/easylistchina.txt', 'adblock'),
    ('https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt', 'adblock'),
    ('https://raw.github.com/tomasko126/easylistczechandslovak/master/filters.txt', 'adblock'),
    ('https://easylist-downloads.adblockplus.org/easylistdutch.txt', 'adblock'),
    ('https://easylist-downloads.adblockplus.org/easylistgermany.txt', 'adblock'),
    ('https://raw.githubusercontent.com/easylist/EasyListHebrew/master/EasyListHebrew.txt', 'adblock'),
    ('https://easylist-downloads.adblockplus.org/easylistitaly.txt', 'adblock'),
    ('http://margevicius.lt/easylistlithuania.txt', 'adblock'),
    ('https://easylist-downloads.adblockplus.org/easylistspanish.txt', 'adblock'),
    ('https://notabug.org/latvian-list/adblock-latvian/raw/master/lists/latvian-list.txt', 'adblock'),
    ('https://easylist-downloads.adblockplus.org/Liste_AR.txt', 'adblock'),
    ('https://easylist-downloads.adblockplus.org/liste_fr.txt', 'adblock'),
    ('http://www.zoso.ro/pages/rolist.txt', 'adblock'),
    ('https://easylist-downloads.adblockplus.org/advblock.txt', 'adblock'),

    ('https://easylist-downloads.adblockplus.org/easyprivacy.txt', 'adblock'),
    ('https://adblock.gardar.net/is.abp.txt', 'adblock'),
    ('http://www.void.gr/kargig/void-gr-filters.txt', 'adblock'),
    ('http://bit.ly/11QrCfx', 'adblock'),
    ('https://raw.githubusercontent.com/zpacman/Blockzilla/master/Blockzilla.txt', 'adblock'),
    ('http://adblock.dajbych.net/adblock.txt', 'adblock'),
    ('http://adblock.ee/list.php', 'adblock'),
    ('http://gurud.ee/ab.txt', 'adblock'),
    ('http://abp.mozilla-hispano.org/nauscopio/filtros.txt', 'adblock'),
    ('https://raw.githubusercontent.com/szpeter80/hufilter/master/hufilter.txt', 'adblock'),
    ('https://adblock.dk/block.csv', 'adblock'),
    ('http://noads.it/filtri.txt', 'adblock'),
    ('https://raw.githubusercontent.com/yous/YousList/master/youslist.txt', 'adblock'),

    ('https://easylist-downloads.adblockplus.org/antiadblockfilters.txt', 'adblock'),
    ('https://easylist-downloads.adblockplus.org/adwarefilters.txt', 'adblock'),
    ('https://easylist-downloads.adblockplus.org/fanboy-annoyance.txt', 'adblock'),
    ('https://easylist-downloads.adblockplus.org/fanboy-social.txt', 'adblock'),
    ('http://www.kiboke-studio.hr/i-dont-care-about-cookies/abp/', 'adblock'),
    ('https://easylist-downloads.adblockplus.org/malwaredomains_full.txt', 'adblock'),
    ('https://raw.github.com/liamja/Prebake/master/obtrusive.txt', 'adblock'),
    ('https://raw.githubusercontent.com/Dawsey21/Lists/master/adblock-list.txt', 'adblock'),

]

def get_file_name(url):
    return os.path.split(urlparse.urlparse(url).path)[1]

def get_content_from_url(url, key):
    file_name = 'nf_'+get_file_name(url)+key
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

whitelist_domains = set([])

def make_domain_group(urls):
    pass_re = re.compile('[\$\%\*=|\#&@\/\?\+,;:]')
    ip_pattern = re.compile(r"^(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|2[0-4]\d|25[0-5])$")

    res = set()
    url_index = 0
    for url, type in urls:
        url_index += 1
        try:
            content = get_content_from_url(url, str(url_index)).split('\n')
        except:
            print 'get_content_from_url error: ', type, url
            raise

        for line in content:
            if type!='adblock':
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
            elif type=='adblock':
                if line.startswith('||') and not pass_re.search(line[2:]): 
                    line = line[2:]
                    if line[-1] in ('.', '-', '_'):
                        continue
                    line = line[:-1]
                    if line[-1] in ('.', '-', '_'):
                        continue

                    if ip_pattern.match(line):
                        continue

                    domain = line
                    if '.' in domain:
                        res.add('.'+domain)
    
    res = res - whitelist_domains
    res = list(res)

    def sort_fun(o):
        x = o.split('.')
        if x[-2] in ('com', 'co') and len(x)>=3:
            return x[-3]
        else:
            return x[-2]

    res.sort(key=sort_fun)
    
    with open('amt.txt', 'w') as f:
        for item in res:
            f.write(item+'\n')

if __name__=='__main__':
    make_domain_group(domain_source_urls)

