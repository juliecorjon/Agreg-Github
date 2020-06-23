r"""Écoulement de Poiseuille

Description
-----------
Ce programme représente le champ de vitesse dans un écoulement de Poiseuille (tube)


Informations
------------
Auteurs : Arnaud Raoux, Emmanuel Baudin, François Lévrier, Pierre Cladé et la prépa agreg de Montrouge
Année de création : 2016 
Version : 1.2
Version de Python : 3.6
Licence : Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International

Liste des modifications :
    * v 1.00 : 2016-03-01 Première version complète
    * v 1.10 : 2016-05-02 Mise à jour de la mise en page
    * v 1.2 : 
"""

import matplotlib.pyplot as plt
import numpy as np

import programmes_lecons


titre = "Écoulement de Poiseuille"

description = """Ce programme représente le champ de vitesse dans un écoulement de Poiseuille (tube)"""

#Definition d'un maillage du plan dans lequel a lieu l'ecoulement
Y, X = np.mgrid[-1:1:25j, 0:3:6j]

#Calcul du champ de vitesse
U = 4*(1-(Y**2))
V = 0

#Epaisseur des vecteurs vitesse
widths = np.linspace(0, 2, X.size)

# Creation de la figure
fig = plt.figure()
fig.suptitle(titre)

ax = fig.subplots(1, 1)

#Creation des vecteurs vitesse
ax.quiver(X, Y, U, V, 
           color='Teal', 
           scale=25,
           headlength=10)

#Definition des axes
ax.set_xlim(0, 3)
ax.set_ylim(-1.5, 1.5)

#Repere des limites superieure et inferieure de l'ecoulement
ax.axhline(1, color='k')
ax.axhline(-1, color='k')

#Nom des axes
ax.set_xlabel('Position X (m)')
ax.set_ylabel('Position Z (m)')

if __name__=="__main__":
    plt.show(fig) # On provoque l'affichage a l'ecran
