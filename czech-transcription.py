#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @file		czech-transcription.py
#  @author		Jaxxer <jaxxer@aeternum.cz>
#  
#  @section	LICENSE
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

class Suffixes:
	oneSuffix       = None
	twoToFourSuffix = None
	fiveMoreSuffix  = None
	
	def __init__(self, oneSuffix, twoToFourSuffix,
					fiveMoreSuffix):
		self.oneSuffix       = oneSuffix
		self.twoToFourSuffix = twoToFourSuffix
		self.fiveMoreSuffix  = fiveMoreSuffix



class _AbstractGroup:
	digits = ""
	menForm = True
	
	def __init__(self, digits, menForm=True):
		if type(digits) is str:
			self.digits = self.filterDigits(digits)
		else:
			raise TypeError("Given number is not 'str'.")
		
		self.menForm = menForm
	
	def get(self):
		if not self.digits:
			return u""
		
		baseGroup = BaseGroup(self.digits, self.menForm)
		wordsList = baseGroup.get()
		
		groupSuffixes = self.getGroupSuffixes()
		
		digitsToInt = int(self.digits)
		
		
		if digitsToInt is 1:
			return [groupSuffixes.oneSuffix]
		
		elif 1 < digitsToInt and digitsToInt < 5:
			wordsList.append(groupSuffixes.twoToFourSuffix)
		
		elif digitsToInt >= 5:
			wordsList.append(groupSuffixes.fiveMoreSuffix)
		
		
		return wordsList
	
	def filterDigits(self, digits):
		raise NotImplemented("This method is abstract.")
	
	def getGroupSuffixes(self):
		raise NotImplemented("This method is abstract.")



class BillionGroup(_AbstractGroup):
	def get(self):
		self.menForm = False
		
		return _AbstractGroup.get(self)
	
	def filterDigits(self, digits):
		return digits[-12:-9]
	
	def getWords(self):
		return Suffixes(u"jedna miliarda", u"miliardy", u"miliard")

class MillionGroup(_AbstractGroup):
	def filterDigits(self, digits):
		return digits[-9:-6]
	
	def getWords(self):
		return Suffixes(u"jeden milión", u"milióny", u"miliónů")

class ThousandGroup(_AbstractGroup):
	def filterDigits(self, digits):
		return digits[-6:-3]
	
	def getWords(self):
		return Suffixes(u"jeden tisíc", u"tisíce", u"tisíc")



class BaseGroup(_AbstractGroup):
	def get(self):
		wordsList = []
		
		n = Hundreds(self.digits, self.menForm)
		wordsList.append(n.getWord())
		
		n = Tens(self.digits, self.menForm)
		wordsList.append(n.getWord())
		
		n = Units(self.digits, self.menForm)
		wordsList.append(n.getWord())
		
		return wordsList
	
	def filterDigits(self, digits):
		return digits[-3:]



class _AbstractBase:
	digits = ""
	menForm = True
	
	def __init__(self, digits, menForm=True):
		self.digits = digits
		self.menForm = menForm
	
	def getWord(self):
		index = int(self.getIndex())
		words = self.getWords()
		
		if index < 0:
			return u""
		
		if index < len(words):
			return words[index]
		else:
			raise IndexError("Index must be less then length of words list.")
	
	def getIndex(self):
		raise NotImplemented("This method is abstract.")
	
	def getWords(self):
		raise NotImplemented("This method is abstract.")



class Units(_AbstractBase):
	wordsMenForm = [u"", u"jedna", u"dva", u"tři",
		u"čtyři", u"pět", u"šest", u"sedm", u"osm",
		u"devět"]
	wordsWomenForm = [u"", u"jedna", u"dvě", u"tři",
		u"čtyři", u"pět", u"šest", u"sedm", u"osm",
		u"devět"]
	
	
	def getWords(self):
		return (self.wordsMenForm if self.menForm
					else self.wordsWomenForm)
	
	
	def getIndex(self):
		if not self.digits or (len(self.digits) > 1
					and self.digits[-2] is "1":)
			return -1
		
		return self.digits[-1]



class Tens(_AbstractBase):
	tenToTwenty = [u"deset", u"jedenáct", u"dvanáct",
		u"třináct", u"čtrnáct", u"patnáct",
		u"šestnáct", u"sedmnáct", u"osmnáct",
		u"devatenáct"]
	tens = [u"", u"", u"dvacet", u"třicet", u"čtyřicet",
		u"padesát", u"šedesát", u"sedmdesát",
		u"osmdesát", u"devadesát"]
	
	
	def isLessThenTwenty(self):
		return (len(self.digits) > 1
					and self.digits[-2] is "1":)
	
	
	def getWords(self):
		return (self.tenToTwenty 
					if self.isLessThenTwenty()
					else self.tens)
	
	
	def getIndex(self):
		if len(self.digits) < 2:
			return -1
		
		return (self.digits[-1]
					if self.isLessThenTwenty()
					else self.digits[-2])



class Hundreds(_AbstractBase):
	words = [u"", u"sto", u"dvě stě", u"tři sta",
		u"čtyři sta", u"pět set", u"šest set",
		u"sedm set", u"osm set", u"devět set"]
	
	
	def getWords(self):
		return words
	
	def getIndex(self):
		if len(self.digits) < 3:
			return -1
		
		return self.digits[-3]



def main():
	
	return 0

if __name__ == '__main__':
	main()

