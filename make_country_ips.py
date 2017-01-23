import os, urlparse, urllib2, math, urllib

all_nic_urls = [
'ftp://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-extended-latest',
'ftp://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-extended-latest',
'ftp://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest',
'ftp://ftp.apnic.net/public/stats/apnic/delegated-apnic-extended-latest',
'ftp://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-extended-latest']

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
  
def get_all_contents(urls):
    content = ''
    for url in urls:
        content += get_content_from_url(url)+'\n'

    return content

def get_all_country_codes():
    res = {}
    for line in open('country_code.txt'):
        line = line.strip()
        code = line[-2:]
        name = line[:-3].strip('"')
        res[code] = name
    return res

def make_all_country_ips(urls):
    country_codes = get_all_country_codes()
    content = get_all_contents(urls)

    res = {}
    
    content = content.split('\n')
    for line in content:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        cc = line.split('|')
        if cc[-1]=='summary':
            continue

        if cc[2].lower()=='ipv4':
            if cc[6].lower()=='reserved':
                continue
            code = cc[1].upper()
            if not code or code=='ZZ':
                continue

            ip = cc[3]
            cidr = int(32-math.log(int(cc[4]))/math.log(2))
            status = cc[6]
            host_num = 2**(32-cidr)

            o = ip.split('.')
            num = int(o[0])*256**3+int(o[1])*256**2+int(o[2])*256+int(o[3])

            ll = res.setdefault(code, [])
            ll.append((ip, cidr, num, host_num))

        elif cc[2].lower()=='ipv6':
            pass
        elif cc[2].lower()=='asn':
            pass
        else:
            pass
    
    host_num_dict = {}
    for code in res:
        res[code].sort(key=lambda o: o[2])
        f = open('country_ips/'+code+'.txt', 'w')
        host_num_dict[code] = 0
        for ip, cidr, _, host_num in res[code]:
            f.write(ip+'/'+str(cidr)+'\n')
            host_num_dict[code] += host_num
        f.close()
    
    list_file = open('country_ips/summary.txt', 'w')
    for code in sorted(res.keys(), key=lambda o: host_num_dict.get(o, 0), reverse=True):
        list_file.write(country_codes[code]+'|'+code+'|'+str(len(res[code]))+'|'+str(host_num_dict.get(code, 0))+'\n')
    list_file.close()

if __name__=='__main__':
    make_all_country_ips(all_nic_urls)

