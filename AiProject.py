import streamlit as st
import time
import streamlit.components.v1 as components
from typing import List, Set

# ==========================================
# 1. المحرك الأساسي (Student 1 & 2)
# ==========================================
class Rule:
    def __init__(self, rule_id, conditions, conclusion, description, priority=1):
        self.rule_id = rule_id
        self.conditions = set(conditions)
        self.conclusion = conclusion
        self.description = description
        self.priority = priority

class InteractiveExpertSystem:
    def __init__(self):
        self.rules: List[Rule] = [
            Rule("R01", ["sara_prior_argument"], "sara_motive", "خلاف سابق بين سارة وريم."),
            Rule("R02", ["khalid_financial_dispute"], "khalid_motive", "خلاف مالي بين خالد وريم."),
            Rule("R03", ["majed_prior_dispute"], "majed_motive", "خلاف سابق بين ماجد وريم."),
            Rule("R04", ["noura_family_dispute"], "noura_motive", "خلاف عائلي بين نورة وريم."),
            Rule("R05", ["khalid_seen_near_lake_during_window"], "khalid_opportunity", "رؤية خالد قرب البحيرة وقت الجريمة."),
            Rule("R06", ["sara_left_before_window", "sara_no_return_verified"], "sara_verified_alibi", "تأكيد خروج سارة وعدم عودتها."),
            Rule("R07", ["khalid_shoeprint_match"], "khalid_physical_link", "تطابق آثار الحذاء مع خالد."),
            Rule("R08", ["khalid_device_location_near_lake"], "khalid_location_confirmed", "موقع جهاز خالد يؤكد وجوده بالبحيرة."),
            Rule("R09", ["majed_camera_access", "camera_shutdown_under_majed_account"], "majed_tampering_suspected", "شك في عبث ماجد بالكاميرات."),
            Rule("R10", ["noura_home_video_during_window"], "noura_verified_alibi", "فيديو المنزل يؤكد حجة غياب نورة."),
            Rule("R11", ["khalid_motive", "khalid_opportunity"], "khalid_primary_suspect", "خالد مشتبه به أولي."),
            Rule("R12", ["khalid_primary_suspect", "khalid_physical_link", "khalid_location_confirmed"], "khalid_strong_suspicion", "اشتباه قوي ضد خالد."),
            Rule("R13", ["sara_verified_alibi"], "sara_excluded", "استبعاد سارة."),
            Rule("R14", ["noura_verified_alibi"], "noura_excluded", "استبعاد نورة."),
            Rule("R15", ["khalid_strong_suspicion", "khalid_forensic_link", "no_material_contradiction_verified"], "khalid_guilty", "إثبات إدانة خالد."),
        ]
        self.evidence_facts = {
            "E01": ["sara_bracelet_at_lake"], "E02": ["sara_left_before_window", "sara_no_return_verified"],
            "E03": ["khalid_financial_dispute"], "E04": ["khalid_seen_near_lake_during_window"],
            "E05": ["khalid_shoeprint_match"], "E06": ["majed_camera_access"],
            "E07": ["camera_shutdown_under_majed_account"], "E08": ["majed_prior_dispute"],
            "E09": ["noura_family_dispute"], "E10": ["noura_home_video_during_window"],
            "E11": ["khalid_left_at_1022"], "E12": ["majed_fingerprint_on_control_box"],
            "E13": ["khalid_device_location_near_lake"], "E14": ["khalid_forensic_link"],
        }
        self.discovered_evidence: Set[str] = set()
        self.confirmed_extra_facts: Set[str] = set()
        self.facts: Set[str] = set()
        self.fired_rules: Set[str] = set()
        self.rule_trace = []

    def _rebuild_working_memory(self):
        self.facts = set(self.confirmed_extra_facts)
        for evidence_id in self.discovered_evidence:
            self.facts.update(self.evidence_facts[evidence_id])
        self.fired_rules.clear()
        self.rule_trace.clear()

    def add_evidence(self, evidence_id):
        if evidence_id not in self.evidence_facts: raise ValueError("Unknown ID")
        if evidence_id not in self.discovered_evidence:
            self.discovered_evidence.add(evidence_id)
            self.confirmed_extra_facts.discard("no_material_contradiction_verified")
            self._rebuild_working_memory()

    def add_confirmed_fact(self, fact):
        if fact != "no_material_contradiction_verified":
            self.confirmed_extra_facts.discard("no_material_contradiction_verified")
        self.confirmed_extra_facts.add(fact)
        self._rebuild_working_memory()

    def run_forward_chaining(self):
        ordered_rules = sorted(self.rules, key=lambda rule: (-rule.priority, rule.rule_id))
        while True:
            rule_fired_in_loop = False
            for rule in ordered_rules:
                if rule.rule_id in self.fired_rules: continue
                if not rule.conditions.issubset(self.facts): continue
                self.fired_rules.add(rule.rule_id)
                if rule.conclusion in self.facts: continue
                self.facts.add(rule.conclusion)
                rule_fired_in_loop = True
                self.rule_trace.append({"rule_id": rule.rule_id, "conditions": sorted(rule.conditions), "conclusion": rule.conclusion, "description": rule.description})
            if not rule_fired_in_loop: break
        return set(self.facts)

    def resolve_conflicts(self):
        problems = []
        if "khalid_verified_elsewhere_during_window" in self.confirmed_extra_facts:
            problems.append("دليل غياب موثق: خالد كان في مكان آخر.")
        if "material_contradiction_verified" in self.confirmed_extra_facts:
            problems.append("تم التحقق من وجود تعارض جوهري.")
        if problems:
            self.confirmed_extra_facts.discard("no_material_contradiction_verified")
            self._rebuild_working_memory()
            return {"status": "CONFLICT", "details": problems}
        if "no_material_contradiction_verified" in self.confirmed_extra_facts:
            return {"status": "CLEAR", "details": ["لا يوجد تعارض جوهري."]}
        return {"status": "REVIEW_REQUIRED", "details": ["المراجعة المستقلة مطلوبة."]}

    def final_investigation_result(self):
        if "khalid_guilty" in self.facts and "R15" in self.fired_rules:
            return "Khalid is guilty", "success"
        review = self.resolve_conflicts()
        if review["status"] == "CONFLICT": return "Investigation incomplete: Conflicting evidence was found.", "error"
        elif review["status"] == "REVIEW_REQUIRED": return "Investigation incomplete: Independent review is required.", "warning"
        else: return "Investigation incomplete: Some required facts are missing.", "warning"

