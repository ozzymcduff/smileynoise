#!/usr/bin/env python
# encoding: utf-8
"""
smileys.py

Created by Oskar Gewalli on 2010-02-15.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
import re

class SmileysValidation:
	def __init__(self):
		self.chars = re.compile(u"^\s*['%sÞ]*\s*$" % re.escape(u'^#&)(*-,/.0398€;:=<>@CBDOPSTX[]\_cbdmoqpuwv}|~!"'),re.UNICODE)
		pass
	def isValid(self,txt):
		return self.chars.match(txt)

class smileysTests(unittest.TestCase):
	def setUp(self):
		self.smileys = u":-) :) :o) :D :] :3 :c) :> =] 8) =) C: :-D :D 8D XD =D =3 <=3 <=8 <=3 <=8 8===D ( o )( o ) :-( :( :c :< :[ D: D8 D; D= DX v.v :-9 ;-) ;) *) ;] ;D :-P :P XP :-p :p =p :-Þ :Þ :-b :b :-O :O O_O o_o 8O OwO O-O 0_o O_o O3O o0o ;o_o; o...o 0w0 :-/ :/ :\ =/ =\ :S :| d:-) qB-) :)~ :-X :X :-# :# O:-) 0:3 O:)  :'( ;*( T_T TT_TT T.T :-* :* >:) >;) B) B-) 8) 8-) ^>.>^ ^<.<^ ^>_>^ ^<_<^ <3 <333 =^_^= =>.>= =<_<= =>.<= \,,/ \m/ \m/\>.</\m/ \o/ \o o/ o/\o :& :u @}-;-'--- 8€ (_!_) ') \"_\"".split(" ")
		self.val = SmileysValidation()
		pass
	def test(self):
		for smiley in self.smileys:
			isValid = self.val.isValid(smiley)
			if not isValid: print smiley
			self.assertTrue(isValid)

if __name__ == '__main__':
	unittest.main()