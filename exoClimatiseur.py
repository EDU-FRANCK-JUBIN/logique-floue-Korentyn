import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
#cf pdf 09 page 111


temperatures = ctrl.Antecedent(np.arange(5, 70, 5), 'temperatures')
humidite = ctrl.Antecedent(np.arange(16, 100, 7), 'humidite')
puissance = ctrl.Consequent(np.arange(0.0, 3.0, 0.01), 'puissance')

#Paramètrage graphe températures
temperatures['VVC'] = fuzz.trimf(temperatures.universe, [0, 5, 15])
temperatures['VC'] = fuzz.trimf(temperatures.universe, [5, 15, 25])
temperatures['C'] = fuzz.trimf(temperatures.universe, [15, 25, 35])
temperatures['F'] = fuzz.trimf(temperatures.universe, [25, 35, 45])
temperatures['H'] = fuzz.trimf(temperatures.universe, [35, 45, 55])
temperatures['VH'] = fuzz.trimf(temperatures.universe, [45, 55, 65])
temperatures['VVH'] = fuzz.trimf(temperatures.universe, [55, 65, 75])
#temperatures.view()

#Paramètrage graphe humidité
humidite['VVL'] = fuzz.trimf(humidite.universe, [2, 16, 30])
humidite['VL'] = fuzz.trimf(humidite.universe, [16, 30, 44])
humidite['L'] = fuzz.trimf(humidite.universe, [30, 44, 58])
humidite['M'] = fuzz.trimf(humidite.universe, [44, 58, 72])
humidite['H'] = fuzz.trimf(humidite.universe, [58, 72, 86])
humidite['VH'] = fuzz.trimf(humidite.universe, [72, 86, 100])
humidite['VVH'] = fuzz.trimf(humidite.universe, [86, 100, 114])
#humidite.view()

#Paramètrage graphe puissance climatiseur
puissance['VVL'] = fuzz.trapmf(puissance.universe, [0, 0, 0.166, 0.333])
puissance['VL'] = fuzz.trapmf(puissance.universe, [0.166, 0.333, 0.666, 0.833])
puissance['L'] = fuzz.trapmf(puissance.universe, [0.666, 0.833, 1.166, 1.333])
puissance['M'] = fuzz.trapmf(puissance.universe, [1.166, 1.333, 1.666, 1.833])
puissance['H'] = fuzz.trapmf(puissance.universe, [1.666, 1.833, 2.166, 2.333])
puissance['VH'] = fuzz.trapmf(puissance.universe, [2.166, 2.333, 2.666, 2.833])
#puissance.view()

#Règlages du climatiseur
rule1 = ctrl.Rule(temperatures['VVC'] | humidite['VVL'], puissance['VVL'])
rule2 = ctrl.Rule(temperatures['VVC'] | humidite['VL'], puissance['VVL'])
rule3 = ctrl.Rule(temperatures['VVC'] | humidite['L'], puissance['VL'])
rule4 = ctrl.Rule(temperatures['VVC'] | humidite['M'], puissance['VL'])
rule5 = ctrl.Rule(temperatures['VC'] | humidite['VVL'], puissance['VVL'])
rule6 = ctrl.Rule(temperatures['VC'] | humidite['VL'], puissance['VL'])
rule7 = ctrl.Rule(temperatures['VC'] | humidite['L'], puissance['VL'])
rule8 = ctrl.Rule(temperatures['VC'] | humidite['M'], puissance['L'])
rule9 = ctrl.Rule(temperatures['C'] | humidite['VVL'], puissance['VL'])
rule10 = ctrl.Rule(temperatures['C'] | humidite['VL'], puissance['VL'])
rule11 = ctrl.Rule(temperatures['C'] | humidite['L'], puissance['L'])
rule12 = ctrl.Rule(temperatures['C'] | humidite['M'], puissance['L'])
rule13 = ctrl.Rule(temperatures['F'] | humidite['VVL'], puissance['VL'])
rule14 = ctrl.Rule(temperatures['F'] | humidite['VL'], puissance['L'])
rule15 = ctrl.Rule(temperatures['F'] | humidite['L'], puissance['L'])
rule16 = ctrl.Rule(temperatures['F'] | humidite['M'], puissance['M'])

#Enregistrement des réglages
reglages_clim = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8,
                                 rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16])

#Application des réglages
climatiseur = ctrl.ControlSystemSimulation(reglages_clim)

#Paramétrage des conditions du test
climatiseur.input['temperatures'] = 35
climatiseur.input['humidite'] = 100

#Calcule de la puissance
climatiseur.compute()


#Affichage du résultat
puissance.view(sim=climatiseur)
#print(climatiseur.output['puissance'])

#Test 2 non couvert par les paramètres du climatiseur
# climatiseur.input['temperatures'] = 45
# climatiseur.input['humidite'] = 75
# climatiseur.compute()
# puissance.view(sim=climatiseur)

#Test 3
climatiseur.input['temperatures'] = 50
climatiseur.input['humidite'] = 50
climatiseur.compute()
puissance.view(sim=climatiseur)
