# -*- coding: latin-1 -*-

#
#  IS-105 LAB3
#
#  lab3.py - kildekode som inneholder studentenes løsning.
#         
#
#
import sys
import os
import subprocess
import re

# Gruppe
gruppe = {  'student1': Simon Valvik, \
			'student2': Maiken Flågan, \
            'student3': Daniel Vassdal, \
}

#
#  Oppgave 1

lab3_scripts()

subprocess.call(["../scripts/test1.sh"])
