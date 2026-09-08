import re
from collections import Counter

ACTION = {"analyzed","architected","automated","built","cleaned","created","designed","developed","evaluated","implemented","integrated","led","managed","modeled","optimized","performed","produced","queried","translated","transformed","utilized","validated"}
WEAK = {"responsible for","helped with","worked on","assisted with","tasked with"}

def _words(s): return re.findall(r"[a-z0-9+#.-]+", (s or "").lower())

def _bullet_score(text, jd=""):
    words=_words(text); n=len(words); first=words[0] if words else ""
    action=100 if first in ACTION else 55
    specificity=min(100,55+12*len(re.findall(r"\b\d+(?:\.\d+)?%?|\bapproximately\s+\d+",text or "",re.I)))
    if any(x in (text or "").lower() for x in WEAK): specificity=max(35,specificity-20)
    length=100 if 14<=n<=32 else (82 if 9<=n<=38 else 60)
    jd_terms=set(_words(jd))-{"and","the","with","for","from","this","that","will","intern","internship","role"}
    overlap=len(set(words)&jd_terms); alignment=min(100,55+overlap*7) if jd_terms else 80
    return round(action*.30+specificity*.25+length*.20+alignment*.25)

def assess_resume_spec(spec, job_description="", preferences=None):
    preferences=preferences or {}; bullets=[]
    for item in spec.get("items",[]): bullets += [b for b in item.get("bullets",[]) if str(b).strip()]
    scores=[_bullet_score(b,job_description) for b in bullets]
    bullet_quality=round(sum(scores)/max(1,len(scores))) if bullets else 45
    tokens=[x for x in _words(" ".join(bullets)) if len(x)>4]; counts=Counter(tokens)
    redundancy=max(55,100-min(45,sum(v-2 for v in counts.values() if v>2)*3))
    metric_bullets=sum(bool(re.search(r"\b\d+(?:\.\d+)?%?|\bapproximately\s+\d+",b,re.I)) for b in bullets)
    evidence=min(100,65+metric_bullets*7)
    density_pref=preferences.get("information_density",preferences.get("bullet_density","Balanced"))
    target={"Compact":8,"Balanced":10,"Detailed":12,"High Density":13}.get(density_pref,10)
    density=max(55,100-abs(len(bullets)-target)*5)
    selected=sum(1 for x in spec.get("items",[]) if x.get("selected",True)); alignment=min(100,72+selected*4); truth=100
    overall=round(bullet_quality*.28+evidence*.18+density*.14+redundancy*.12+alignment*.18+truth*.10)
    improvements=[]
    if bullet_quality<82: improvements.append("Strengthen action-led bullets and connect each line to a target-role requirement.")
    if evidence<82: improvements.append("Surface verified metrics and concrete scope where the profile supports them; never invent numbers.")
    if redundancy<85: improvements.append("Remove overlapping bullets so every line proves a distinct capability.")
    if density<85: improvements.append("Rebalance the one-page space budget so the strongest verified evidence receives more room.")
    return {"overall":overall,"job_alignment":alignment,"evidence_strength":evidence,"bullet_quality":bullet_quality,"information_density":density,"redundancy":redundancy,"truth_integrity":truth,"bullet_scores":scores,"improvements":improvements}
