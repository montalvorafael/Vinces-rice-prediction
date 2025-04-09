import pandas as pd

# Read the CSV file
df = pd.read_csv("INEC_ctnac_BD_2018.csv", sep = ';', low_memory=False)
data = pd.DataFrame(df)
print(data)
arr = []
tipo_riego = [] #tipo de riego
fqui_npk = [] #fertilizante quimico NPK
fqui_nit = [] #f nitrogeno
fqui_fos = [] #f fosforo
fqui_pot = [] #f potasio
pq_herb = [] #herbicidas lb
pq_ins = [] #insecticida lb
pq_fun = [] #fungicida lb

#functions
def convertidorLibra(numero, medida, arreglo):
    if row[medida] == "1":
        #print(numero)
        arreglo.append(numero)
    elif row[medida] == "2":
        convertor_kg= float(numero) * 2.2046
        arreglo.append(str(convertor_kg).replace(".",","))
    elif row[medida] == "3":
        convertor_q = float(numero) * 100
        arreglo.append(str(convertor_q).replace(".",","))
    elif row[medida] == "4":
        convertor_tn= float(numero) * 2204.62
        arreglo.append(str(convertor_tn).replace(".",","))
    elif row[medida] == "5":
        convertor_lt= float(numero) * 2.20
        arreglo.append(str(convertor_lt).replace(".",","))
    else:
        arreglo.append(" ")

def convertidorLitros(numero, medida, arreglo):
    if row[medida] == "1":
        convertor_lb = float(numero) * 0.4535
        arreglo.append(str(convertor_lb).replace(".",","))
    elif row[medida] == "2":
        arreglo.append(numero.replace(".",","))
    elif row[medida] == "3":
        convertor_q = float(numero) * 20
        arreglo.append(str(convertor_q).replace(".",","))
    elif row[medida] == "4":
        convertor_tn= float(numero) * 1000
        arreglo.append(str(convertor_tn).replace(".",","))
    elif row[medida] == "5":
        arreglo.append(numero.replace(".",","))
    else:
        arreglo.append(" ")

variables_names = ["Identificador", "ct_clacul", "ct_prepa_suelo", "ct_k510h", "ct_k511h", "ct_afecta_prod", "ct_riego", 
"ct_superf_regada_ha", "Tipo_riego", "ct_fqui", "ct_fqui_npk","ct_fqui_nit", "ct_fqui_fos", "ct_fqui_pot", "su_fertilizada",
"ct_pqui", "pq_herb","ct_color_her_pq", "pq_ins","ct_color_ins_pq", "pq_fun", "ct_color_fun_pq", "su_plaguicidas", "ct_prod",
"Ventas"] #cambiar por ct_clacul, (2019) cambiar ct_clacul, ct_510h, ct_511h, ct_pqui (ct_afito) (2018)


for index, row in data.iterrows():
    if str(row["Identificador"])[0:4] == "1208" and row["ct_clacul"] == 507: #cambiar rc_clacul por ct_clacul (2019,2018)
        #tipo de riego
        if row["ct_porc_surc"] == "100":
            tipo_riego.append("1")
        elif row["ct_porc_aspe"] == "100":
            tipo_riego.append("2")
        elif row["ct_porc_micr"] == "100":
            tipo_riego.append("3")
        elif row["ct_porc_gote"] == "100":
            tipo_riego.append("4")
        elif row["ct_porc_nebu"] == "100":
            tipo_riego.append("5")
        elif row["ct_porc_otro"] == "100":
            tipo_riego.append("6")
        else: tipo_riego.append("0")

        #fertilizante
        #f organico no hay en arroz
        #fqui_npk
        if row["ct_cantidad_npk_fq"] != " ":
            numero = row["ct_cantidad_npk_fq"].replace(",",".")
            convertidorLibra(numero,"ct_umed_npk_fq", fqui_npk)
        else: 
            fqui_npk.append(" ")

        #f. nitrogenado
        if row["ct_cantidad_nit_fq"] != " ":
            numeroNit = row["ct_cantidad_nit_fq"].replace(",",".")
            convertidorLibra(numeroNit,"ct_umed_nit_fq", fqui_nit)
        else: 
            fqui_nit.append(" ")

        #f. fosfatado
        if row["ct_cantidad_fq"] != " ":
            numeroFos = row["ct_cantidad_fq"].replace(",",".")
            convertidorLibra(numeroFos,"ct_umed_fq", fqui_fos)
        else: 
            fqui_fos.append(" ")

        #f. potasico
        if row["ct_cantidad_pot_fq"] != " ":
            numeroPot = row["ct_cantidad_pot_fq"].replace(",",".")
            convertidorLibra(numeroPot,"ct_umed_pot_fq", fqui_pot)
        else: 
            fqui_pot.append(" ")


        #plaguisidas

        #herbicidas
        if row["ct_cantidad_her_pq"] != " ":
            numeroHerb = row["ct_cantidad_her_pq"].replace(",",".")
            convertidorLitros(numeroHerb,"ct_umed_her_pq", pq_herb)
        else: 
            pq_herb.append(" ")
        
        #insectisidas
        if row["ct_cantidad_ins_pq"] != " ":
            numeroInsec = row["ct_cantidad_ins_pq"].replace(",",".")
            #print(row["ct_umed_ins_pq"])
            convertidorLitros(numeroInsec,"ct_umed_ins_pq", pq_ins)
        else: 
            pq_ins.append(" ")
        
        #fungicidas
        if row["ct_cantidad_fun_pq"] != " ":
            numeroFun = row["ct_cantidad_fun_pq"].replace(",",".")
            print(row["ct_umed_fun_pq"])
            convertidorLitros(numeroFun,"ct_umed_fun_pq", pq_fun)
        else: 
            pq_fun.append(" ")


        arr.append(index)
    else: 
        tipo_riego.append(" ")
        fqui_npk.append(" ")
        fqui_nit.append(" ")
        fqui_fos.append(" ")
        fqui_pot.append(" ")
        pq_herb.append(" ")
        pq_ins.append(" ")
        pq_fun.append(" ")

df2 = data.assign(Tipo_riego=tipo_riego, ct_fqui_npk= fqui_npk, ct_fqui_nit= fqui_nit, ct_fqui_fos= fqui_fos, ct_fqui_pot= fqui_pot,
 pq_herb= pq_herb, pq_ins= pq_ins, pq_fun= pq_fun)

result = df2.iloc[arr]
result = result[variables_names]

print(result)
result.to_csv("vinces2018.csv", sep=';')
    