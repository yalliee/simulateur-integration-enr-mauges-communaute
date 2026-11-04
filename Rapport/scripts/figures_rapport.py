import pandas as pd, numpy as np, json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
D="/mnt/user-data/uploads/Smart Grids/donnees/processed/"
NAVY="#0E2166"; ORA="#C85A12"; SOFT="#A6AEBB"; PV="#E3A21A"; EOL="#2A78D6"; GRID="#E3E6EC"; GREY="#595959"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"axes.edgecolor":"#9AA3AF","axes.labelcolor":GREY,"xtick.color":GREY,"ytick.color":GREY,
 "axes.grid":True,"grid.color":GRID,"grid.linewidth":0.6,"axes.spines.top":False,"axes.spines.right":False,"legend.frameon":False,"axes.axisbelow":True,
 "axes.formatter.use_locale":False})
def fr(x,d=0): return f"{x:,.{d}f}".replace(","," ").replace(".",",")
def save(f,name): f.savefig(f"figures/{name}.pdf",bbox_inches="tight"); plt.close(f)
h=pd.read_csv(D+"mauges_horaire_2021_2025.csv.gz",sep=";")
h["dt"]=pd.to_datetime(h.datetime_local,utc=True).dt.tz_convert("Europe/Paris")

# 1. carte communes : puissance ENR installée par habitant + comparaison sociale
g=json.load(open("/mnt/user-data/uploads/Smart Grids/simulateur/public/data/geo.json"))
f,(a,b)=plt.subplots(1,2,figsize=(7.4,3.4),gridspec_kw={"width_ratios":[1.15,1]})
vals={ft["properties"]["nom"]:(ft["properties"]["pv_MW"]+ft["properties"]["eol_MW"])*1e6/ft["properties"]["population"] for ft in g["communes"]["features"]}
cmap=plt.get_cmap("Blues"); vmax=4300
OFF={"Beaupréau-en-Mauges":(0.03,-0.03),"Montrevault-sur-Èvre":(-0.02,0.02),"Chemillé-en-Anjou":(0.02,0.0),"Mauges-sur-Loire":(0,0.01)}
for ft in g["communes"]["features"]:
    v=vals[ft["properties"]["nom"]]
    for poly in ft["geometry"]["coordinates"]:
        xy=np.array(poly[0]); a.add_patch(Polygon(xy,closed=True,fc=cmap(0.15+0.8*v/vmax),ec="white",lw=1))
    xy=np.array(ft["geometry"]["coordinates"][0][0]); cx,cy=xy[:,0].mean(),xy[:,1].mean()
    dx,dy=OFF.get(ft["properties"]["nom"],(0,0)); cx+=dx; cy+=dy
    nm=ft["properties"]["nom"].replace("-en-","-en-\n").replace("-sur-","-sur-\n").replace(" d'"," d'\n")
    a.text(cx,cy,f"{nm}\n{fr(v)} W/hab",ha="center",va="center",fontsize=5.8,color="white" if v>2500 else NAVY)
a.autoscale(); a.set_aspect(1/np.cos(np.radians(47.2))); a.axis("off"); a.set_title("Puissance ENR installée par habitant (2025)",fontsize=8.5,color=NAVY)
t=pd.read_csv(D+"territoire_insee.csv",sep=";").set_index("geo")
ind={"Logements en maison":t.maisons_2023/t.logements_2023,"Chauffage électrique":t.rp_chauffage_electricite_2023/t.rp_total_tableau_chauffage_2023,
     "Ménages à 2 voitures ou +":t.menages_2_voitures_plus_2023/t.residences_principales_2023,"Emplois industriels":t.emplois_industrie_2023/t.emplois_total_2023}
geos=[("Mauges","Mauges",NAVY),("49","Maine-et-Loire","#5B76B8"),("52","Pays de la Loire",SOFT),("FR","France","#D9DDE3")]
x=np.arange(len(ind)); w=0.2
for k,(gcode,lab,c) in enumerate(geos):
    ys=[ind[i].get(gcode,np.nan)*100 for i in ind]
    b.barh(x+(k-1.5)*w,ys,w,color=c,label=lab)
    if gcode=="Mauges":
        for xi,yv in zip(x,ys): b.text(yv+1.5,xi+(k-1.5)*w,fr(yv)+" %",va="center",fontsize=6.5,color=NAVY)
b.set_yticks([]); b.invert_yaxis()
for xi,nm in zip(x,ind): b.text(0,xi-0.47,nm,fontsize=7,color=GREY,va="bottom"); b.set_xlabel("%"); b.set_xlim(0,110)
b.legend(fontsize=6.5,ncol=4,loc="upper center",bbox_to_anchor=(0.45,-0.16)); b.set_ylim(len(ind)-0.45,-0.75); b.set_title("Un territoire rural, pavillonnaire et industriel (INSEE 2023)",fontsize=8.5,color=NAVY)
save(f,"territoire")

