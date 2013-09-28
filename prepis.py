#!/usr/bin/env python
# -*- coding: utf-8 -*-

class _AbstractGroup:
	digits = ""
	
	def __init__(self, number):
		if type(number) is str:
			self.digits = self.filterDigits(number)
		else:
			raise TypeError("Given number is not 'str'.")
	
	def get(self):
		base = BaseGroup(self.digits)
		transcriptList = base.get()
		
		if not self.digits:
			return u""
		
		words = self.getWords()
		
		digitsToInt = int(self.digits)
		
		if digitsToInt is 1:
			return [words[0]]
		elif 1 < digitsToInt and digitsToInt < 5:
			transcriptList.append(words[1])
		elif digitsToInt >= 5:
			transcriptList.append(words[2])
		
		return transcriptList
	
	def filterDigits(self, number):
		raise NotImplemented("This method is abstract.")
	
	def getWords(self):
		raise NotImplemented("This method is abstract.")

class BillionGroup(_AbstractGroup):
	def get(self):
		if self.digits is "2":
			words = self.getWords()
			
			return [u"dvě", words[1]]
		
		return _AbstractGroup.get(self)
	
	def filterDigits(self, number):
		return number[-12:-9]
	
	def getWords(self):
		return (u"jedna miliarda", u"miliardy", u"miliard")

class MillionGroup(_AbstractGroup):
	def filterDigits(self, number):
		return number[-9:-6]
	
	def getWords(self):
		return (u"jeden milión", u"milióny", u"miliónů")

class ThousandGroup(_AbstractGroup):
	def filterDigits(self, number):
		return number[-6:-3]
	
	def getWords(self):
		return (u"jeden tisíc", u"tisíce", u"tisíc")

class BaseGroup(_AbstractGroup):
	def get(self):
		transcriptList = []
		
		n = Hundreds(self.digits)
		transcriptList.append(n.get())
		
		n = Tens(self.digits)
		transcriptList.append(n.get())
		
		n = Units(self.digits)
		transcriptList.append(n.get())
		
		return transcriptList
	
	def filterDigits(self, number):
		return number[-3:]

class Units:
	digits = ""
	words = [u"", u"jedna", u"dva", u"tři", u"čtyři",
		u"pět", u"šest", u"sedm", u"osm", u"devět"]
	
	def __init__(self, digits):
		self.digits = digits
	
	def get(self):
		if not self.digits:
			return u""
		
		if len(self.digits) > 1 and self.digits[-2] is "1":
			return u""
		
		baseDigit = self.digits[-1]
		baseDigitToInt = int(baseDigit)
		
		return self.words[baseDigitToInt]

class Tens:
	digits = ""
	
	tenToTwenty = [u"deset", u"jedenáct", u"dvanáct",
		u"třináct", u"čtrnáct", u"patnáct",
		u"šestnáct", u"sedmnáct", u"osmnáct",
		u"devatenáct"]
	tens = [u"", u"", u"dvacet", u"třicet", u"čtyřicet",
		u"padesát", u"šedesát", u"sedmdesát",
		u"osmdesát", u"devadesát"]
	
	def __init__(self, digits):
		self.digits = digits
	
	def get(self):
		if len(self.digits) < 2:
			return u""
		
		if self.digits[-2] is "1":
			baseDigit = self.digits[-1]
			baseDigitToInt = int(baseDigit)
			
			return self.tenToTwenty[baseDigitToInt]
		
		else:
			tenDigit = self.digits[-2]
			tenDigitToInt = int(tenDigit)
			
			return self.tens[tenDigitToInt]

class Hundreds:
	digits = ""
	words = [u"", u"sto", u"dvě stě", u"tři sta",
		u"čtyři sta", u"pět set", u"šest set",
		u"sedm set", u"osm set", u"devět set"]
	
	def __init__(self, digits):
		self.digits = digits
	
	def get(self):
		if len(self.digits) < 3:
			return u""
		
		hundredDigit = self.digits[-3]
		hundredDigitToInt = int(hundredDigit)
		
		return self.words[hundredDigitToInt]