# ==========================================
# 2. دوال المؤثرات الصوتية والموسيقى (Student 3)
# ==========================================
def play_sound(url):
    audio_html = f'<audio autoplay="true" style="display:none;"><source src="{url}" type="audio/mp3"></audio>'
    st.markdown(audio_html, unsafe_allow_html=True)

def play_background_music(enabled: bool):
    """تشغيل موسيقى خلفية مستمرة عبر الـ DOM دون انقطاع عند تحديث الصفحة"""
    bg_music_url = "https://otomusu.com/audio/真犯人はあなた.mp3"
    volume = 0.25 if enabled else 0.0
    
    html_code = f"""
        <script>
            (function() {{
                const doc = window.parent.document;
                let audio = doc.getElementById('bg-mystery-music');
                if (!audio) {{
                    audio = doc.createElement('audio');
                    audio.id = 'bg-mystery-music';
                    audio.src = "{bg_music_url}";
                    audio.loop = true;
                    audio.volume = {volume};
                    audio.style.display = 'none';
                    doc.body.appendChild(audio);
                }}
                audio.loop = true;
                audio.volume = {volume};
                if ({str(enabled).lower()}) {{
                    audio.play().catch(() => {{}});
                }} else {{
                    audio.pause();
                }}
            }})();
        </script>
    """
    components.html(html_code, height=0, width=0)

# روابط المؤثرات الصوتية
SOUND_ERROR = "https://actions.google.com/sounds/v1/cartoon/wood_plank_flicks.ogg"
SOUND_SUCCESS = "https://actions.google.com/sounds/v1/crowds/crowd_cheer.ogg"
SOUND_THINKING = "https://actions.google.com/sounds/v1/cartoon/slide_whistle_to_drum_hit.ogg"

