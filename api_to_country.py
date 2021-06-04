from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import sys
import json


def getCsv(ips, FILENAME, FILEMODE):
    BASE_URL = "http://ip-api.com/json/{}?fields=query,country,city,isp,status"
    with open(FILENAME, FILEMODE) as f:
        for ip in ips:
            ERROR = False
            url = BASE_URL.format(ip)
            try:
                response = urlopen(url).read()
                response = response.decode('utf-8')
                response_json = json.loads(response)

                if response_json.get("status") == "fail":
                    # try with another api
                    getCsv2(ip, f)
                else:
                    # ip = response_json.get('query')
                    country = response_json.get('country')
                    city = response_json.get('city')
                    isp = response_json.get('isp')
                    if isp:
                        isp = isp.replace(',', '')
                    row = f'{ip}, {country}, {city}, {isp}\n'
                    f.write(row)

            except HTTPError as e:
                ERROR = True
                pass
            except URLError as e:
                ERROR = True
                pass

            if ERROR:
                # try with another api
                getCsv2(ip, f)


def getCsv2(ip, f):

    FREE_ROW = '{}, , ,\n'
    BASE_URL = 'https://ipapi.co/{}/json/'

    url = BASE_URL.format(ip)
    try:
        response = urlopen(url).read().decode('utf-8')
        response_json = json.loads(response)

        if response_json.get('error'):
            row = FREE_ROW.format(ip)
        else:
            ip = response_json.get('ip')
            country = response_json.get('country_name')
            city = response_json.get('city')
            isp = response_json.get('org')
            if isp:
                isp = isp.replace(',', '')
            row = f'{ip}, {country}, {city}, {isp}\n'
        f.write(row)

    except HTTPError as e:
        f.write(FREE_ROW.format(ip))
        return
    except URLError as e:
        f.write(FREE_ROW.format(ip))
        return


def parseIPs(fname):

    with open(fname, 'r') as f:
        doc = f.read()

    try:
        doc.index(',')
        doc = doc.replace('\n', '')
        doc = doc.replace(' ', '')
        doc = doc.split(',')
        return doc

    except ValueError as e:
        # no comma 
        try:
            doc.index('\n')
            doc = doc.replace(' ', '')
            doc = doc.split('\n')
            return doc

        except ValueError as e:
            doc = doc.split(' ')
            return doc

def main():
    '''
    Usage: to write new dest.csv file
    python api_to_country.py src.csv dest.csv w+

    If no w given it will write to new file
    '''
    n = len(sys.argv)
    if n < 2:
        print("Please provide src.csv file")
    elif n == 2:
        SRC_FILENAME = sys.argv[1]
        DEST_FILENAME = 'ip_res.csv'
        FILEMODE = 'w+'
    elif n == 3:
        SRC_FILENAME = sys.argv[1]
        DEST_FILENAME = sys.argv[2]
        FILEMODE = 'w+'

    ips = parseIPs(SRC_FILENAME)
    getCsv(ips, DEST_FILENAME, FILEMODE)

if __name__ == "__main__":
    main()