# 2. méthodes conso S et R : semaine de janvier 2024 + profil moyen
y=h[h.annee==2024]
f,(a,b)=plt.subplots(1,2,figsize=(7.2,2.5),gridspec_kw={"width_ratios":[1.7,1]})
wk=y[(y.dt>="2024-01-15")&(y.dt<"2024-01-22")]
a.plot(wk.dt,wk.conso_mauges_R_MW,color=NAVY,lw=1.1,label="Méthode R (éCO2mix régional)")
a.plot(wk.dt,wk.conso_mauges_S_MW,color=ORA,lw=1.1,label="Méthode S (profils Enedis)")
a.set_ylabel("MW"); a.legend(fontsize=7,loc="lower left"); a.set_title("Semaine du 15 janvier 2024",fontsize=8.5,color=NAVY)
import matplotlib.dates as mdates; a.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m",tz="Europe/Paris"))
p=y.groupby("heure_locale")[["conso_mauges_R_MW","conso_mauges_S_MW"]].mean()
b.plot(p.index,p.conso_mauges_R_MW,color=NAVY,lw=1.4); b.plot(p.index,p.conso_mauges_S_MW,color=ORA,lw=1.4)
b.set_xlabel("heure locale"); b.set_xticks([0,6,12,18,23]); b.set_title("Profil journalier moyen 2024",fontsize=8.5,color=NAVY)
save(f,"conso_methodes")

# 3. capacité éCO2mix
c=pd.read_csv(D+"capacites_eco2mix_52.csv",sep=";"); c["date"]=pd.to_datetime(c.date,utc=True)
f,(a,b)=plt.subplots(1,2,figsize=(7.2,2.3))
for ax,col,lab in [(a,"pv","Solaire"),(b,"eol","Éolien")]:
    ax.plot(c.date,c[f"cap_{col}_implicite_MW"],color=ORA,lw=1.2,drawstyle="steps-post",label="capacité implicite d'éCO2mix")
    ax.plot(c.date,c[f"cap_{col}_lissee_MW"],color=NAVY,lw=1.2,label="capacité lissée (correction)")
    ax.set_title(f"{lab}, Pays de la Loire",fontsize=8.5,color=NAVY); ax.set_ylabel("MW")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
a.legend(fontsize=7,loc="upper left")
save(f,"capacite_eco2mix")

# 4. saisonnalité : bilan mensuel A 2022 + journée de juillet A et B
y=h[h.annee==2022].copy(); y["prod"]=y.pv_A_MW+y.eol_A_MW+y.autres_enr_A_MW
m=y.groupby("mois").agg(pv=("pv_A_MW","sum"),eol=("eol_A_MW","sum"),au=("autres_enr_A_MW","sum"),c=("conso_mauges_MW","sum"))/1000
y["cov"]=np.minimum(y["prod"],y.conso_mauges_MW)
f,(a,b)=plt.subplots(1,2,figsize=(7.2,2.7))
mo=["J","F","M","A","M","J","J","A","S","O","N","D"]; x=np.arange(12)
a.bar(x,m.eol+m.au,0.6,color=EOL,label="éolien (+ autres ENR)"); a.bar(x,m.pv,0.6,bottom=m.eol+m.au,color=PV,label="solaire")
a.plot(x,m.c,color=NAVY,marker="o",ms=3,lw=1.4,label="consommation")
a.set_xticks(x); a.set_xticklabels(mo); a.set_ylabel("GWh"); a.set_title("Bilan mensuel, parc actuel (2022)",fontsize=8.5,color=NAVY)
j=y[(y.mois==7)&(y.est_weekend==0)].groupby("heure_locale")[["conso_mauges_MW","pv_A_MW","eol_A_MW","autres_enr_A_MW"]].mean()
hh=j.index
b.plot(hh,j.conso_mauges_MW,color=NAVY,lw=1.6,label="consommation")
b.plot(hh,1.2*j.conso_mauges_MW,color=NAVY,lw=1,ls="--",label="seuil de vigilance (120 %)")
b.plot(hh,j.pv_A_MW+j.eol_A_MW+j.autres_enr_A_MW,color=SOFT,lw=1.4,label="production A")
pb=2*j.pv_A_MW+j.eol_A_MW+j.autres_enr_A_MW
b.plot(hh,pb,color=ORA,lw=1.8,label="production B (solaire × 2)")
b.fill_between(hh,1.2*j.conso_mauges_MW,pb,where=pb>1.2*j.conso_mauges_MW,color=ORA,alpha=0.25,lw=0)
b.set_xlabel("heure locale"); b.set_ylabel("MW"); b.set_xticks([0,6,12,18,23]); b.set_title("Jour ouvré moyen de juillet 2022",fontsize=8.5,color=NAVY)
b.legend(fontsize=6.5,loc="upper center",bbox_to_anchor=(0.45,-0.25),ncol=2)
a.legend(fontsize=6.5,loc="upper center",bbox_to_anchor=(0.5,-0.12),ncol=3)
save(f,"saisonnalite")

