#!/usr/bin/env python
# encoding: utf-8
"""
urlhelper.py

Created by Oskar Mathieu Gewalli on 2010-04-29.
Copyright (c) 2010 Gewalli. All rights reserved.
"""

import sys
import os
import unittest
import urllib

def urlencode(val):
	return force_unicode(urllib.quote_plus(smart_str(val)))
def urldecode(val):
	return force_unicode(urllib.unquote_plus(val.encode("utf-8")))
#django
def force_unicode(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_unicode, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and is_protected_type(s):
        return s
    try:
        if not isinstance(s, basestring,):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                try:
                    s = unicode(str(s), encoding, errors)
                except UnicodeEncodeError:
                    if not isinstance(s, Exception):
                        raise
                    # If we get to here, the caller has passed in an Exception
                    # subclass populated with non-ASCII data without special
                    # handling to display as a string. We need to handle this
                    # without raising a further exception. We do an
                    # approximation to what the Exception's standard str()
                    # output should be.
                    s = ' '.join([force_unicode(arg, encoding, strings_only,
                            errors) for arg in s])
        elif not isinstance(s, unicode):
            # Note: We use .decode() here, instead of unicode(s, encoding,
            # errors), so that if s is a SafeString, it ends up being a
            # SafeUnicode at the end.
            s = s.decode(encoding, errors)
    except UnicodeDecodeError, e:
        raise DjangoUnicodeDecodeError(s, *e.args)
    return s

#django
def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    #if isinstance(s, Promise):
    #    return unicode(s).encode(encoding, errors)
    elif not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s

class urlhelperTests(unittest.TestCase):
	def setUp(self):
		pass
	def test(self):
		print urlencode(u"€")
		print urllib.quote_plus(u"€".encode('utf-8'))
		self.assertEqual(u"€",urldecode(urlencode(u"€")));
	def testOfNonUnicode(self):
		self.assertEqual(u"€",urldecode(urlencode("€")));
	def testOfVal(self):
		self.assertEqual(u":€",urldecode("%3A%E2%82%AC"));
		self.assertEqual(u":€",urldecode(u"%3A%E2%82%AC"));
	def testOfHeadbangingSmiley(self):
		encoded = "%5Cm%2F%5C>.<%2F%5Cm%2F"
		unencoded = "\m/\>.</\m/"
		print unencoded
		self.assertEqual(unencoded,urldecode(encoded));
if __name__ == '__main__':
	unittest.main()