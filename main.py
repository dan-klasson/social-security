
from BeautifulSoup import BeautifulStoneSoup 
import urllib
import urllib2
import re
from datetime import date

"""
Checks if numbers are luhn valid
"""
def is_luhn_valid(check):
    num = [int(x) for x in str(check)]
    return sum(num[::-2] + [sum(divmod(d * 2, 10)) for d in num[-2::-2]]) % 10 == 0

"""
Gets the oldest Personnummer in the dictionary
"""
def get_oldest_pn(result):
    a = dict(map(lambda item: (item[1],item[0]),result.items()))
    return a[max(a.keys())]

request_url = ""
submit_url = ""
email = ""

# Fetch the data from the feed and parse it with BeautifulSoup
request = urllib2.Request(request_url)
response = urllib2.urlopen(request)
soup = BeautifulStoneSoup(response.read())

result = {}

# Find all data that is within the entry tag
for row in soup.findAll('entry'):

    # Find all data that is in a Personnummer format: XXXXXX-XXXX
    for personnummer in re.findall(r'\d{6}-\d{4}', str(row)):

        # Personummer as a string (without the minus symbol)
        pn = personnummer.replace('-', '')

        # Only valid luhn Personnummer are allowed
        if is_luhn_valid(pn):

            # Get the age in days of people at a specific date
            date1 = date(2008, 12, 31)
            date2 = date(int("19" + pn[0:2]), int(pn[2:4]), int(pn[4:6]))
            delta = date1 - date2

            # And record the people who's date of birth is divisible by 7
            if delta.days % 7 == 0:
                result[personnummer] = delta.days

# Find the oldest person in the result dictionary
oldest_pn = get_oldest_pn(result)

values = {
    'match': oldest_pn,
    'email': email,
}

# Return the calculated value 
data = urllib.urlencode(values)
req = urllib2.Request(submit_url, data)
response = urllib2.urlopen(req)

print response.read()  