# ==========================================
# 3. الواجهة السينمائية والتفاعلية (Student 3)
# ==========================================
st.set_page_config(page_title="The Last Night at the Park", page_icon="🕵️‍♂️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Inter:wght@300;400;600&display=swap');
    .stApp { background: radial-gradient(circle, #2a2a35 0%, #0f1115 100%); color: #e0e0e0; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Cinzel', serif; color: #ff3333; text-shadow: 2px 2px 10px rgba(255, 0, 0, 0.5); }
    .stButton>button { background: linear-gradient(90deg, #8b0000 0%, #ff0000 100%); color: white; border: none; border-radius: 8px; padding: 12px 28px; font-weight: 600; box-shadow: 0 0 20px rgba(255, 0, 0, 0.6); transition: all 0.3s ease-in-out; width: 100%; font-size: 18px; text-transform: uppercase; letter-spacing: 2px; }
    .stButton>button:hover { transform: scale(1.03); box-shadow: 0 0 30px rgba(255, 0, 0, 1); color: #fff; }
    .stCheckbox>label { font-size: 15px; color: #d1d1d1; transition: color 0.2s; cursor: pointer; line-height: 1.4; }
    .stCheckbox>label:hover { color: #ff4b4b; }
    .stSidebar { background-color: #14161a !important; border-right: 2px solid #ff3333; }
    .rule-trace-box { background-color: #12141a; padding: 15px; border-radius: 8px; border: 1px solid #ff3333; font-family: monospace; color: #00ffcc; max-height: 400px; overflow-y: auto; box-shadow: inset 0 0 10px rgba(0,255,204,0.2); }
    .interrogation-box { background-color: #1e2029; padding: 20px; border-left: 5px solid #ffcc00; border-radius: 5px; margin-top: 15px; }
    .case-briefing { background-color: #1a1c23; padding: 20px; border-radius: 8px; border: 1px solid #444; margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.5); }
    .case-briefing h4 { color: #ffcc00; margin-top: 0; }
    .case-briefing p { font-size: 16px; line-height: 1.6; color: #ccc; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("🕵️‍♂️ Detective Dossier")
    st.markdown("---")
    st.markdown("**Victim:** Reem (24) 🩸")
    st.markdown("**Time of Death:** 10:10 - 10:20 PM ⏱️")
    st.markdown("**Location:** Lake Park 🌳")
    st.markdown("---")
    
    st.subheader("🎵 Atmosphere")
    music_toggle = st.checkbox("🔊 Enable Background Music", value=True)
    play_background_music(music_toggle)
    st.markdown("---")
    
    st.subheader("Prime Suspects:")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=200&h=200&fit=crop&crop=faces", caption="Sara (Friend)", use_container_width=True)
    with col2:
        st.image("https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=200&h=200&fit=crop&crop=faces", caption="Khalid (Colleague)", use_container_width=True)
    with col1:
        st.image("https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&h=200&fit=crop&crop=faces", caption="Majed (Security)", use_container_width=True)
    with col2:
        st.image("https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200&h=200&fit=crop&crop=faces", caption="Noura (Sister)", use_container_width=True)

# --- Main Page Header ---
st.markdown("<h1 style='text-align: center;'>🩸 The Last Night at the Park 🩸</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #aaa;'>Case #001: The Murder of Reem</h3>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #ff3333;'>", unsafe_allow_html=True)

# --- Case Briefing ---
st.markdown("""
<div class='case-briefing'>
    <h4>📜 Case Briefing:</h4>
    <p>At <b>10:30 PM</b>, Reem (24) was found dead beside the lake in Lake Park. 
    The investigation places the crime between <b>10:10 PM and 10:20 PM</b>. 
    A nearby security camera stopped recording during this exact interval. 
    Four people are connected to the victim. Your job is to reveal the evidence, question the suspects, and use the Expert System to deduce the killer.</p>
</div>
""", unsafe_allow_html=True)

# --- Tabs for Interaction ---
tab1, tab2, tab3 = st.tabs(["🔎 Crime Scene (Evidence)", "🗣️ Interrogation Room", "⚖️ Final Deduction"])

# TAB 1: Evidence
with tab1:
    st.markdown("### 📋 Evidence Board")
    st.info("Review the discovered evidence from the case file.")
    
    ev_checkboxes = {}
    evidence_data = {
        "E01": "Sara's bracelet was found by the lake.",
        "E02": "Exit record at 9:50 PM and independent confirmation she did not return.",
        "E03": "Financial dispute with Reem.",
        "E04": "Camera places Khalid near the lake at 10:15 PM.",
        "E05": "Footwear impressions match Khalid's shoes.",
        "E06": "Majed has camera-control access.",
        "E07": "Shutdown logged under Majed's account.",
        "E08": "Earlier dispute between Majed and Reem.",
        "E09": "Messages indicate a family disagreement.",
        "E10": "Home video confirms Noura's whereabouts.",
        "E11": "Witness saw Khalid leave at 10:22 PM.",
        "E12": "Majed's print on control box; not proof of tampering.",
        "E13": "Device location independently confirms Khalid's presence.",
        "E14": "Fictional forensic trace on Reem's belongings links to Khalid."
    }
    
    c1, c2 = st.columns(2)
    for i, (key, desc) in enumerate(evidence_data.items()):
        if i < 7:
            with c1: ev_checkboxes[key] = st.checkbox(f"**{key}**: {desc}")
        else:
            with c2: ev_checkboxes[key] = st.checkbox(f"**{key}**: {desc}")

# TAB 2: Interrogation Room
with tab2:
    st.markdown("### 🗣️ Interrogation Room")
    st.write("Click on a suspect to read their statement.")
    
    if st.button("Interrogate Sara"): st.markdown("<div class='interrogation-box'><b>You:</b> When did you leave?<br><b>Sara:</b> At 9:50 PM.<br><br><b>You:</b> Why was your bracelet there?<br><b>Sara:</b> I lost it during an earlier visit.</div>", unsafe_allow_html=True)
    if st.button("Interrogate Khalid"): st.markdown("<div class='interrogation-box'><b>You:</b> Did you argue with Reem?<br><b>Khalid:</b> Yes, about money.<br><br><b>You:</b> Where were you at 10:15?<br><b>Khalid:</b> Walking in the park.<br><br><b>You:</b> Did you go to the lake?<br><b>Khalid:</b> I do not remember going there.</div>", unsafe_allow_html=True)
    if st.button("Interrogate Majed"): st.markdown("<div class='interrogation-box'><b>You:</b> Why did the camera stop?<br><b>Majed:</b> I thought it was a technical fault.<br><br><b>You:</b> Who can control the camera?<br><b>Majed:</b> I manage it; maintenance procedures also exist.</div>", unsafe_allow_html=True)
    if st.button("Interrogate Noura"): st.markdown("<div class='interrogation-box'><b>You:</b> Where were you?<br><b>Noura:</b> At home.<br><br><b>You:</b> Can you prove it?<br><b>Noura:</b> The home camera recorded me.</div>", unsafe_allow_html=True)

# TAB 3: Deduction
with tab3:
    st.markdown("### ⚖️ Independent Review & Deduction")
    no_contradiction = st.checkbox("I confirm there is NO MATERIAL CONTRADICTION verified.")
    solve_btn = st.button("🚨 RUN INFERENCE ENGINE 🚨")
    
    result_container = st.container()
    explanation_container = st.container()

    if solve_btn:
        selected_evidence = [key for key, checked in ev_checkboxes.items() if checked]
        
        if not selected_evidence and not no_contradiction:
            with result_container:
                play_sound(SOUND_ERROR)
                st.error("❌ **Validation Error:** You cannot run the system without selecting any evidence.")
                st.toast("Validation failed!", icon="🚨")
            st.stop()
            
        system = InteractiveExpertSystem()
        for ev in selected_evidence: system.add_evidence(ev)
        if no_contradiction: system.add_confirmed_fact("no_material_contradiction_verified")
            
        with result_container:
            play_sound(SOUND_THINKING)
            with st.spinner("Analyzing forensic data and tracing rules..."):
                time.sleep(1.5)
                system.run_forward_chaining()
                time.sleep(0.5)
                
            result_text, status = system.final_investigation_result()
            
            if status == "success":
                play_sound(SOUND_SUCCESS)
                st.balloons()
                st.success(f"### 🎯 CONCLUSION: {result_text}")
            elif status == "error":
                play_sound(SOUND_ERROR)
                st.error(f"### 🛑 {result_text}")
            else:
                st.warning(f"### ⚠️ {result_text}")
                
        with explanation_container:
            st.markdown("### 🧠 Expert System Reasoning")
            tab_a, tab_b = st.tabs(["📜 Rule Trace Log", "🗂️ Final Facts"])
            
            with tab_a:
                if not system.rule_trace: st.info("No rules fired. Insufficient data.")
                else:
                    st.markdown("<div class='rule-trace-box'>", unsafe_allow_html=True)
                    for step, entry in enumerate(system.rule_trace, 1):
                        st.markdown(f"**[{entry['rule_id']}]** 🔹 *{entry['description']}*")
                        st.markdown(f"👉 Triggered because: `{', '.join(entry['conditions'])}`")
                        st.markdown(f"👉 Conclusion: **{entry['conclusion']}**")
                        st.markdown("---")
                    st.markdown("</div>", unsafe_allow_html=True)
            with tab_b:
                st.json(list(system.facts))