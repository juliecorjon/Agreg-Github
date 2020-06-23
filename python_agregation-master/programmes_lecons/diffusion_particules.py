"""Diffusion de particules

Description
-----------

Ce programme représente l'évolution de la distribution spatiale de densité de particules lors d'une diffusion 1D. Il est possible de faire varier le temps, le nombre de particules initialement considérées (le problème est conservatif), le coeffcient de diffusion. 

Formules
--------

Informations
------------
Auteurs : Emmanuel Baudin, Arnaud Raoux, François Lévrier, Pierre Cladé et la prépa agreg de Montrouge
Année de création : 2016 
Version : 1.2
Version de Python : 3.7
Licence : Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International

Liste des modifications :
    * v 1.00 : 2016-05-02 Première version complète - baudin@lpa.ens.fr
    * v 1.10 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor
    * v 1.2  : 2019-05-10
"""

import numpy as np
import matplotlib.pyplot as plt

from programmes_lecons import FloatSlider, IntSlider
from programmes_lecons import make_param_widgets, make_choose_plot, make_reset_button
from programmes_lecons import justify



titre = "Diffusion de particules"

description = """Ce programme représente l'évolution de la distribution spatiale de densité de particules lors d'une diffusion 1D. Il est possible de faire varier le temps, le nombre de particules initialement considérées (le problème est conservatif) et le coefficient de diffusion $D$."""

#===========================================================
# --- Variables globales et paramètres ---------------------
#===========================================================

parameters = dict(
    t = FloatSlider(description='Temps (s)', min=0., max=100.0, value=0),
    a = FloatSlider(description='Nb part', min=0.1, max=1000.0, value=500),
    D = FloatSlider(description='Coef. de diffusion -- $D$ (m^2.s^-1)', min=0., max=5.0, value=1),
)

sigma_x0 = 0.1 # Largeur de départ

#===========================================================
# --- Modèle physique --------------------------------------
#===========================================================

#Creation de la fonction diffusion
def maxi(sigma_x0, t, D):
    return np.sqrt(sigma_x0**2 + D*t)
    
def diffusion(t, a, sigma_x0, x, D):
    return a*np.exp(-1/2*(x/maxi(sigma_x0, t, D))**2) / np.sqrt(2*np.pi*maxi(sigma_x0, t, D))


#===========================================================
# --- Réalisation du plot ----------------------------------
#===========================================================

# La fonction plot_data est appelée à chaque modification des paramètres
def plot_data(t, a, D):
    x = np.linspace(-10.0, 10.0, 1001)

    y = diffusion(t, a, sigma_x0, x, D)

    lines['diff'].set_data(x, y)


#===========================================================
# --- Création de la figure et mise en page ----------------
#===========================================================

fig = plt.figure()
fig.suptitle(titre)
fig.text(0.02, .9, justify(description), multialignment='left', verticalalignment='top')

ax = fig.add_axes([0.35, 0.3, 0.6, 0.6])

lines = {}
lines['diff'], = ax.plot([],[], lw=2, color='red')

ax.set_xlabel('Position (m)')
ax.set_ylabel('Densite de particules (#$.m^{-1}$)')

ax.set_xlim(-10, 10)
ax.set_ylim(0, 1500)

param_widgets = make_param_widgets(parameters, plot_data, slider_box=[0.35, 0.07, 0.4, 0.15])
#choose_widget = make_choose_plot(lines, box=[0.015, 0.3, 0.2, 0.15])
reset_button = make_reset_button(param_widgets)


if __name__=="__main__":
    plt.show()