# 5. batterie : écrêtement selon la taille
cb=pd.read_csv(D+"courbe_taille_batterie.csv",sep=None,engine="python")
f,axs=plt.subplots(1,2,figsize=(7.2,2.6),sharey=False)
for ax,sc,fiche in [(axs[0],"B",471),(axs[1],"C",706)]:
    for pil,col,lab in [("glouton",SOFT,"stocker tout surplus"),("pointe",NAVY,"stocker seulement les excès")]:
        q=cb[(cb.scenario==sc)&(cb.pilotage==pil)].groupby("energie_MWh").ecretement_part_prod.agg(["mean","min","max"])*100
        ax.plot(q.index,q["mean"],color=col,lw=1.5,marker="o",ms=2.5,label=lab); ax.fill_between(q.index,q["min"],q["max"],color=col,alpha=0.15,lw=0)
    ax.axhline(5,color=ORA,lw=1,ls="--"); ax.axvline(fiche,color=GREY,lw=0.8,ls=":")
    ax.text(fiche+10,ax.get_ylim()[1]*0.85,"taille de\nla fiche",fontsize=6.5,color=GREY,ha="left")
    ax.set_title(f"Scénario {sc}",fontsize=8.5,color=NAVY); ax.set_xlabel("énergie de la batterie (MWh)"); ax.set_ylabel("écrêtement (% de la production)")
axs[0].legend(fontsize=7); axs[1].text(80,3.6,"limite de 5 %",fontsize=6.5,color=ORA)
save(f,"batterie_taille")

# 6. trajectoires : carte de chaleur avec ballons
tj=pd.read_csv(D+"trajectoires.csv",sep=";"); tj=tj[(tj.horizon=="actuel")&(tj.paquet=="P1 ballons")&(tj.m_pv<=2.0)]
pvs=sorted(tj.m_pv.unique()); eos=sorted(tj.m_eol.unique())
M=tj.pivot(index="m_eol",columns="m_pv",values="couv_h")*100; E=tj.pivot(index="m_eol",columns="m_pv",values="ecret_max")*100
f,a=plt.subplots(figsize=(5.2,2.9))
im=a.imshow(M.values,origin="lower",cmap="Greens",vmin=40,vmax=75,aspect="auto")
for i,e in enumerate(M.index):
    for k,pv_ in enumerate(M.columns):
        ok=E.loc[e,pv_]<=5
        a.text(k,i,fr(M.loc[e,pv_],0)+("" if ok else "\n✕"),ha="center",va="center",fontsize=7.5,color=(NAVY if ok else "#8A8F99"))
        if not ok: a.add_patch(plt.Rectangle((k-.5,i-.5),1,1,fc="white",alpha=0.55,ec="none"))
r=list(M.index).index(1.5); cc=list(M.columns).index(1.25)
a.add_patch(plt.Rectangle((cc-.5,r-.5),1,1,fill=False,ec=ORA,lw=2))
a.set_xticks(range(len(M.columns))); a.set_xticklabels([f"+{int(round((v-1)*100))} %" for v in M.columns],fontsize=7)
a.set_yticks(range(len(M.index))); a.set_yticklabels([f"+{int(round((v-1)*100))} %" for v in M.index],fontsize=7)
a.set_xlabel("puissance solaire ajoutée"); a.set_ylabel("puissance éolienne ajoutée"); a.grid(False)
cb_=f.colorbar(im,ax=a,fraction=0.03,pad=0.02); cb_.set_label("taux de couverture (%)",fontsize=7)
save(f,"trajectoires")

# 7. postes
ps=[("Chemillé",23.1,37.0),("St-Pierre-\nMontlimart",0.9,13.6),("Le Genêt",0.5,8.8),("Aubigné",3.1,6.6),("La\nSourdrie",4.9,1.9),("Recou-\nvrance",33.3,4.7),("St-\nGeorges",29.0,1.5),("Vallet",29.9,4.6),("Cholet",44.6,0.4)]
f,a=plt.subplots(figsize=(7.2,2.5)); x=np.arange(len(ps))
a.bar(x-0.2,[p[1] for p in ps],0.38,color=SOFT,label="capacité S3REnR restante")
a.bar(x+0.2,[p[2] for p in ps],0.38,color=ORA,label="ajout du scénario recommandé (au prorata du parc)")
a.set_xticks(x); a.set_xticklabels([p[0] for p in ps],fontsize=7); a.set_ylabel("MW"); a.legend(fontsize=7)
save(f,"postes")
print("ok")
