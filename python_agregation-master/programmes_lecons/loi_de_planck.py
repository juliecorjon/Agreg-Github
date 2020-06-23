r"""Loi de Planck

Description
-----------
Ce programme représente la loi de Planck du corps noir en fonction de la 
fréquence du rayonnement électromagnétique. Il est possible de modifier 
la température du corps noir pour observer les effets. 

Les lois de Rayleigh-Jeans et de Wien ont aussi été implémentées pour comparaison.

Formules
--------
Planck : $\frac{2h\nu^3}{c^2 (e^{h\nu/kT} -1)}$

Wien : $\frac{2h\nu^3}{c^2 e^{h\nu/kT}}$

Rayleigh-Jeans: $\frac{2kT\nu^2}{c^2}$


Informations
------------
Auteurs : François Lévrier, Emmanuel Baudin, Arnaud Raoux, Pierre Cladé et la prépa agreg de Montrouge
Année de création : 2016 
Version : 1.3
Version de Python : 3.6
Licence : Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International

Liste des modifications:
    * v 1.0 : 2016-03-01 Première version complète
    * v 1.1 : 2016-05-02 Mise à jour de la mise en page - baudin@lpa.ens.fr
    * v 1.2 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor
    * v 1.3 : 2019-05-10 Simplification du programme
"""
import matplotlib.pyplot as plt
import numpy as np

from programmes_lecons import FloatSlider, IntSlider
from programmes_lecons import make_param_widgets, make_choose_plot, make_reset_button, make_log_button
from programmes_lecons import justify
from programmes_lecons.constantes import c, h, k

titre = r'Loi de Planck'

description = r"""Ce programme représente la loi de Planck du corps noir en 
fonction de la fréquence du rayonnement électromagnétique.

Les lois de Rayleigh-Jeans et de Wien sont également tracées.

Planck : $\frac{2hc^2}{\lambda^5 (e^{hc/(\lambda kT)} -1)}$

Wien : $\frac{2hc^2}{\lambda^5 e^{hc/(\lambda kT)}}$

Rayleigh-Jeans: $\frac{2kTc}{\lambda^4}$

"""


#===========================================================
# --- Variables globales et paramètres ---------------------
#===========================================================

parameters = {
    'T' : FloatSlider(value=5800, description='Température -- $T$ (K)', min=1, max=10000),
    }


#===========================================================
# --- Modèle physique --------------------------------------
#===========================================================

def loi_de_planck_nu(T, nu):
    return 2*h*nu**3/c**2 * 1/(np.exp(h*nu/(k*T)) - 1 )

def loi_de_rayleigh_jeans_nu(T, nu):
    return 2*k*T*nu**2/c**2

def loi_de_wien_nu(T, nu):
    return 2*h*nu**3/c**2 * 1/(np.exp(h*nu/(k*T)))


def loi_de_planck_lamb(T, lamb):
    return loi_de_planck_nu(T, c/lamb)*c/lamb**2

def loi_de_rayleigh_jeans_lamb(T, lamb):
    return loi_de_rayleigh_jeans_nu(T, c/lamb)*c/lamb**2

def loi_de_wien_lamb(T, lamb):
    return loi_de_wien_nu(T, c/lamb)*c/lamb**2


#===========================================================
# --- Réalisation du plot ----------------------------------
#===========================================================

# La fonction plot_data est appelée à chaque modification des paramètres
def plot_data(T):

    lines['Planck'].set_data(lamb*1E6, loi_de_planck_lamb(T, lamb)*1E-12)
    lines['Wien'].set_data(lamb*1E6, loi_de_wien_lamb(T, lamb)*1E-12)
    lines['Rayleigh-Jeans'].set_data(lamb*1E6, loi_de_rayleigh_jeans_lamb(T, lamb)*1E-12)

    i = loi_de_planck_lamb(T, lamb).argmax()
    lines['max'].set_data([lamb[i]*1E6], [loi_de_planck_lamb(T, lamb[i])*1E-12])

    i = loi_de_wien_lamb(T, lamb).argmax()
    lines['maxW'].set_data([lamb[i]*1E6], [loi_de_wien_lamb(T, lamb[i])*1E-12])

    fig.canvas.draw_idle()


#===========================================================
# --- Création de la figure et mise en page ----------------
#===========================================================

fig = plt.figure()
fig.suptitle(titre)
fig.text(0.02, .9, justify(description), multialignment='left', verticalalignment='top')

ax = fig.add_axes([0.35, 0.3, 0.6, 0.6])

ax.axvline(c/6.7E14*1E6,lw=2, color='purple') #violet
ax.axvline(c/5.7E14*1E6,lw=2, color='green') #vert
ax.axvline(c/4.6E14*1E6,lw=2, color='red') #rouge

ax.text(c/4.5E14*1E6, 14, "rouge :  633 nm", color='red', rotation='vertical',horizontalalignment='left', verticalalignment='top')
ax.text(c/5.6E14*1E6, 14, "vert : 525 nm", color='green', rotation='vertical',horizontalalignment='left', verticalalignment='top')
ax.text(c/6.5E14*1E6, 14, "violet : 425 nm", color='purple', rotation='vertical',horizontalalignment='left', verticalalignment='top')

lines = {}
lines['Planck'], = ax.plot([], [], lw=2, color='blue', visible=True)
lines['Wien'], = ax.plot([], [], lw=2,color='black', visible=False)
lines['Rayleigh-Jeans'], = ax.plot([], [], lw=2, color='brown',visible=False)

lines['max'], = ax.plot([], [], 'o', markersize=15, color='blue')
lines['maxW'], = ax.plot([], [], 'o', markersize=15, color='black', visible=False)


lamb = np.logspace(-7, -5.5,num=1001)

ax.set_xlim(lamb.min()*1E6, lamb.max()*1E6)
ax.set_ylim(0, 30)

ax.set_xlabel(r"$\lambda$ [$\mathrm{\mu m}$]")
#ax.set_ylabel(r"$B_\nu$ [$\mathrm{W.m^{-2}.Hz^{-1}.sr^{-1}}$]")
ax.set_ylabel(r"$B_\nu$ [$\mathrm{kW.m^{-2}.nm^{-1}.sr^{-1}}$]")

param_widgets = make_param_widgets(parameters, plot_data, slider_box=[0.35, 0.07, 0.4, 0.05])
choose_widget = make_choose_plot(lines, box=[0.015, 0.25, 0.2, 0.15], which=[('Planck', 'max'), ('Wien', 'maxW'), 'Rayleigh-Jeans'])
reset_button = make_reset_button(param_widgets)
log_button =  make_log_button(ax, ylims={'log':(0.001, 1000), 'linear':ax.get_ylim()})

if __name__=='__main__':
    plt.show()



