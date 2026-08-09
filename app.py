import streamlit as st
import google.generativeai as genai

# പേജിന്റെ ഡിസൈൻ
st.set_page_config(page_title="Malayalam Application Builder", layout="centered")
st.title("📝 Malayalam Official Letter Generator")
st.write("മംഗ്ലീഷിൽ നൽകുന്ന വിവരങ്ങൾ ഉപയോഗിച്ച് ഔദ്യോഗിക മലയാളം അപേക്ഷകൾ തയ്യാറാക്കാം.")

# API കീ നൽകാൻ (Streamlit Secrets വഴി)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # ഇവിടെയാണ് Gemini 3.1 വേർഷൻ നൽകിയിരിക്കുന്നത്. 
    # നിങ്ങളുടെ API-യ്ക്ക് അനുസരിച്ച് 'gemini-3.1-flash' അല്ലെങ്കിൽ 'gemini-3.1-pro' ഉപയോഗിക്കാം.
    model = genai.GenerativeModel('gemini-3.1-flash') 
    
except Exception as e:
    st.error("API Key സെറ്റ് ചെയ്തിട്ടില്ല. ദയവായി Streamlit Secrets-ൽ കീ നൽകുക.")

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
            
            # AI റിസൾട്ട്
            try:
                response = model.generate_content(prompt)
                st.success("അപേക്ഷ തയ്യാറാണ്!")
                st.markdown("---")
                st.write(response.text)
            except Exception as e:
                st.error(f"എന്തോ തകരാർ സംഭവിച്ചു: {e}")
    else:
        st.warning("ദയവായി എല്ലാ കോളങ്ങളും പൂരിപ്പിക്കുക!")
