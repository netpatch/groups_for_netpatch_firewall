## Country ips groups(country_ips/*.txt)

source:

1, ftp://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-extended-latest
2, ftp://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-extended-latest
3, ftp://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest
4, ftp://ftp.apnic.net/public/stats/apnic/delegated-apnic-extended-latest
5, ftp://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-extended-latest

make youself groups:

    python make_country_ips.py
    
<https://firewall.netpatch.co/country_ips/>


## Ad/Malware/Tracking group(amt.txt)

sources:

1, <https://pgl.yoyo.org/as/>
2, <https://adblockplus.org/subscriptions>

make yourself group

    python make_domain_group.py
    
<https://firewall.netpatch.co/files/amt.txt>


## Add domain names or sources

Please create an issue, thanks.


## Download NetPatch Firewall

<https://firewall.netpatch.co/>

