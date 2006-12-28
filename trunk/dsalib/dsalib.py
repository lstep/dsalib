# -*- coding: latin-1 -*-
"""
Copyright (C) 2006 Adelux <contact@adelux.fr>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

TODO: Pour la recuperation des DSA, faire une recuperation
de ce qui est - vieux que X mois, pour ne pas etre coince
si l'on est au debut de l'anee.
"""
import urllib,datetime,re,time,shelve,os
from xml.dom.minidom import parse, parseString

def memoize(function):
        return MemoizeDisk(function)

class MemoizeDisk(object):
    def __init__(self, fn):
        self.fn=fn
        self.cache = shelve.open(os.path.expanduser('~/.checkdsa-cache'))

    def __get__(self, instance, cls=None):
        self.instance = instance
        return self

    def __call__(self,*args):
        # To be generic, make it a string, not a tuple
        mykey = reduce(lambda x, y: str(x)+str(y), args)

        if self.cache.has_key(mykey):
            return self.cache[mykey]
        else:
            object = self.cache[mykey] = self.fn(self.instance, *args)
            self.cache.sync()
            return object

# From Paul Moore's Python Cookbook recipe 52201
class Memoize(object):
    def __init__(self, fn):
        self.cache={}
        self.fn=fn

    def __get__(self, instance, cls=None):
        self.instance = instance
        return self

    def __call__(self,*args):
        if self.cache.has_key(args):
            return self.cache[args]
        else:
            object = self.cache[args] = self.fn(self.instance, *args)
            return object

class DSABase:
    def __init__(self, architecture=None):
        print "Using version 1.01"
        self.dsa_advisories = {}
        self.architecture = architecture or 'Intel IA-32'
        self.proxies = None

    def update_base(self, year=None, proxies=None):
        """
        Returns the number of items found
        """
        self.year = year or time.localtime()[0]
        self.link =  'http://www.debian.org/security/%d/' % self.year
        self.proxies = proxies
        expr = re.compile('<tt>\[(?P<date>.*?)\]</tt> <strong><a href="./(?P<id>.*?)">(?P<id2>.*?) (?P<name>.*?)</a></strong> - (?P<desc>.*?) <br>')

        data = urllib.urlopen(self.link + 'index.html', proxies=self.proxies).read()
        for m in expr.finditer(data):
            item = m.group('id')
            self.dsa_advisories[item] = {}
            self.dsa_advisories[item]['date'] = m.group('date')
            self.dsa_advisories[item]['desc'] = m.group('desc')
            self.dsa_advisories[item]['name'] = m.group('name')
            self.dsa_advisories[item].update(self.get_dsa_details(item))

        return len(self.dsa_advisories)


    @memoize
    def get_dsa_details(self, ident):
        print "Getting", self.link + ident
        packages = []
        regexpDebianBug = re.compile(r'<a href=".*?">Bug (\d+)</a>')
        regexpCANCVEBug =  re.compile(r'<a href=".*?">(CVE-\d{4}-\d+)</a>')
        regexpBugtraqBug =  re.compile(r'<a href=".*?">BugTraq ID (\d+)</a>')
        regexpAffectedPackages1 = re.compile(r'Debian GNU/Linux.*?<dt>%s:(.*?)(<dt>|</dl>)' % self.architecture, re.M+re.S)
        regexpAffectedPackages1a= re.compile(r'Debian GNU/Linux.*?<dt>Architecture-independent component:(.*?)(<dt>|</dl>)', re.M+re.S)
        regexpAffectedPackages2 = re.compile(r'<dd><a href="[^"]*/(.*?)_[0-9a-z]+.deb">.*?</a><br>')

        data = urllib.urlopen(self.link + ident, self.proxies).read()

        debianReferences = regexpDebianBug.findall(data)
        CVEReferences = list(set(regexpCANCVEBug.findall(data)))  # Remove duplicates
        bugtraqReferences = regexpBugtraqBug.findall(data)

        result = regexpAffectedPackages1.search(data)
        if result:
            d = result.group(1)
            packages += regexpAffectedPackages2.findall(d)

        # Get the Architecture independent packages too!
        result = regexpAffectedPackages1a.search(data)
        if result:
            d = result.group(1)
            packages += regexpAffectedPackages2.findall(d)

        return {'debianReferences':debianReferences,
                'CVEReferences':CVEReferences,
                'bugtraqReferences':bugtraqReferences,
                'fixedIn':packages }

if __name__ == '__main__':
    dsaBase = DSABase()
    dsaBase.update_base()

    for e in dsaBase.dsa_advisories.items():
        print e
        print
