import streamlit as st
import litellm
import os

# Tvůj API klíč z Groq (vložen pro tebe)
os.environ["GROQ_API_KEY"] = "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"

# 1. NASTAVENÍ STRÁNKY (Barvy a ikona)
st.set_page_config(
    page_title="Invictus AI", 
    page_icon="⚡", 
    layout="centered"
)

# 2. DESIGN (Trochu stylingu, aby to nebylo nudné)
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    h1, h3 {
        color: #ffffff !important;
        font-family: 'Helvetica', sans-serif;
    }
    .stButton>button {
        width: 100%;
        background-color: #00ffcc;
        color: black;
        font-weight: bold;
        border: None;
    }
    .stButton>button:hover {
        background-color: #00ccaa;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. OBSAH STRÁNKY
st.title("⚡ INVICTUS AI")
st.markdown("### Multi-modelový agregátor nové generace")
st.write("Zadej otázku a já proženu nejlepší AI modely světa, aby ti daly jeden dokonalý výsledek.")

# Vstupní pole
otazka = st.text_area("Tvoje otázka:", placeholder="Např. Jaký je nejlepší marketingový plán pro nový brand v roce 2026?", height=100)

# Tlačítko pro spuštění
if st.button("SPUSTIT ANALÝZU"):
    if otazka:
        # Animace načítání
        with st.status("🚀 Dotazuji se modelů Llama 3.3 a Mixtral...", expanded=True) as status:
            modely = ["groq/llama-3.3-70b-versatile", "groq/mixtral-8x7b-32768"]
            odpovedi = []
            
            # Postupně sbíráme odpovědi
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

            status.update(label="✅ Odpovědi sesbírány. Rozhodčí tvoří finální verdikt...", state="complete")

        # 4. ROZHODČÍ (Sjednocení textu)
        podklady = "\n\n---\n\n".join(odpovedi)
        
        with st.spinner("Skládám finální odpověď..."):
            try:
                final = litellm.completion(
                    model="groq/llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system", 
                            "content": "Jsi elitní analytik. Tvým úkolem je sjednotit odpovědi od různých AI. Vytvoř strukturovanou, čtivou a profesionální odpověď v češtině. Používej tučné písmo, odrážky a jasné sekce."
                        },
                        {"role": "user", "content": f"Otázka: {otazka}\n\nPodklady:\n{podklady}"}
                    ]
                )
                
                # ZOBRAZENÍ VÝSLEDKU
                st.markdown("---")
                st.markdown("## 🏆 Finální výsledek")
                st.markdown(final.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Chyba při tvorbě finální odpovědi: {e}")
    else:
        st.warning("Musíš nejdřív něco napsat!")

st.markdown("---")
st.caption("Powered by Groq & Invictus Dev Team 2026")