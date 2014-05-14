#
# -*- coding: latin-1 -*-
#
import sys

# Skriv inn fullt navn på gruppemedlemene (erstatte '-' med navn #slikt 'Kari Trå')
#gruppe = {  'student1': 'Simon', \
#			'student2': 'Maiken', \
#           'student3': 'Daniel', \


#Oppgave 1

#       \/_
#  \,   /( ,/
#   \\\' ///
#    \_ /_/
#    (./
#     '` 

def ascii_fugl():
	print """
       
	\/_
  \,   /( ,/
   \\\\\\' ///
    \_ /_/
    (./
     '` 
"""

	return

ascii_fugl()

#Oppgave 2

def bitAnd(x, y):
	return x&y
print bitAnd (5,6)


#  Oppgave 4

def bitXor(x, y):
	return x^y
print bitXor (4,5)

# Oppgave 5

def bitOr(x, y):
	return x|y
print bitOr (0, 1)

#Oppgave 6

#Ascii-verdien til A
print ord ('A')
print '{0:08b}'.format(65)

#Selve oppgaven
def ascii8Bin(bokstav):
	return '{0:08b}'.format(ord (bokstav))
print ascii8Bin('A')

#  Oppgave 7

def transferBin(tekst):
	liste = list(tekst)
# list = navn - Tekst = Argument
	for bokstav in liste:
		print ascii8Bin(bokstav)

transferBin ("Hei")

