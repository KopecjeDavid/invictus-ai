import streamlit as st
import litellm
import os
import requests
from bs4 import BeautifulSoup

# Načtení klíče (pro jistotu ponecháno i zde, ale Streamlit Cloud si ho bere ze Secrets)
os.environ["GROQ_API_KEY"] = "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"

# 1. NASTAVENÍ STRÁNKY
st.set_page_config(
    page_title="Invictus AI Pro", 
    page_icon="⚡", 
    layout="centered"
)

# Funkce pro stažení textu z webu (pro analýzu konkurence)
def nacti_web(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Odstranění nepotřebných prvků
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return "\n".join(chunk for chunk in chunks if chunk)[:4000]
    except Exception as e:
        return f"Chyba při čtení webu: {e}"

# 2. DESIGN (Neon Invictus Style)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: #00ffcc !important; font-family: 'Helvetica', sans-serif; }
    .stButton>button {
        width: 100%;
        background-color: #00ffcc;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        height: 3em;
    }
    .stButton>button:hover { background-color: #00ccaa; color: white; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #1a1c23;
        color: white;
        border: 1px solid #00ffcc;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. OBSAH STRÁNKY
st.title("⚡ INVICTUS AI PRO")
st.markdown("### Inteligentní Business Agregátor")

# Záložky pro přepínání funkcí
tab1, tab2 = st.tabs(["🔍 Chytré hledání", "🕵️ Analýza konkurence"])

# --- TAB 1: CHYTRÉ HLEDÁNÍ ---
with tab1:
    otazka = st.text_area("Tvoje otázka:", placeholder="Zadej dotaz pro analýzu více modely...", height=100)
    if st.button("SPUSTIT MULTI-ANALÝZU"):
        if otazka:
            with st.status("🚀 Dotazuji se modelů Llama 3.3 a Llama 3.1...", expanded=True) as status:
                # AKTUALIZOVANÉ MODELY (Mixtral nahrazen Llama 3.1 8B)
                modely = ["groq/llama-3.3-70b-versatile", "groq/llama-3.1-8b-instant"]
                odpovedi = []
                
                for m in modely:
                    try:
                        st.write(f"Sběr dat z: {m.split('/')[-1]}...")
                        res = litellm.completion(
                            model=m, 
                            messages=[{"role": "user", "content": otazka}]
                        )
                        odpovedi.append(res.choices[0].message.content)
                    except Exception as e:
                        st.error(f"Chyba u modelu {m}: {e}")

                status.update(label="✅ Data sesbírána. Generuji verdikt...", state="complete")

            podklady = "\n\n---\n\n".join(odpovedi)
            with st.spinner("Skládám finální odpověď..."):
                final = litellm.completion(
                    model="groq/llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Jsi elitní analytik. Sjednoť odpovědi do jedné profesionální české zprávy s odrážkami."},
                        {"role": "user", "content": f"Otázka: {otazka}\n\nPodklady:\n{podklady}"}
                    ]
                )
                st.markdown("---")
                st.markdown("## 🏆 Finální výsledek")
                st.markdown(final.choices[0].message.content)
        else:
            st.warning("Napiš otázku!")

# --- TAB 2: ANALÝZA KONKURENCE ---
with tab2:
    st.write("Vlož URL adresu konkurence a já ti řeknu, jak je porazit.")
    url_konkurence = st.text_input("URL konkurenta:", placeholder="https://www.priklad.cz")
    
    if st.button("ROZEBRAT WEBOVOU STRÁNKU"):
        if url_konkurence:
            with st.spinner("Skenuji web a připravuji strategii..."):
                obsah_webu = nacti_web(url_konkurence)
                
                if "Chyba" in obsah_webu:
                    st.error(obsah_webu)
                else:
                    prompt = f"""
                    Jsi elitní business konzultant. Tady je obsah webu konkurence:
                    {obsah_webu}
                    
                    Proveď analýzu pro brand INVICTUS:
                    1. Hlavní prodejní argument (Co slibují?).
                    2. Tonalita (Jak mluví na lidi?).
                    3. 3 slabá místa, kde je může INVICTUS přejet.
                    4. Návrh konkrétního kroku pro INVICTUS.
                    Napiš česky, stručně, úderně.
                    """
                    
                    res = litellm.completion(
                        model="groq/llama-3.3-70b-versatile", 
                        messages=[{"role": "user", "content": prompt}]
                    )
                    st.markdown("---")
                    st.markdown("## 🕵️ Strategický report")
                    st.markdown(res.choices[0].message.content)
        else:
            st.warning("Vlož URL!")

st.markdown("---")
st.caption("Powered by Groq & Invictus Dev Team 2026")
