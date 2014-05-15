# -*- coding: latin-1 -*-

#
#  IS-105 LAB11
#  Implementer alt som er markert med OPPGAVE.
#  I tillegg skal du i filen lab11defs.txt beskrive et program (så detaljert du kan)
#	for en poker server, hvor spillere kan melde seg på et poker spill, 
#	få utdelt en hånd hver, legge inn en sats eller kaste sin hånd 
#	og få utpekt en (eller flere i tilfelle uavgjort) vinner.
#	Det er lagt ut flere implementasjoner av sockets klient-tjener modell i Class Fronter.
#	Det som er aktuelt å se på er de som er implementert i Python.
#
#  lab11.py - kildekode som inneholder studentenes løsning.
#         
#
#
import random # brukes for å dele ut kort

# Skriv inn fullt navn på gruppemedlemene (erstatte '-' med navn slikt 'Kari Trå')
gruppe = {  'student1': 'Maiken Flågan', \
			'student2': 'Simon Valvik', \
            'student3': '-', \
}

# Oppgave 
# 	Implementere pokerspill. Vi begynner med representasjon og testing.
#
#	Testing i Python kan gjøres med assert. Eksemplet under skal være selvforklarende.
#
#   Det er gitt et kortstokk http://en.wikipedia.org/wiki/Playing_card med 52 kort.
#	I denne oppgaven prøver vi å lage et prototype som gir svar på følgende:
#	Hvordan representere alle kort? Hvordan finne ut hvilken hånd er best? Hvordan dele ut kort?
#
#   Les deg opp på hva poker er og hvordan det spilles, hvis du ikke kjenner til det fra før.
#	Domenkunnskap i systemutvikling er viktigst!!!
#	http://no.wikipedia.org/wiki/Poker
#	http://en.wikipedia.org/wiki/Poker
#
#	Her er et forslag for representasjon av kort og hender, som jeg anbefaler dere å bruke.
#	Dere kan gjøre egne modifikasjoner, med de må være begrunnet i lab11defs.txt filen.
#
#   Typer (kind): H - heart, S - spade, C - club, D - diamond (13 kort av hver type)
#   Verdi (rank): A - ace, K - king, Q - queen, J - jack, T - ten, 9, 8, 7, 6, 5, 4, 3, 2
#   En hånd (hand): består av 5 kort http://en.wikipedia.org/wiki/Hand_rankings
#   Hånd rangeres fra høyest til lavest (i paranteser anbefalt navn på variabelen på en hånd): 
#		 8 - Straight flush (sf) (finnes også Royal Flush, som er den beste av Straight flush)
#		 7 - Four of a Kind (fk) 
#		 6 - Full House (fh) 
#	     5 - Flush (fl)
#		 4 - Straight (st) 
#		 3 - Three of a kind (tk) 
#	     2 - Two Pair (tp) 
#        1 - One Pair (op) 
#        0 - High Card (hc)
#   
#
# OPPGAVE: erstatt max med en funksjon allmax, som tar hensyn til uavgjort mellom to eller flere hender 
def poker(hands):
	"""
		Denne funksjonene må omdefineres for å ta hensyn til spesialtilfelle med flere like "Straight Flush" hender
		dvs. uavgjort
		Returnerer en eller flere hender: poker([hand, ...]) => [[hand], ...]
		hand_rank er en funksjon som må skrives og brukes i sammenligningen av "hender"
	"""
	return allmax(hands, key=hand_rank)

# OPPGAVE: Implementer denne funksjonen (brukes i poker funksjonen for å løse uavgjort tilfeller)
# For eksempel, gitt 4 følgende hender
#   [['6C', '7C', '8C', '9C', 'TC'],
#   ['6D', '7D', '8D', '9D', 'TD'],
#   ['9D', '9H', '9S', '9C', '7D'],
#   ['TD', 'TC', 'TH', '7C', '7D']]
# skal allmax returnere to hender [['6C', '7C', '8C', '9C', 'TC'], ['6D', '7D', '8D', '9D', 'TD']]
def allmax(iterable, key = lambda x:x):
    "returnerer en liste over alt som er max."
    maxvalue = None
    maxitems = []
    for item in iterable:
        keyvalue = key(item)
        if maxvalue is None or keyvalue > maxvalue:
            maxvalue = keyvalue
            maxitems = [item]
        elif keyvalue == maxvalue:
            maxitems.append(item)
    return maxitems	

