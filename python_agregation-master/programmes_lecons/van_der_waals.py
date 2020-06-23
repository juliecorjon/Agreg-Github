r"""Transition liquide-vapeur pour un fluide de Van der Waals

Description
-----------
Ce programme représente le diagramme PV en unités réduite 
d'un fluide respectant l'équation d'état de Van der Waals. 
Les références de température, pression et volume sont 
prises au point critique.

Informations
------------
Auteurs : François Lévrier, Emmanuel Baudin, Arnaud Raoux, Pierre Cladé et la prépa agreg de Montrouge
Version 1.3
Version de Python : 3.6
Licence : Creative Commons Attribution - Pas d'utilisation Commerciale 4.0 International

Liste des modifications :
    * v 1.0 : 2016-05-02 Première version complète
    * v 1.1 : 2016-05-02 Mise à jour de la mise en page
    * v 1.2 : 2019-01-09 Remplacement de axisbg dépréciée par facecolor
    * v 1.3 : 2019-05-10 Simplification du programme. Utilisation d'un fichier JSON
"""

import json

import matplotlib.pyplot as plt
import numpy as np

from programmes_lecons import FloatSlider, IntSlider
from programmes_lecons import make_param_widgets, make_choose_plot, make_reset_button, make_log_button
from programmes_lecons import justify

titre = 'Transition liquide-vapeur pour un fluide de Van der Waals'

description = """Ce programme représente le diagramme PV en unités
réduites d'un fluide respectant l'équation d'état de Van der Waals. 
Les références de température, pression et volume sont prises
au point critique. 
"""



#===========================================================
# --- Variables globales et paramètres ---------------------
#===========================================================

parameters = {
    'Tr' : FloatSlider(value=0.9, description='Temperature reduite -- $T_r$', min=0.85, max=1.15),
}

#===========================================================
# --- Modèle physique --------------------------------------
#===========================================================

# On charge les tableaux precalcules qui contiennent les donnees pour la courbe spinodale et la courbe de saturation
datas = json.load(open('van_der_waals_precalc_data.json'))
p_spin = np.array(datas['p_spin'])
p_sat = np.array(datas['p_sat'])
v_spin = np.array(datas['v_spin'])
v_sat = np.array(datas['v_sat'])


# Equation de van der Waals en variables reduites
def VdW_Pr(Tr, Vr):
    return 8.0*Tr/(3.0*Vr-1.0) - 3/Vr**2

# Fonction de calcul de la spinodale
def spinodale(Tr):
    # On calcule la position des zeros de la derivee de p par rapport a v (tangentes horizontales)
    null_dpdv = np.roots([4.0*Tr,-9.0,6.0,-1.0])
    # On ne garde que les valeurs v>1/3, etant donnee que c'est une limite inferieure pour le volume reduit
    null_dpdv = null_dpdv[null_dpdv>1./3.]
    # On calcule la pression correspondant a chacun de ces points, et si elle est positive, on trace le point dans le plan (Vr,Pr)
    p = VdW_Pr(Tr, null_dpdv)
    local_v_spin = null_dpdv[p>0]
    local_p_spin = p[p>0]
    return local_v_spin, local_p_spin

# Fonction de calcul de la courbe de saturation
# Pour calculer la courbe de saturation, on suit la construction de Maxwell
# On explore un domaine de pression "raisonnable" entre les deux pressions correspondant aux tangentes horizontales
def saturation(Tr, Vr):
    # On calcule la pression reduite
    Pr = VdW_Pr(Tr, Vr)
    # On determine le domaine ou cette pression est inferieure a la pression de la courbe de saturation
    # On prendra garde, avant d'appeler cette fonction, a verifier que Tr<1
    mask = Pr<p_sat
    # On en tire les valeurs extremes, qui sont donc les volumes reduits correspondant aux croisements de l'isotherme avec la courbe de saturation
    V0 = Vr[mask][0]
    V1 = Vr[mask][-1]
    # On calcule les pressions correspondantes
    P0 = VdW_Pr(Tr, V0)
    P1 = VdW_Pr(Tr, V1)
    return [V0,V1],[P0,P1]


#===========================================================
# --- Réalisation du plot ----------------------------------
#===========================================================

# La fonction plot_data est appelée à chaque modification des paramètres
def plot_data(Tr):
    Vr = v_sat
    Pr = VdW_Pr(Tr, Vr)
    lines["Courbe spinodale"].set_data(Vr, Pr) 

    if(Tr<1.0):
        lines["spin"].set_data(*spinodale(Tr))
        lines['sat'].set_data(*saturation(Tr, Vr))
        lines["spin"].set_visible(True)
        lines["sat"].set_visible(True)
    else:
        lines["spin"].set_visible(False)
        lines["sat"].set_visible(False)

    fig.canvas.draw_idle()


#===========================================================
# --- Création de la figure et mise en page ----------------
#===========================================================

fig = plt.figure()
fig.suptitle(titre)
fig.text(0.02, .93, justify(description, 120), multialignment='left', verticalalignment='top')

ax = fig.add_axes([0.05, 0.16, 0.9, 0.7])

# On trace la courbe spinodale
ax.plot(v_spin, p_spin, 'k--', lw=2, label='Courbe spinodale')

# On trace la courbe de saturation
ax.plot(v_sat, p_sat, 'b--', lw=2, label="Courbe de saturation")

# Affichage du point critique
ax.plot(1.0,1.0,'go')

lines = {}
lines["Courbe spinodale"], = ax.plot([], [], lw=4, color='red', label="Isotherme")
lines["spin"], = ax.plot([], [], 'ko')
lines["sat"], = ax.plot([], [], 'bo',ls='-',lw=4)

ax.set_xlim(0.4, 3.0)
ax.set_ylim(0, 2.5)
ax.set_xlabel(r"Volume reduit $V_r$")
ax.set_ylabel(r"Pression reduite $P_r$")
ax.legend()


param_widgets = make_param_widgets(parameters, plot_data, slider_box=[0.25, 0.03, 0.4, 0.05])
reset_button = make_reset_button(param_widgets)

if __name__=='__main__':
    plt.show()



