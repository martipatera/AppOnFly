import pandas as pd

# === 1. Načtení dat ===
stripe = pd.read_csv(r'C:\Users\pater\Desktop\Složky\AppOnFly\Python\Narovnani_stavu\Exporty_pro_narovnani_stavu\stripe_export.csv')
firebase = pd.read_csv(r'C:\Users\pater\Desktop\Složky\AppOnFly\Python\Narovnani_stavu\Exporty_pro_narovnani_stavu\Firebase_export.csv', sep=";")
vmc = pd.read_csv(r'C:\Users\pater\Desktop\Složky\AppOnFly\Python\Narovnani_stavu\Exporty_pro_narovnani_stavu\vmc_export.csv', sep=";")
hyperv = pd.read_csv(r'C:\Users\pater\Desktop\Složky\AppOnFly\Python\Narovnani_stavu\Exporty_pro_narovnani_stavu\hyperV_export.csv')
hyperv_slozky = pd.read_csv(r'C:\Users\pater\Desktop\Složky\AppOnFly\Python\Narovnani_stavu\Exporty_pro_narovnani_stavu\hyper-v_slozky.csv')
zabbix = pd.read_csv(r'C:\Users\pater\Desktop\Složky\AppOnFly\Python\Narovnani_stavu\Exporty_pro_narovnani_stavu\zabbix_export.csv.csv')

# Předčištění
for df in [stripe, firebase, vmc]:
    df['virtualMachineId'] = df['virtualMachineId'].astype(str).str.strip().str.lower()

# === Sjednocení virtualMachineId ve všech tabulkách ===
stripe['virtualMachineId'] = stripe['virtualMachineId'].astype(str).str.strip().str.lower()
firebase['virtualMachineId'] = firebase['virtualMachineId'].astype(str).str.strip().str.lower()
vmc['virtualMachineId'] = vmc['virtualMachineId'].astype(str).str.strip().str.lower()


for df in [stripe, firebase, vmc, hyperv, hyperv_slozky, zabbix]:
    df.columns = df.columns.str.strip()

# === Spojování ===
unmatched = []

# 1. Stripe + Firebase
df_stripe_fb, not_matched = pd.merge(
    stripe, firebase,
    on='virtualMachineId',
    how='left',
    indicator=True,
    suffixes=('', '_firebase')
).pipe(
    lambda d: (
        d[d['_merge'] == 'both'].drop(columns=['_merge']),
        d[d['_merge'] == 'left_only'].assign(nepripojeno_na='firebase')
    )
)
unmatched.append(not_matched)

# 2. + VMC
df_vmc, not_matched = pd.merge(df_stripe_fb, vmc, on='virtualMachineId', how='left', indicator=True).pipe(
    lambda d: (
        d[d['_merge'] == 'both'].drop(columns=['_merge']),
        d[d['_merge'] == 'left_only'].assign(nepripojeno_na='vmc')
    )
)
unmatched.append(not_matched)

# === PŘED spojováním přes 'Name' – Sjednocení formátu ===

# U všech tabulek, které mají sloupec 'Name', převést na text, oříznout mezery a malá písmena
df_vmc['Name'] = df_vmc['Name'].astype(str).str.strip().str.lower()
hyperv['Name'] = hyperv['Name'].astype(str).str.strip().str.lower()
hyperv_slozky['Name'] = hyperv_slozky['Name'].astype(str).str.strip().str.lower()
zabbix['Name'] = zabbix['Name'].astype(str).str.strip().str.lower()




# 3. + Hyper-V
hv, not_matched = pd.merge(df_vmc, hyperv, on='Name', how='left', indicator=True).pipe(
    lambda d: (
        d[d['_merge'] == 'both'].drop(columns=['_merge']),
        d[d['_merge'] == 'left_only'].assign(nepripojeno_na='hyperv')
    )
)
unmatched.append(not_matched)

# Sjednocení formátu sloupce 'Name' před porovnáním
df_vmc['Name'] = df_vmc['Name'].astype(str).str.strip().str.lower()
hyperv_slozky['Name'] = hyperv_slozky['Name'].astype(str).str.strip().str.lower()
# 4. + Hyper-V složky
hvs, not_matched = pd.merge(df_vmc, hyperv_slozky, on='Name', how='left', indicator=True).pipe(
    lambda d: (
        d[d['_merge'] == 'both'].drop(columns=['_merge']),
        d[d['_merge'] == 'left_only'].assign(nepripojeno_na='hyperv_slozky')
    )
)
unmatched.append(not_matched)

zabbix['Name'] = zabbix['Name'].astype(str).str.strip().str.lower()
# 5. + Zabbix
zb, not_matched = pd.merge(df_vmc, zabbix, on='Name', how='left', indicator=True).pipe(
    lambda d: (
        d[d['_merge'] == 'both'].drop(columns=['_merge']),
        d[d['_merge'] == 'left_only'].assign(nepripojeno_na='zabbix')
    )
)
unmatched.append(not_matched)

# === Výstup ===
vysledek = pd.concat(unmatched, ignore_index=True)

# Vybrat jen důležité sloupce
sloupce = ['Customer Email', 'virtualMachineId', 'Name', 'nepripojeno_na']
vysledek = vysledek[[col for col in sloupce if col in vysledek.columns]]

# Ukázka jmen, která se nespojila na hyperv_slozky
selhala_jmena = vysledek[vysledek['nepripojeno_na'] == 'hyperv_slozky']['Name'].dropna().unique()
print("\n🧾 Prvních 10 jmen, která se nespojila s hyperv_slozky:")
print(selhala_jmena[:10])
# Zkontroluj, jestli některá z jmen opravdu existují v hyperv_slozky
print("\n🔍 Ověření: jsou tato jména v hyperv_slozky?")
for name in selhala_jmena[:10]:
    exists = name in hyperv_slozky['Name'].values
    print(f"{name} -> {'ANO' if exists else 'NE'}")

# Počet záznamů
print("Počet nespojených záznamů:", len(vysledek))
print("\n🧾 Počet záznamů podle místa, kde spojení selhalo:")
print(vysledek['nepripojeno_na'].value_counts())


# Ověř, zda je v chybovém výstupu
print(vysledek[vysledek['Name'] == 'AOFVPSSubs-168.75'])

# Ověř, zda je ve vstupu hyperv
print(hyperv[hyperv['Name'] == 'AOFVPSSubs-168.75'])

# Uložit CSV
vysledek.to_csv(
    r'C:\Users\pater\Desktop\Složky\AppOnFly\Python\Narovnani_stavu\Exporty_pro_narovnani_stavu\nespojene_zaznamy.csv',
    index=False,
    encoding='utf-8-sig'
)
print("Hotovo. Výstupní soubor: nespojene_zaznamy.csv")
