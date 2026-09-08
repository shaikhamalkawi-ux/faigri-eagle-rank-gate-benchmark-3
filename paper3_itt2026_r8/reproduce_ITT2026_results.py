#!/usr/bin/env python3
"""Paper 3 ITT 2026 R8 - paper-specific aligned crisp/fuzzy replay.

Run from paper3_itt2026_r8/ inside the public benchmark repository.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
BASE_CASES = REPO / "data" / "baseline_case_inputs.csv"
PUBLIC_ROWS = REPO / "data" / "mandatory_safeguards_46.csv"
SYNTH_ROWS = HERE / "synthetic_sensitivity_rows_4.csv"
CRITERIA = ["P", "F", "T", "H", "L"]
ALL = CRITERIA + ["r"]
LAMBDA = 0.75


def dense_rank_desc(values):
    return pd.Series(values).rank(ascending=False, method="dense").astype(int).to_numpy()


def crisp_topsis(df):
    X = df[ALL].to_numpy(float)
    norms = np.sqrt(np.sum(X * X, axis=0))
    weights = np.ones(6) / 6.0
    V = (X / norms) * weights
    pos = np.array([V[:, j].max() if j < 5 else V[:, j].min() for j in range(6)])
    neg = np.array([V[:, j].min() if j < 5 else V[:, j].max() for j in range(6)])
    dp = np.sqrt(np.sum((V - pos) ** 2, axis=1))
    dm = np.sqrt(np.sum((V - neg) ** 2, axis=1))
    cc = dm / (dp + dm)
    return cc, dense_rank_desc(cc), norms, weights, pos, neg


def vertex_distance(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return float(np.sqrt(np.mean((a - b) ** 2)))


def aligned_fuzzy(df, h, norms, weights, pos, neg):
    out = []
    for _, row in df.iterrows():
        dp2 = dm2 = 0.0
        for j, col in enumerate(ALL):
            x = float(row[col])
            tri = np.array([x, x, x]) if col == "r" else np.array([max(0, x-h), x, min(1, x+h)])
            vtri = weights[j] * tri / norms[j]
            ptri = np.repeat(pos[j], 3)
            ntri = np.repeat(neg[j], 3)
            dp2 += vertex_distance(vtri, ptri) ** 2
            dm2 += vertex_distance(vtri, ntri) ** 2
        dp, dm = np.sqrt(dp2), np.sqrt(dm2)
        out.append(dm / (dp + dm))
    return np.asarray(out)


def family(label):
    s = str(label).lower()
    if any(k in s for k in ["privacy", "cybersecurity", "retention", "data terms"]): return "Privacy/data"
    if any(k in s for k in ["fairness", "bias", "proportionality"]): return "Fairness/proportionality"
    if any(k in s for k in ["appeal", "contestab", "human", "supervision", "override", "false-positive", "non-sole-use", "escalation", "reconsideration"]): return "Human review/recourse"
    if any(k in s for k in ["transparency", "audit trail", "explainability"]): return "Transparency/auditability"
    return "Institutional/legal boundaries"


def main():
    df = pd.read_csv(BASE_CASES).rename(columns={"Case_ID":"Case"})
    pub = pd.read_csv(PUBLIC_ROWS)
    syn = pd.read_csv(SYNTH_ROWS)
    gate = pub.groupby("Case_ID")["m_ij"].apply(lambda x: int((x == 1).all())).to_dict()
    df["Gate_documented"] = df["Case"].map(gate).astype(int)
    df["Gate_state"] = np.where(df.Gate_documented.eq(1), "Documented", "Hold")
    df["G"] = df[CRITERIA].mean(axis=1)
    df["S075"] = df.G * np.exp(-LAMBDA * df.r)

    crisp_cc, crisp_rank, norms, weights, pos, neg = crisp_topsis(df)
    df["Crisp_TOPSIS_CC"] = crisp_cc
    df["Crisp_TOPSIS_rank"] = crisp_rank
    fuzzy0 = aligned_fuzzy(df, 0.0, norms, weights, pos, neg)
    assert np.max(np.abs(fuzzy0 - crisp_cc)) < 1e-12
    fuzzy10 = aligned_fuzzy(df, 0.10, norms, weights, pos, neg)
    df["Fuzzy_TOPSIS_CC_h010"] = fuzzy10
    df["Fuzzy_TOPSIS_rank_h010"] = dense_rank_desc(fuzzy10)

    rho_f = float(spearmanr(fuzzy10, crisp_cc).statistic)
    rho_g = float(spearmanr(df.G, crisp_cc).statistic)
    rho_s = float(spearmanr(df.S075, crisp_cc).statistic)
    widths=[]
    for h in [0.05,0.10,0.15]:
        cc=aligned_fuzzy(df,h,norms,weights,pos,neg)
        rr=dense_rank_desc(cc)
        t=pd.DataFrame({"Case":df.Case,"cc":cc,"rank":rr,"gate":df.Gate_documented}).sort_values(["rank","Case"])
        top=t.head(5)
        widths.append([h,float(spearmanr(cc,crisp_cc).statistic),int((top.gate==0).sum()),",".join(top.Case)])
    width_df=pd.DataFrame(widths,columns=["TFN_half_width","Spearman_vs_crisp_TOPSIS","Top5_Hold_count","Top5_set"])

    pub["Sensitivity_family"] = pub["Mandatory_Safeguard"].map(family)
    families=["Privacy/data","Fairness/proportionality","Transparency/auditability","Human review/recourse","Institutional/legal boundaries"]
    frows=[]
    base=[c for c,g in pub.groupby("Case_ID") if (g.m_ij==1).all()]
    frows.append(["None (baseline)",len(base),11-len(base),", ".join(base)])
    for fam in families:
        passes=[c for c,g in pub.groupby("Case_ID") if (g[g.Sensitivity_family!=fam].m_ij==1).all()]
        frows.append([fam,len(passes),11-len(passes),", ".join(passes)])
    fam_df=pd.DataFrame(frows,columns=["Removed_family","Documented_cases","Hold_cases","Passing_case_IDs"])

    df.to_csv(HERE/"P3_ITT2026_R8_Aligned_Crisp_Fuzzy_Gate_Results.csv",index=False)
    width_df.to_csv(HERE/"P3_ITT2026_R8_Fuzzy_Width_Sensitivity.csv",index=False)
    fam_df.to_csv(HERE/"P3_ITT2026_R8_Leave_One_Safeguard_Family_Out.csv",index=False)
    pub[["Case_ID","Safeguard_ID","Mandatory_Safeguard","m_ij","Sensitivity_family"]].to_csv(HERE/"P3_ITT2026_R8_Safeguard_Family_Map.csv",index=False)

    summary={"n_cases":11,"documented":int(df.Gate_documented.sum()),"hold":int((df.Gate_documented==0).sum()),
             "mandatory_rows_total":int(len(pub)+len(syn)),"mandatory_rows_public":int(len(pub)),"mandatory_rows_synthetic":int(len(syn)),
             "spearman_fuzzy_vs_crisp_h010":rho_f,"spearman_G_vs_crisp":rho_g,"spearman_S075_vs_crisp":rho_s,
             "h0_max_abs_difference_from_crisp":float(np.max(np.abs(fuzzy0-crisp_cc))),
             "top5_h010":width_df.loc[width_df.TFN_half_width.eq(.10),"Top5_set"].iloc[0],
             "top5_hold_h010":int(width_df.loc[width_df.TFN_half_width.eq(.10),"Top5_Hold_count"].iloc[0])}
    (HERE/"P3_ITT2026_R8_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n")

    fig,ax=plt.subplots(figsize=(6.9,3.55))
    for gatev,marker,label in [(0,"o","Veto Hold"),(1,"s","Mandatory documented")]:
        sub=df[df.Gate_documented.eq(gatev)]
        ax.scatter(sub.Crisp_TOPSIS_rank,sub.Fuzzy_TOPSIS_CC_h010,marker=marker,s=52,label=label,facecolors="none" if gatev==1 else None)
    for _,row in df.iterrows():
        if row.Case not in ("C01","C02"):
            ax.text(row.Crisp_TOPSIS_rank+.08,row.Fuzzy_TOPSIS_CC_h010+.0025,row.Case,fontsize=7)
    y=float(df.loc[df.Case.eq("C01"),"Fuzzy_TOPSIS_CC_h010"].iloc[0]); ax.text(2.1,y+.0035,"C01/C02",fontsize=7,fontweight="bold")
    ax.set_xlabel("Crisp TOPSIS rank (1 = highest)"); ax.set_ylabel("Aligned fuzzy TOPSIS closeness (h = 0.10)")
    ax.set_title(f"Aligned fuzzy sensitivity preserves rank; documentary gate remains separate (rho={rho_f:.3f})",fontsize=9.1)
    ax.set_xticks(range(1,11)); ax.grid(axis="y",alpha=.25); ax.legend(fontsize=7,loc="lower left"); fig.tight_layout()
    fig.savefig(HERE/"Fig1_Crisp_Fuzzy_Gate_ITT2026_R8.png",dpi=300,bbox_inches="tight"); plt.close(fig)

    expected={"C01":2,"C02":2,"C03":1,"C04":3,"C05":6,"C06":7,"C07":4,"C08":8,"C09":5,"C10":10,"C11":9}
    assert all(int(df.loc[df.Case.eq(c),"Crisp_TOPSIS_rank"].iloc[0])==r for c,r in expected.items())
    assert abs(rho_f-1.0)<1e-12 and all(abs(x-1.0)<1e-12 for x in width_df.Spearman_vs_crisp_TOPSIS)
    assert len(pub)==46 and len(syn)==4 and summary["documented"]==2 and summary["hold"]==9 and summary["top5_hold_h010"]==3
    assert fam_df.loc[fam_df.Removed_family.eq("Human review/recourse"),"Documented_cases"].iloc[0]==3
    print("PAPER3_ITT2026_R8_REPRODUCTION: PASS")

if __name__ == "__main__": main()