# OPPGAVE: fullføre denne funksjonene for alle hender i poker og lage tester med assert
def hand_rank(hand):
    "Returnerer hvor høy ranken til hånda er."
    groups = group(['--23456789TJQKA'.index(r) for r, s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks)-min(ranks) == 4
    flush = len(set([s for r, s in hand])) == 1
    return (
        9 if (5, ) == counts else
        8 if straight and flush else
        7 if (4, 1) == counts else
        6 if (3, 2) == counts else
        5 if flush else
        4 if straight else
        3 if (3, 1, 1) == counts else
        2 if (2, 2, 1) == counts else
        1 if (2, 1, 1, 1) == counts else
        0), ranks
	
# Funksjonene card_ranks(hand) returnerer en ORDNET (sorted) tuple av verdier (ranks)
# Verdier for J, Q, K og A er tilsvarende 11, 12, 13, 14. 
# En hånd TD TC TH 7C 7D skal returnere [10,10,10,7,7]
def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    # ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    # ranks = [{'A':14,
    #           'K':13,
    #           'Q':12,
    #           'J':11,
    #           'T':10,
    #           }.get(r,r) for r, s in hand]
    ranks = [14 if r == 'A' else
             13 if r == 'K' else
             12 if r == 'Q' else
             11 if r == 'J' else
             10 if r == 'T' else
             int(r)
             for r, s in hand]
    ranks.sort(reverse = True)
    if ranks == [14, 5, 4, 3, 2]:
        ranks = [5, 4, 3, 2, 1]
    return ranks

# OPPGAVE: Implementer denne funksjonen
# Funksjonen straight(ranks) returner True hvis hånden er en Straight.
def straight(ranks):
	return sum(ranks) - min(ranks)*5 == 10

# OPPGAVE: Implementere denne funksjonen
# Funksjonen flush(hand) returnerer True hvis hånden er en Flush.
def flush(hand):
    flushand = [s for r, s in hand]
    return len(set(flushand)) == 1


# OPPGAVE: Implementer denne funksjonen
# Funksjonen kind(nr, ranks) returnerer den første verdien (rank) som hånden har nøyaktig n av.
# For en hånd med 4 syvere, skal denne funksjonen returnere 7.
def kind(n, ranks):
    """Returnerer det første cardet som har (n)r of.
    returnerer ingenting hvor det ikke er noe n card."""
    for r in set(ranks):
        if ranks.count(r) == n:
            return r

# OPPGAVE: Implementer denne funksjonen
# Funksjonen two_pair(ranks) gjør følgende:
# hvis det er Two Pair, skal funksjonen returnere deres verdi (rank) som en tuple.
# For eksempel, en hånd med to toere og 2 firere vil gi en returverdi på (4, 2).
def two_pair(ranks):
    """Returnerer to par som en tuple, men hvis der ikke er noe par, return none."""
    result = [r for r in set(ranks) if ranks.count(r) == 2]
    if len(result) == 2:
        return (max(result), min(result))

# Denne strukturen definerer et kortstokk for poker
mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']

# Denne funksjonen deler ut numhands med n kort i hver hånd
def deal(numhands, n=5, deck=mydeck):
    # Your code here.
	random.shuffle(deck)
	return [deck[n*i:n*(i+1)] for i in range(numhands)]


def test():
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    s1 = "AS 2S 3S 4S 5C".split() # A-5 straight
    s2 = "2C 3C 4C 5S 6S".split() # 2-6 straight
    s3 = "TC JC QC KS AS".split() # 10-A straight
    tp = "5S 5D 9H 9C 6S".split() # two pair
    ah = "AS 2S 3S 4S 6C".split() # A high
    sh = "2S 3S 4S 6C 7D".split() # 7 high
   
	# Dette ble gjort i LAB 5
	# Den innebygde (built-in) funksjonen max kan brukes for å finne den beste hånden
	# Skriv test for den innebygde funksjonen max på flere "list of numbers" (lon)
	# Eksemplene er gitt, du må kommentere disse ut og sette på en verdi som ikke gir feil
    #lon1 = [6, 7, 8, 0]
    #lon2 = [6, 7, -9, 0]
    #assert max(lon1) == 8
    #assert max(lon2, key=abs) == 9
	# Disse testtilfellene ble skrevet i LAB 5
	# Skriv tre nye testtilfeller som sammenligner hender basert på eksemplet overfor
	# 1) Four of Kind (fk) mot Full House (fh) skal returnere Four of Kind (fk)
	# 2) Full House (fh) mot Full House (fh) skal returnere Full House (fh)
	# 3) Straight (st) skal slå Two pair (tp) OBS! Du må selv lage eksempler på hender her
	

	
	# Dette ble gjort i LAB 5
	# 1) teste et tilfelle der det kun er en hånd og at poker returnerer den samme hånden
	# 2) teste et tilfelle hvor man sammenligner en Straight Flush med 100 Full Houses
	# og det må da returnere Straight Flush (urealistisk med så mange spillere, men 
	# vi tar høyde for det).
	# Hva skjer hvis man har en tom liste som inn-data, dvs. ingen hender?
	#assert poker([sf]) = sf
    #assert poker([sf, 100*fh]) = sf

	# Dette ble gjort i LAB 5
	# Implementer funksjonen card_rank(hand) og legg til tester for 
	# sf, fk og fh variabler som er definert i denne testfunksjonen
	# Du kan gjerne definere flere hender og legge til flere tester :)
    #assert card_rank(sf) = [10,9,8,7,6]
    #assert card_rank(fk) = [9,9,9,9,7]

    # 
    # hand_rank(..) implementere i denne laben (LAB 11)
	# Her er gitt noen eksempler på testing av denne funksjonen som man kan bruke på et senere tidspunkt
    #
    assert card_ranks(fk) == [9, 9, 9, 9, 7]
    assert card_ranks(fh) == [10, 10, 10, 7, 7]
    assert card_ranks(['AC', '3D', '4S', 'KH']) == [14, 13, 4, 3]
    return "Done testing"

print test()


