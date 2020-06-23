r"""Oscillateur amorti

Description
-----------

Ce programme représente la réponse temporelle d'un oscillateur amorti 
générique à un forçage en échelon à l'instant t=0

Informations
------------
Auteurs : Emmanuel Baudin, Arnaud Raoux, François Lévrier, Pierre Cladé et la prépa agreg de Montrouge
Année de création : 2015
Version : 1.2
Version de Python : 3.6
Licence : Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International

Liste des modifications
    * v 0.1 : 2015-10-01 Première version complète
    * v 1.0 : 2016-05-02 
    * v 1.1 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor
    * v 1.2 : 2019-05-10 Simplification du programme
"""

import numpy as np
import matplotlib.pyplot as plt

from programmes_lecons import FloatSlider, IntSlider
from programmes_lecons import make_param_widgets, make_choose_plot, make_reset_button
from programmes_lecons import justify


titre = r"Oscillateur amorti"

description = """Ce programme représente la réponse temporelle d'un oscillateur amorti générique à un forçage en échelon à l'instant t=0. 
"""


#===========================================================
# --- Variables globales et paramètres ---------------------
#===========================================================

parameters = {
    "freq": FloatSlider(description='Fréquence propre -- $f$ (Hz)', min=1, max=30.0, value=5),
    "amp" : FloatSlider(description="Amplitude de l'echelon -- $A$ (V)", min=0.1, max=10.0, value=5),
    "tau" : FloatSlider(description=r"Temps de declin caracteristique -- $\tau$ (s)", min=0.1, max=2.0, value=0.5),
    "phi" : FloatSlider(description='Phase de la réponse -- $\phi$ (rad)', min=-np.pi, max=np.pi, value=0),
}


#===========================================================
# --- Modèle physique --------------------------------------
#===========================================================

# Creation de la fonction à tracer 
def oscillation(t, amp, freq, phi, tau):
    return amp*np.cos(2*np.pi*freq*t+phi)*np.exp(-(t/tau))
# Et on fait aussi les enveloppes
def enveloppe(t, amp, freq, phi, tau):
    return amp*np.exp(-t/tau)


#===========================================================
# --- Réalisation du plot ----------------------------------
#===========================================================

# La fonction plot_data est appelée à chaque modification des paramètres
def plot_data(amp, freq, phi, tau):
    lines['Fonction'].set_data(t, oscillation(t, amp, freq, phi, tau))
    lines['Env. Sup'].set_data(t, enveloppe(t, amp, freq, phi, tau))
    lines['Env. Inf'].set_data(t, -enveloppe(t, amp, freq, phi, tau))


#===========================================================
# --- Création de la figure et mise en page ----------------
#===========================================================

fig = plt.figure()
fig.suptitle(titre)
fig.text(0.02, .9, justify(description), multialignment='left', verticalalignment='top')

ax = fig.add_axes([0.35, 0.3, 0.6, 0.6])

lines = {}
lines['Fonction'], = ax.plot([],[], lw=2, color='red')
lines['Env. Sup'],  = ax.plot([],[], lw=1, ls='--',color='red', visible=False)
lines['Env. Inf'],  = ax.plot([],[], lw=1, ls='--',color='red', visible=False)

ax.set_xlabel('temps (s)')
ax.set_ylabel('Amplitude (V)')

t = np.arange(0.0, 1.0, 0.001)

ax.set_xlim(t.min(), t.max())
ax.set_ylim(-10, 10)

param_widgets = make_param_widgets(parameters, plot_data, slider_box=[0.35, 0.07, 0.4, 0.15])
choose_widget = make_choose_plot(lines, box=[0.015, 0.3, 0.2, 0.15])
reset_button = make_reset_button(param_widgets)


if __name__=="__main__":
    plt.show()

