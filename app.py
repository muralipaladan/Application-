import streamlit as st
import google.generativeai as genai

# പേജിന്റെ ഡിസൈൻ
st.set_page_config(page_title="Malayalam Application Builder", layout="centered")
st.title("📝 Malayalam Official Letter Generator")
st.write("മംഗ്ലീഷിൽ നൽകുന്ന വിവരങ്ങൾ ഉപയോഗിച്ച് ഔദ്യോഗിക മലയാളം അപേക്ഷകൾ തയ്യാറാക്കാം.")

# API കീ കോൺഫിഗറേഷൻ
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # API കീയ്ക്ക് സപ്പോർട്ട് ചെയ്യുന്ന മോഡലുകൾ കണ്ടുപിടിക്കാനുള്ള കോഡ്
    available_models = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # 'models/' എന്ന ഭാഗം ഒഴിവാക്കി പേര് മാത്രം ലിസ്റ്റിലേക്ക് മാറ്റുന്നു
            available_models.append(m.name.replace('models/', ''))
            
    if available_models:
        # ഡ്രോപ്പ് ഡൗൺ വഴി മോഡൽ തിരഞ്ഞെടുക്കാൻ സ്ക്രീനിൽ കാണിക്കുന്നു
        selected_model = st.selectbox("ലഭ്യമായ AI വേർഷൻ തിരഞ്ഞെടുക്കുക:", available_models)
        model = genai.GenerativeModel(selected_model)
    else:
        st.error("നിങ്ങളുടെ API കീയിൽ മോഡലുകൾ ഒന്നും ലഭ്യമല്ല. API കീ പരിശോധിക്കുക.")
        st.stop()
        
except Exception as e:
    st.error(f"API കീ നൽകുന്നതിൽ തകരാർ: ദയവായി Streamlit Secrets പരിശോധിക്കുക.")
    st.stop()

st.markdown("---")

# ഇൻപുട്ട് കോളങ്ങൾ
applicant_details = st.text_area("അപേക്ഷകന്റെ വിവരങ്ങൾ (From Address):", placeholder="പേര്, വിലാസം, ഫോൺ നമ്പർ...")
recipient_details = st.text_area("ആർക്കാണ് നൽകുന്നത് (To Address):", placeholder="ഉദ്യോഗസ്ഥന്റെ പേര്/പദവി, ഓഫീസ്...")
manglish_points = st.text_area("പ്രധാന കാര്യങ്ങൾ (Manglish Points):", placeholder="ഉദാഹരണത്തിന്: Enikku income certificate venam, education loan edukkan anu...")

# ബട്ടൺ
if st.button("അപേക്ഷ തയ്യാറാക്കുക (Generate Letter)"):
    if applicant_details and recipient_details and manglish_points:
        with st.spinner("അപേക്ഷ തയ്യാറാക്കുന്നു... ദയവായി കാത്തിരിക്കുക..."):
            
            # AI-യ്ക്കുള്ള സിസ്റ്റം പ്രോംപ്റ്റ്
            prompt = f"""
            You are an expert Malayalam official letter writer. Generate a highly formal Malayalam letter based on these details:
            
            From Address: {applicant_details}
            To Address: {recipient_details}
            Reason/Points (in Manglish): {manglish_points}
            
            Instructions:
            - Translate the Manglish reason into professional and formal Malayalam.
            - Structure it perfectly with Date, Subject (വിഷയം), Salutation (ബഹുമാനപ്പെട്ട സർ/മാഡം), Body Paragraph, Conclusion (വിശ്വസ്തതയോടെ), and Signature space.
            - Output ONLY the letter in Malayalam.
            """
            
            try:
                # തിരഞ്ഞെടുക്കപ്പെട്ട മോഡൽ ഉപയോഗിച്ച് റിസൾട്ട് ഉണ്ടാക്കുന്നു
                response = model.generate_content(prompt)
                st.success("അപേക്ഷ തയ്യാറാണ്!")
                st.markdown("---")
                st.write(response.text)
            except Exception as e:
                st.error(f"എന്തോ തകരാർ സംഭവിച്ചു: {e}")
    else:
        st.warning("ദയവായി എല്ലാ കോളങ്ങളും പൂരിപ്പിക്കുക!")
