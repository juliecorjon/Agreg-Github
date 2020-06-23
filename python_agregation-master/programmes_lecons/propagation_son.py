"""Déplacement de poussières dans une onde sonore

Description
-----------

Ce programme représente les positions d'un ensemble 
de poussières soumises à une onde sonore à 2KHz et d'amplitude choisie.

Le choix de représenter des poussières plutôt que des particule du gaz 
permet de supprimer le problème de la représentation des vitesses thermiques. 

Les zones de compression et dilatation peuvent être directement observées.
Une poussière rouge est singularisée pour être suivie individuellement.
Deux graphiques inférieurs représentent le champ de pression et le champ
de vitesse respectivement. 

ATTENTION : Le niveau sonore de 190 dB SPL correspond à une surpression
de l'ordre de la pression atmosphèrique! L'hypothèse de perturbation
pour obtenir l'équation de propagation du son n'est donc pas valide.
Par ailleurs à ces niveaux la vitesse maximale de la particule fluide
dépasse la vitesse du son ce qui n'est pas possible. Il faut donc
prendre cette représentation avec prudence : ces niveaux extrêmes
sont nécessaires pour pouvoir observer le phénomène dans une classe,
mais ils ne correspondent pas à une situation réaliste. Au delà de
185 dB SPL, les champs de vitesse et de pression prédits par la théorie
et représentés ne correspondent plus à la distribution représentée. 

Informations
------------
Auteurs : Emmanuel Baudin, Arnaud Raoux, François Lévrier, Pierre Cladé et la prépa agreg de Montrouge
Version : v 1.2
Version de Python : 3.6
Licence : Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International

Liste des modifications :
    * v 1.0 : 2016-05-02 Première version complète - baudin@lpa.ens.fr
    * v 1.1 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor
    * v 1.2 : 2019-05-10 Simplification du programme

"""


titre = 'Déplacement de poussières dans une onde sonore'

description = """Ce programme représente les positions d'un ensemble de poussières soumises à une onde sonore à 2KHz et d'amplitude choisie.""" 



import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from programmes_lecons import FloatSlider, IntSlider
from programmes_lecons import make_param_widgets, make_choose_plot, make_reset_button, make_start_stop_animation
from programmes_lecons import justify


#===========================================================
# --- Variables globales et paramètres ---------------------
#===========================================================

cs = 340. #Vitesse du son en m/s
Pr = 2E-5 #Pression de référence (Pa) pour le calcul du niveau sonore en dB SPL
P0 = 1.01325E5 #Pression atmospherique moyenne (Pa)
rho0 = 1.184 #Masse volumique de l'air moyenne a 25°C (kg/m**3)
f0 = 2000. #Frequence de l'onde sonore en Hz
lambda0 = cs/f0 #Longueur d'onde de l'onde sonore (m)

parameters = dict(
    L = FloatSlider(description='Amplitude sonore (dB SPL)', min=160, max=190, value=180), # Remarquer la valeur initiale a 190 dB SPL
    T = FloatSlider(description='Temps t (ms)', min=0., max=1., value=0) # Remarquer la valeur initiale à 0
)


#===========================================================
# --- Modèle physique --------------------------------------
#===========================================================

def onde_pression(x, A,  t):
	return (A*np.sin(2.*pi/lambda0*(x-cs*t)))

def onde_vitesse(x, A,  t):
	return (A*np.sin(2.*pi/lambda0*(x-cs*t)))

def poussieres(x, y, A,  t):
	return ((x + A*np.cos(2.*pi/lambda0*(x-cs*t)))), 2*(y-0.5)


#===========================================================
# --- Réalisation du plot ----------------------------------
#===========================================================

# La fonction plot_data est appelée à chaque modification des paramètres
def plot_data(L, T):
    AP = (10.**(L/20.))*np.sqrt(2)*Pr #Amplitude de pression sonore. 
    A = AP/P0*lambda0/2./pi #Amplitude du déplacement sonore.
    Av = AP/rho0/cs #Amplitude de la vitesse des particules de poussiere

    T = T/1000. #Valeur recuperee en s

    lines['points'].set_data(*poussieres(part_x, part_y, A, T))
    lines['point_rouge'].set_data(*poussieres(np.array([0.5]), np.array([0.5]), A, T))
    
    lines['pression'].set_data(x_graph, onde_pression(x_graph, AP,  T))
    lines['vitesse'].set_data(x_graph, onde_vitesse(x_graph, Av, T))

    fig.canvas.draw_idle()


#===========================================================
# --- Création de la figure et mise en page ----------------
#===========================================================

fig = plt.figure()
fig.suptitle(titre)
fig.text(0.5, .93, description, multialignment='left', verticalalignment='top', horizontalalignment='center')

ax1, ax2, ax3 = fig.subplots(3, 1, sharex=True,
            gridspec_kw={'left':0.1, 'bottom':0.25, 'top':0.9, 'hspace':0.05})


lines = {}
lines['points'], = ax1.plot([], [], 'o', color='blue', markersize=3, alpha=0.3, markeredgecolor='none')
lines['point_rouge'], = ax1.plot([],[], 'o', color='red', markersize=5., alpha=0.8, markeredgecolor='none')
lines['pression'], = ax2.plot([],[], lw=2, color='red')
lines['vitesse'], = ax3.plot([],[], lw=2, color='black')


ax1.set_xlim(0, 1)
ax1.set_ylim(-1, 1)
ax1.axes.get_yaxis().set_visible(False)

ax2.set_ylabel('Surpression (Pa)')
ax2.set_ylim(-1E5, 1E5)
ax2.axhline(0, color='k')

ax3.set_ylabel('Vitesse (m/s)')
ax3.set_ylim(-1E2, 1E2)
ax3.set_xlabel('Position (m)')
ax3.axhline(0, color='k')

#On créé n particules à des positions aléatoires sur la fenêtre observée 
n=500
part_x, part_y = np.random.rand(2, n)

x_graph = np.linspace(0, 1, 1001)


param_widgets = make_param_widgets(parameters, plot_data, slider_box=[0.35, 0.07, 0.4, 0.10])
reset_button = make_reset_button(param_widgets)

#===========================================================
# --- Animation --------------------------------------------
#===========================================================

start_animation = False # Est-ce que l'animation se lance automatiquement ? 

def animation_function(val):
    param_widgets['T'].set_val((val/100)%1)
    if val==0 and start_animation==False:
        ani.event_source.stop()
    return lines.values()

ani = animation.FuncAnimation(fig, animation_function, interval=100.0)
anim_btn = make_start_stop_animation(ani, start_animation=start_animation)

if __name__=='__main__':
    plt.show()

