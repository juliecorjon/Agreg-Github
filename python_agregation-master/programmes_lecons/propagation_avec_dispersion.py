"""Propatation d'un paquet d'onde avec dispersion

Description
-----------

Ce programme permet d'observer l'effet de la dispersion sur la propagation 
d'une onde, et en particulier de faire la différence entre vitesse de phase 
et vitesse de groupe.

Formules
--------

Informations
------------
Auteurs : Vincent Lusset, Arnaud Raoux, Pierre Cladé et la prépa agreg de Montrouge
Année de création : 2018
Version : 1.2
Version de Python : 3.6
Licence : Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International

Liste des modifications :
    * v 1.00 : 2018-03-01 Première version complète
    * v 1.10 : 2019-03-12 Amélioration, simplification et nettoyage du code
    * v 1.2  : 2019-05-10 Calcul en temps réel. 
"""

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from numpy import exp, cos, pi


from programmes_lecons import FloatSlider, IntSlider
from programmes_lecons import make_param_widgets, make_choose_plot, make_reset_button, make_start_stop_animation
from programmes_lecons import justify



titre =  r"Propatation d'un paquet d'onde avec dispersion"

description = """Ce programme permet d'observer l'effet de la dispersion 
sur la propagation d'une onde, et en particulier de faire la différence 
entre vitesse de phase et vitesse de groupe."""


#===========================================================
# --- Variables globales et paramètres ---------------------
#===========================================================

T=0.25 #période de l'onde

#définition des vitesses de phase et de groupe (à optimiser, avec vphi > vg)
c=1
vphi=1.1*c # Pas de dispersion si vphi=vg
vg=c**2/vphi

tau = 15 # Temps d'amortissement de l'onde. À comparer à Tmax

parameters = dict(
    t = FloatSlider(description='$t$ (ms)', min=0, max=10., value=0),
    )

#===========================================================
# --- Modèle physique --------------------------------------
#===========================================================

def enveloppe(t, x):
    att = 1+(t/tau)**2
    return exp(-(t-x/vg)**2/att)/att

def amplitude(t, x):
    att = 1+(t/tau)**2
    return enveloppe(t, x) * cos(2*pi/T*(t-x/vphi))


Xmin = -2
Xmax = 10.0 #échelle max selon l'axe de propagation

NbEchantillons=3000 # Échantillonage spatial
x = np.linspace(Xmin, Xmax, NbEchantillons) # x est ici un array en ligne


#===========================================================
# --- Réalisation du plot ----------------------------------
#===========================================================

# La fonction plot_data est appelée à chaque modification des paramètres
def plot_data(t):
    att = 1+(t/tau)**2
    lines['courbe'].set_data(x, amplitude(t, x))

    lines['enveloppes_p'].set_data(x, enveloppe(t, x))
    lines['enveloppes_m'].set_data(x, -enveloppe(t, x))

    lines['points_vg'].set_data([vg*t], [1/att])
    x_vphi = np.array([t*vphi])
    lines['points_vphi'].set_data(x_vphi, amplitude(t, x_vphi))

    

#===========================================================
# --- Création de la figure et mise en page ----------------
#===========================================================

fig = plt.figure()
fig.suptitle(titre)

ax = fig.add_axes([0.08, 0.15, 0.84, 0.75], xlim=(Xmin, Xmax), ylim=(-1.5, 1.5))

ax.set_xlabel(r'x')
ax.set_ylabel(r'$\psi$')


ax.axhline(y=1,xmin=Xmin,xmax=Xmax,linestyle=':',color='grey') 
ax.axhline(y=-1,xmin=Xmin,xmax=Xmax,linestyle=':',color='grey') 

lines = {}
lines['courbe'], = ax.plot([],[],'c-')
lines['enveloppes_p'], = ax.plot([], [], 'r--')
lines['enveloppes_m'], = ax.plot([], [], 'r--')

lines['points_vg'], = ax.plot([], [], 'ro')  # point rouge avançant à vg
lines['points_vphi'], = ax.plot([], [], 'bo') # point bleu avançant à vphi


param_widgets = make_param_widgets(parameters, plot_data, slider_box=[0.08+0.84*2/12, 0.01, 0.84*10/12, 0.05])

#===========================================================
# --- Animation --------------------------------------------
#===========================================================

start_animation = False # Est-ce que l'animation se lance automatiquement ? 

def animation_function(val):
    param_widgets['t'].set_val((val/10)%10)
    # Astuce permettant de stopper l'animation tout de suite
    if val==0 and start_animation==False:
        ani.event_source.stop()
    return lines.values()

ani = animation.FuncAnimation(fig, animation_function, interval=100.0)
anim_btn = make_start_stop_animation(ani, box=[0.01, 0.01, 0.07, 0.1], start_animation=start_animation)

if __name__=="__main__":
    plt.show()