class DecimalGroup(_AbstractGroup):
	words = [(u"jedna desetina", u"desetiny", u"desetin"),
		(u"jedna setina", u"setiny", u"setin"),
		(u"jedna tisícina", u"tisíciny", u"tisícin")]
	
	def get(self):
		if self.digits and int(self.digits) is 2:
			words = self.getWords()
			
			return [u"dvě", words[1]]
		
		return _AbstractGroup.get(self)
	
	def filterDigits(self, number):
		return number[-3:]
	
	def getWords(self):
		return self.words[len(self.digits) - 1]

class NumberTranscription:
	digits = ""
	
	words = (u"celá", u"celé", u"celých")
	
	def __init__(self, digits):
		if type(digits) is float:
			digits = round(digits, 3)
		
		if type(digits) is not str:
			digits = str(digits)
		
		self.digits = digits
	
	def transcript(self):
		digits = self.digits
		decimals = ""
		
		numberParts = digits.split(".", 1)
		
		if len(numberParts) > 1:
			digits = numberParts[0]
			decimals = numberParts[1]
		
		integerPart = self.transcriptIntegerPart(digits)
		decimalPart = self.transcriptDecimalPart(decimals)
		
		integerPartPostfix = u""
		
		if decimalPart:
			digitsToInt = int(digits)
			
			if digitsToInt is 1:
				integerPartPostfix = self.words[0]
			elif 1 < digitsToInt and digitsToInt < 5:
				integerPartPostfix = self.words[1]
			else:
				integerPartPostfix = self.words[2]
		
		return [integerPart, integerPartPostfix, decimalPart]
	
	def transcriptIntegerPart(self, digits):
		transcriptList = []
		
		if digits is "0":
			return u"nula"
		
		if digits[0] is "-":
			transcriptList.extend([u"mínus"])
			digits = digits[1:]
		
		n = BillionGroup(digits)
		transcriptList.extend(n.get())
		
		n = MillionGroup(digits)
		transcriptList.extend(n.get())
		
		n = ThousandGroup(digits)
		transcriptList.extend(n.get())
		
		n = BaseGroup(digits)
		transcriptList.extend(n.get())
		
		return self.transcriptListToStr(transcriptList)
	
	def transcriptDecimalPart(self, decimals):
		transcriptList = []
		
		n = DecimalGroup(decimals)
		decimalsTranscript = n.get()
		
		transcriptList.extend(n.get())
		
		return self.transcriptListToStr(transcriptList)
	
	def transcriptListToStr(self, transcriptList):
		transcriptList = filter(len, transcriptList)
		
		return u" ".join(transcriptList)


class CrownTranscription(NumberTranscription):
	words = (u"koruna", u"koruny", u"korun")
	
	def transcript(self):
		digits = self.digits
		decimals = ""
		
		numberParts = digits.split(".", 1)
		
		if len(numberParts) > 1:
			digits = numberParts[0]
			decimals = numberParts[1]
		
		integerPart = self.transcriptIntegerPart(digits)
		decimalPart = self.transcriptDecimalPart(decimals)
		
		integerPartPostfix = u""
		
		digitsToInt = int(digits)
		
		if digitsToInt is 1:
			integerPartPostfix = self.words[0]
		elif 1 < digitsToInt and digitsToInt < 5:
			integerPartPostfix = self.words[1]
		else:
			integerPartPostfix = self.words[2]
		
		return [integerPart, integerPartPostfix, decimalPart]
	
	def transcriptDecimalPart(self, decimals):
		transcriptList = []
		
		n = CentsGroup(decimals)
		decimalsTranscript = n.get()
		
		transcriptList.extend(n.get())
		
		return self.transcriptListToStr(transcriptList)

class CentsGroup(DecimalGroup):
	words = (u"haléř", u"haléře", u"haléřů")
	
	def getWords(self):
		return self.words


if __name__ == "__main__":
	#a = NumberToWords(u"287 502,- Kč")
	#print a.filterDigits()
	
	
	
	for i in [3, 1307.69]:
		#n = NumberTranscription(i)
		n = CrownTranscription(i)
		transcription = n.transcriptListToStr(n.transcript())
		
		print "%f - %s" % (i, transcription)
	
	#for w in testOutput:
		#print type(w)
		#if w:
			#print w
