r""" Effet tunnel

Description
-----------
Ce programme permet de calculer la transmission d'une barrière de potentiel pour 
une onde de matière incidente d'énergie $E$ variable. Il permet en particulier de 
mettre en évidence l'effet tunnel. 

La transmission est tracée en fonction de l'énergie de la particule incidente. 
Sont également représentés, l'équivalent classique de la transmission et 
l'approximation de barrière large habituelle en mécanique quantique dans sa limite de validité.

Formules
--------
$T = \frac{4K^2k^2}{(K^2+k^2)\mathrm{sh}^2(Kd)+4K^2k^2}$

$K = \sqrt{2m(V_0-E)}/\hbar$

$k = \sqrt{2mE}/\hbar$


Informations
------------
Auteurs : Arnaud Raoux, François Lévrier, Pierre Cladé et la prépa agreg de Montrouge
Année de création : 2016 
Version : 1.2
Version de Python : 3.6
Licence : Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International

Liste des modifications :
    * v 1.00 : 2016-05-15 Première version complète
    * v 1.10 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor
    * v 1.2  : 2019-05-10 

"""

import numpy as np
from numpy.lib.scimath import sqrt
import matplotlib.pyplot as plt

from programmes_lecons import FloatSlider, IntSlider
from programmes_lecons import make_param_widgets, make_choose_plot, make_reset_button
from programmes_lecons import justify

titre = " Effet tunnel"

description = r"""
Ce programme permet de calculer la transmission d'une barrière de potentiel pour 
une onde de matière incidente d'énergie $E$ variable. Il permet en particulier de 
mettre en évidence l'effet tunnel. 

La transmission est tracée en fonction de l'énergie de la particule incidente. 
Sont également représentés, l'équivalent classique de la transmission et 
l'approximation de barrière large habituelle en mécanique quantique dans sa limite de validité.

$T = \frac{4K^2k^2}{(K^2+k^2)\mathrm{sh}^2(Kd)+4K^2k^2}$

$K = \sqrt{2m(V_0-E)}/\hbar$

$k = \sqrt{2mE}/\hbar$
"""

#===========================================================
# --- Variables globales et paramètres ---------------------
#===========================================================

hbar = 1
m = 1

V0 = 1 # Hauteur de la barriere, c'est l'unite d'energie
approx = 1.3 # Valeur minimale acceptable pour K*d afin que l'approximation de barriere large soit verifiée

parameters = {
    'E_max':FloatSlider(value=6, min=0, max=12, description="E_max"),
    'd':FloatSlider(value=2, min=0, max=6, description='Épaisseur de la barrière -- d')
}


#===========================================================
# --- Modèle physique --------------------------------------
#===========================================================

def transmission(E, V, d):
    """ Tranmission par effet tunnel: formule exacte"""
    k = sqrt(2*m*E)/hbar # Vecteur d'onde a l'exterieur de la barriere
    K = sqrt(2*m*(V-E))/hbar # Vecteur d'onde a l'interieur de la barriere
    #t = 2*i*k*K*np.exp(-i*k*d)*1/ ( (K**2+k**2)*np.sinh(K*d) + 2*i*K*k*np.cosh(K*d) ) # coefficient de transmission en amplitude
    T = np.real(4*K**2*k**2 / ( (K**2+k**2)**2*np.sinh(K*d)**2 + 4*K**2*k**2 ) ) # coefficient de transmission en probabilite
    return T

def transmission_classique(E, V, d):
    """Tranmission par effet tunnel: cas classique"""
    T = (E-V) > 0 # Si E>V, la particule passe, sinon elle est reflechie
    return T

def limite_large_barriere(E, V, d): 
    """Tranmission par effet tunnel: Cas d'une barriere épaisse, ou la formule se simplifie """
    k = sqrt(2*m*E)/hbar # Vecteur d'onde a l'exterieur de la barriere
    K = sqrt(2*m*(V-E))/hbar # Vecteur d'onde a l'interieur de la barriere
    T=np.real(16*K**2*k**2 / (K**2+k**2)**2 *np.exp(-2*K*d))
    validite = (E<V) & (K*d>approx)
    return T, validite

#===========================================================
# --- Réalisation du plot ----------------------------------
#===========================================================

# La fonction plot_data est appelée à chaque modification des paramètres
def plot_data(E_max=6, d=2):
    E_abscisse = np.linspace(0, E_max, 200)
    T_exact = transmission(E_abscisse, V0, d)
    T_classique = transmission_classique(E_abscisse, V0, d)
    T_large_barriere, validite_large_barriere = limite_large_barriere(E_abscisse, V0, d)

    lines['Quantique'].set_data(E_abscisse, T_exact)
    lines['Classique'].set_data(E_abscisse, T_classique)
    lines['barriere large'].set_data(E_abscisse[validite_large_barriere], T_large_barriere[validite_large_barriere])

    ax.set_xlim(0, E_max)

    fig.canvas.draw_idle()


#===========================================================
# --- Création de la figure et mise en page ----------------
#===========================================================

fig = plt.figure()
fig.suptitle(titre)
fig.text(0.02, .9, justify(description), multialignment='left', verticalalignment='top')

ax = fig.add_axes([0.35, 0.25, 0.6, 0.65])

lines = {}
lines['Quantique'], = ax.plot([], [], lw=2, color='red', label='Quantique')
lines['Classique'], = ax.plot([], [], ls='--', color='blue', label='Classique')
lines['barriere large'], = ax.plot([], [], lw=3, ls='--', color='green', label='barriere large: Kd>'+str(approx))

ax.legend()
ax.set_xlabel('Énergie (en unite de $V_0$)') 
ax.set_ylabel('Transmission')
ax.set_xlim(0, 6)
ax.set_ylim(0, 1.2*V0)

param_widgets = make_param_widgets(parameters, plot_data, slider_box=[0.45, 0.07, 0.5, 0.07])
choose_widget = make_choose_plot(lines, box=[0.015, 0.10, 0.2, 0.15])
reset_button = make_reset_button(param_widgets)

if __name__=='__main__':
    plt.show()
