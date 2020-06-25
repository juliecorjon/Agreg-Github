# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo

#Le fichier de données sera à remplir dans le format (X,Y,ux,uy)
# données expérimentales
test = np.loadtxt('data.txt') #Nom du fichier à changer
X = test[:,0]
Y = test[:,1]

# incertitudes-types sur les données expérimentales (il faut commenter les lignes inutiles)
ux = test[:,2]
uy = test[:,3]

# fonction f décrivant la courbe à ajuster aux données
def f(x,p):
    a,b = p 
    return a*x+b

# fonction qui renvoie les paramères de la régression et leurs incertitudes
def linreg(y,x,uy=None,ux=None):
    if uy is None:
        uy=np.zeros(len(y))
    if ux is None:
        ux=np.zeros(len(x))
    # fonction d'écart pondérée par les erreurs
    def residual(p, y, x):
        if (uy is None and ux is None):
            return (y-f(x,p))
        return (y-f(x,p))/np.sqrt(uy**2 + (Dx_f(x,p)*ux)**2)
    # dérivée de la fonction f par rapport à la variable de contrôle x
    def Dx_f(x,p):
        a,b = p
        return a
    p0 = np.array([0,0]) # estimation initiale des paramètres : elle ne joue généralement aucun rôle néanmoins, le résultat de l'ajustement est parfois aberrant il faut alors choisir une meilleure estimation initiale
    result = spo.leastsq(residual, p0, args=(y, x), full_output=True) # on utilise l'algorithme des moindres carrés non-linéaires  disponible dans la biliothèque scipy (et indirectement la bibliothèque Fortran MINPACK qui implémente l'algorithme de Levenberg-Marquardt) pour déterminer le minimum voulu
    popt=result[0] # valeurs optimales des paramètres a et b
    a=popt[0] # coef directeur
    b=popt[1] # ordonnée à l'origine
    pcov=result[1] # matrice de variance-covariance estimée des paramètres a et b 
    upopt = np.sqrt(np.abs(np.diagonal(pcov))) # incertitudes-types sur ces paramètres
    ua=upopt[0] # incertitude sur a 
    ub=upopt[1] # incertitude sur b
    chi2r=np.sum(np.square(residual(popt,y,x)))/(x.size-popt.size) # Chi2 réduit pour les paramètres ajustés
    r2 =1 - (np.sum((y-f(x,popt))**2))/(np.sum((y-np.mean(y))**2))
    print('a = '+str(a)+' \pm '+str(ua))
    print('b = '+str(b)+' \pm '+str(ub))
    print('Chi2 = '+str(chi2r))
    print('R² = ' + str(r2))
    return a,b,ua,ub,chi2r,r2

#Affichage du graphique
fig = plt.figure(1,figsize = (8,6))
ax = plt.subplot2grid((1,1),(0,0))
ax.errorbar(X,Y,yerr=uy,xerr=ux,fmt="o",markersize=5,color='blue',ecolor='lightblue',label='Données')
a,b,ua,ub,chi2r,r2 = linreg(Y,X,uy=uy,ux=ux)
p=(a,b)
#Affichage dans la box sur la graphique
chaine = 'Modélisation :\n'
chaine1 = 'a = %.2f $\pm$ %.2f\n'%(a,ua)#.2f permettent de modifier le nb de chiffres significatifs (ici 2)
chaine2 = 'b = %.2f $\pm$ %.2f\n'%(b,ub)
chaine3 = '$\chi^2$  = %.5f \n'%(chi2r) 
chaine4 = '$R^2$  = %.5f \n'%(r2)
ax.plot(X,f(X,p),color='orange',label= chaine + chaine1 + chaine2 + chaine3 + chaine4)
ax.set_title('Titre')#Titre du graphique
ax.set_xlabel('Axe X (unité)')#Titre de l'axe X
#ax.set_xticks([0,2,3]) - choisit la position des labels voulus
#ax.set_xticklabels([-4,-8,150]) - choisit les noms des labels
ax.set_ylabel('Axe Y (unité) ')#Titre de l'axe Y
ax.legend(loc='best',prop={'size':10}) #Légande et localisation 
plt.tight_layout() #Correction de problèmes éventuels
plt.savefig('test.png',bbox_inches='tight',dpi=200) #Enregistrement de la figure















