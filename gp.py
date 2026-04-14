import math

def calcola_barili_massimi(ability_haste):
    cooldown_base = 13  # Ricarica al livello massimo dell'abilità (Grado 5)
    durata_barile = 25  # Secondi prima che il barile scompaia
    barili_iniziali = 5 # Cariche massime immagazzinabili
    
    # 1. Calcolo del tempo di ricarica con la Ability Haste
    tempo_ricarica = cooldown_base * (100 / (100 + ability_haste))
    
    # 2. Calcolo dei barili che si ricaricano prima che il primo scompaia (arrotondato per difetto)
    barili_generati = math.floor(durata_barile / tempo_ricarica)
    
    # 3. Totale barili in campo
    totale_barili = barili_iniziali + barili_generati
    
    return totale_barili





def calcola_danno_barile_con_amp(ad, crit, damage_amp=0.0, is_crit=False):
    # aDMG = Danno base dell'attacco (Q + AD)
    aDMG_base = 130 + ad
    
    # 1. Prima applicazione dell'Amp all'attacco innescante
    aDMG_amped = aDMG_base * (1 + damage_amp)
    
    # Danni aggiuntivi che NON beneficiano della prima amp (o che consideriamo a parte)
    sDMG = 169 + (crit / 2)  # Spellblade
    cDMG = 155               # Danno bonus barile
    
    moltiplicatore_critico = 2.30
    
    if is_crit:
        # Il critico moltiplica l'attacco innescante già amplificato
        danno_barile_pre_amp = (aDMG_amped * moltiplicatore_critico) + sDMG + cDMG
    else:
        danno_barile_pre_amp = aDMG_amped + sDMG + cDMG
        
    # 2. Seconda applicazione dell'Amp al danno finale scaturito dall'esplosione
    danno_finale = danno_barile_pre_amp * (1 + damage_amp)
    
    return danno_finale


def calcolachaingp(danno_primobarile,danno_primobarile_crit,damage_amp,numero_barili_massimo):
    print('danni barile num  1','   non crit:', round(danno_primobarile),'crit:',round(danno_primobarile_crit))
    barreldamagecrit = danno_primobarile_crit
    barreldamage = danno_primobarile
    numero_barili_massimo -= 1
    barrel = 1
    while (numero_barili_massimo == 0) == False:
        barreldamagecrit = round(barreldamagecrit*(1+damage_amp))
        barreldamage = round(barreldamage*(1+damage_amp))
        barrel += 1
        numero_barili_massimo -= 1
        print('danni barile num ',barrel,'   non crit:', barreldamage,'crit:',barreldamagecrit)




endless_hunger = 0
gplevel = 18
ad = 146 + 66 + 55 + 50 + 30 + 15 + 100
crit = 100
penetrazione_oggetti = 0.35 
ignora_barile = 0.40        
letalita = 18                
ability_haste = ((ad/10)*endless_hunger) + 400
critmod = 2.3 + 0.625 + 0.25
damage_amp = 1.48




max_barili = calcola_barili_massimi(ability_haste)
max_crit = round(calcola_danno_barile_con_amp(ad, crit, damage_amp, is_crit=True),2)
max_base = round(calcola_danno_barile_con_amp(ad, crit, damage_amp, is_crit=False),2)
print('max barili:',max_barili,' x')

print('max danno  1 barrel:',max_base)
print('max danno crit 1 barrel:',max_crit," 💥")


calcolachaingp(max_base,max_crit,damage_amp,max_barili)




















def calcola_danno_effettivo_gp(danno_base, armatura_bersaglio, armor_pen_perc, ignora_armatura_perc, letalita):
    """
    Calcola il danno fisico post-mitigazione includendo l'effetto "Ignora Armatura".
    
    :param danno_base: Danno fisico (es. danno del barile di Gangplank).
    :param armatura_bersaglio: Armatura totale del nemico.
    :param armor_pen_perc: Penetrazione armatura % degli oggetti (es. 0.30 per Memento Mori/Dominik).
    :param ignora_armatura_perc: % di armatura ignorata dall'abilità (es. 0.40 per i barili di GP).
    :param letalita: Valore di Letalità fissa dell'attaccante.
    """
    
    # 1. Calcolo dell'Armatura dopo le riduzioni percentuali
    # Le percentuali si "stackano" in modo moltiplicativo.
    # Il bersaglio mantiene: (1 - 30%) * (1 - 40%) della sua armatura
    moltiplicatore_armatura = (1 - armor_pen_perc) * (1 - ignora_armatura_perc)
    armatura_dopo_percentuali = armatura_bersaglio * moltiplicatore_armatura
    
    # 2. Applicazione Letalità (Penetrazione Fissa calcolata come 1:1 nelle patch moderne)
    armatura_finale = armatura_dopo_percentuali - letalita
    
    # L'armatura considerata non può scendere sotto lo zero per via della penetrazione
    if armatura_finale < 0:
        armatura_finale = 0
        
    # 3. Calcolo del Moltiplicatore di Danno
    # Formula: 100 / (100 + Armatura)
    moltiplicatore_danno = 100 / (100 + armatura_finale)
    
    # 4. Danno finale
    danno_post_mitigazione = danno_base * moltiplicatore_danno
    
    return round(danno_post_mitigazione, 2)



