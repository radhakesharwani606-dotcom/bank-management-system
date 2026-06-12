import json
import random
import string
import streamlit as st
from pathlib import Path

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NeoBank",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;700&display=swap');

/* Root overrides */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 680px; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0f1f3d 0%, #1a3a6b 60%, #0f4c81 100%);
    border-radius: 20px;
    padding: 2.5rem 2rem 2rem;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(15,31,61,0.25);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.hero-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: -1px;
    margin: 0;
}
.hero-logo span { color: #4db8ff; }
.hero-sub {
    color: rgba(255,255,255,0.6);
    font-size: 0.85rem;
    margin-top: 0.3rem;
    letter-spacing: 0.5px;
}

/* ── Nav pills ── */
.stRadio > div {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
    background: transparent !important;
}
.stRadio label {
    background: #f0f4ff;
    border: 1.5px solid #dde6f5;
    border-radius: 30px;
    padding: 0.45rem 1.1rem;
    font-size: 0.82rem;
    font-weight: 500;
    color: #3a4a6b;
    cursor: pointer;
    transition: all 0.18s;
}
.stRadio label:hover { background: #dde6ff; border-color: #7aa3e5; }
[data-testid="stRadio"] > div > label[data-checked="true"] {
    background: #0f1f3d;
    color: #fff;
    border-color: #0f1f3d;
}

/* ── Cards ── */
.card {
    background: #fff;
    border-radius: 16px;
    padding: 1.8rem 1.6rem;
    border: 1px solid #e8edf7;
    box-shadow: 0 2px 16px rgba(15,31,61,0.07);
    margin-top: 1.2rem;
}
.card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #0f1f3d;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    border-radius: 10px !important;
    border: 1.5px solid #dde6f5 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 0.9rem !important;
    color: #1a2a4a !important;
    background: #f8faff !important;
    transition: border 0.15s;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #4a82d9 !important;
    box-shadow: 0 0 0 3px rgba(74,130,217,0.12) !important;
}

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    background: linear-gradient(135deg, #1a3a6b, #0f4c81) !important;
    color: #fff !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1.4rem !important;
    letter-spacing: 0.3px !important;
    transition: opacity 0.15s, transform 0.1s !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.88; transform: translateY(-1px); }
.stButton > button:active { transform: translateY(0); }

/* ── Balance badge ── */
.balance-badge {
    background: linear-gradient(135deg, #e6f0ff, #d4e6ff);
    border: 1px solid #b3d0f5;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
    margin: 1rem 0;
}
.balance-amount {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #0f1f3d;
}
.balance-label { font-size: 0.75rem; color: #5a7ab5; letter-spacing: 1px; text-transform: uppercase; }

/* ── Info rows ── */
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid #f0f4ff;
    font-size: 0.88rem;
}
.info-row:last-child { border-bottom: none; }
.info-key { color: #7a90b8; font-weight: 500; }
.info-val { color: #1a2a4a; font-weight: 600; font-family: 'Space Grotesk', sans-serif; }

/* ── Account number pill ── */
.accno-pill {
    background: #0f1f3d;
    color: #4db8ff;
    font-family: 'Space Grotesk', monospace;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 2px;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    display: inline-block;
    margin: 0.5rem 0;
}

/* ── Alerts ── */
.alert-success {
    background: #eafaf1;
    border-left: 4px solid #2ecc71;
    padding: 0.8rem 1rem;
    border-radius: 0 10px 10px 0;
    color: #1a7a45;
    font-size: 0.88rem;
    margin-top: 0.8rem;
}
.alert-error {
    background: #fdf0f0;
    border-left: 4px solid #e74c3c;
    padding: 0.8rem 1rem;
    border-radius: 0 10px 10px 0;
    color: #922b21;
    font-size: 0.88rem;
    margin-top: 0.8rem;
}
.stDivider { margin: 1rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Database helpers ──────────────────────────────────────────────────────────
DB = "data.json"

def load_data():
    if Path(DB).exists():
        with open(DB) as f:
            return json.loads(f.read())
    return []

def save_data(data):
    with open(DB, "w") as f:
        f.write(json.dumps(data, indent=2))

def generate_account_no():
    alpha = random.choices(string.ascii_uppercase, k=3)
    num   = random.choices(string.digits, k=4)
    parts = alpha + num
    random.shuffle(parts)
    return "".join(parts)

def find_user(data, acc_no, pin):
    for u in data:
        # handle both old key "accountNo." and new key "accountNo"
        acc = u.get("accountNo") or u.get("accountNo.")
        if acc == acc_no and u["pin"] == pin:
            return u
    return None

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="hero-logo">Neo<span>Bank</span></p>
    <p class="hero-sub">Simple · Secure · Smart Banking</p>
</div>
""", unsafe_allow_html=True)

# ── Navigation ────────────────────────────────────────────────────────────────
nav = st.radio(
    "",
    ["🆕 Open Account", "💰 Deposit", "🏧 Withdraw", "📋 My Account", "✏️ Update Info", "🗑️ Close Account"],
    horizontal=True,
    label_visibility="collapsed",
)

data = load_data()

# ── Shared auth block ─────────────────────────────────────────────────────────
def auth_fields():
    c1, c2 = st.columns(2)
    with c1:
        acc = st.text_input("Account Number", placeholder="e.g. AB1234")
    with c2:
        pin = st.number_input("4-digit PIN", min_value=0, max_value=9999, step=1, value=None, placeholder="••••")
    return acc.strip(), int(pin) if pin is not None else None

# ═══════════════════════════════════════════════════════════════════════════════
# 1. OPEN ACCOUNT
# ═══════════════════════════════════════════════════════════════════════════════
if nav == "🆕 Open Account":
    st.markdown('<div class="card"><div class="card-title">🆕 Open a New Account</div>', unsafe_allow_html=True)

    name  = st.text_input("Full Name", placeholder="Radha Sharma")
    age   = st.number_input("Age", min_value=1, max_value=120, step=1, value=None, placeholder="18+")
    email = st.text_input("Email Address", placeholder="you@email.com")
    pin   = st.number_input("Choose a 4-digit PIN", min_value=1000, max_value=9999, step=1, value=None, placeholder="Must be 4 digits")

    if st.button("Create Account →"):
        if not name or age is None or not email or pin is None:
            st.markdown('<div class="alert-error">⚠️ Please fill in all fields.</div>', unsafe_allow_html=True)
        elif age < 18:
            st.markdown('<div class="alert-error">❌ You must be 18 or older to open an account.</div>', unsafe_allow_html=True)
        elif len(str(pin)) != 4:
            st.markdown('<div class="alert-error">❌ PIN must be exactly 4 digits.</div>', unsafe_allow_html=True)
        else:
            acc_no = generate_account_no()
            new_user = {"name": name, "age": int(age), "email": email,
                        "pin": int(pin), "accountNo": acc_no, "balance": 0}
            data.append(new_user)
            save_data(data)
            st.markdown(f"""
            <div class="alert-success">
                ✅ Account created! Welcome, <strong>{name}</strong>.<br>
                Your account number: <span class="accno-pill">{acc_no}</span><br>
                <small>📌 Save this — you'll need it to log in.</small>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 2. DEPOSIT
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "💰 Deposit":
    st.markdown('<div class="card"><div class="card-title">💰 Deposit Money</div>', unsafe_allow_html=True)
    acc, pin = auth_fields()
    amount = st.number_input("Amount to Deposit (₹)", min_value=1, max_value=10000, step=100, value=None, placeholder="Max ₹10,000 per transaction")

    if st.button("Deposit →"):
        if not acc or pin is None or amount is None:
            st.markdown('<div class="alert-error">⚠️ Please fill all fields.</div>', unsafe_allow_html=True)
        else:
            user = find_user(data, acc, pin)
            if not user:
                st.markdown('<div class="alert-error">❌ Invalid account number or PIN.</div>', unsafe_allow_html=True)
            elif amount <= 0 or amount > 10000:
                st.markdown('<div class="alert-error">❌ Deposit must be between ₹1 and ₹10,000.</div>', unsafe_allow_html=True)
            else:
                user["balance"] += amount
                save_data(data)
                st.markdown(f"""
                <div class="alert-success">
                    ✅ ₹{amount:,} deposited successfully!<br>
                    <strong>New Balance: ₹{user['balance']:,}</strong>
                </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 3. WITHDRAW
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "🏧 Withdraw":
    st.markdown('<div class="card"><div class="card-title">🏧 Withdraw Money</div>', unsafe_allow_html=True)
    acc, pin = auth_fields()
    amount = st.number_input("Amount to Withdraw (₹)", min_value=1, step=100, value=None, placeholder="Enter amount")

    if st.button("Withdraw →"):
        if not acc or pin is None or amount is None:
            st.markdown('<div class="alert-error">⚠️ Please fill all fields.</div>', unsafe_allow_html=True)
        else:
            user = find_user(data, acc, pin)
            if not user:
                st.markdown('<div class="alert-error">❌ Invalid account number or PIN.</div>', unsafe_allow_html=True)
            elif amount > user["balance"]:
                st.markdown(f'<div class="alert-error">❌ Insufficient balance. Available: ₹{user["balance"]:,}</div>', unsafe_allow_html=True)
            else:
                user["balance"] -= amount
                save_data(data)
                st.markdown(f"""
                <div class="alert-success">
                    ✅ ₹{amount:,} withdrawn successfully!<br>
                    <strong>Remaining Balance: ₹{user['balance']:,}</strong>
                </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 4. MY ACCOUNT
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "📋 My Account":
    st.markdown('<div class="card"><div class="card-title">📋 Account Details</div>', unsafe_allow_html=True)
    acc, pin = auth_fields()

    if st.button("View Details →"):
        if not acc or pin is None:
            st.markdown('<div class="alert-error">⚠️ Please enter your credentials.</div>', unsafe_allow_html=True)
        else:
            user = find_user(data, acc, pin)
            if not user:
                st.markdown('<div class="alert-error">❌ Invalid account number or PIN.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="balance-badge">
                    <div class="balance-label">Current Balance</div>
                    <div class="balance-amount">₹{user['balance']:,}</div>
                </div>
                <div class="info-row"><span class="info-key">Name</span><span class="info-val">{user['name']}</span></div>
                <div class="info-row"><span class="info-key">Email</span><span class="info-val">{user['email']}</span></div>
                <div class="info-row"><span class="info-key">Age</span><span class="info-val">{user['age']}</span></div>
                <div class="info-row"><span class="info-key">Account No.</span><span class="info-val">{user['accountNo']}</span></div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 5. UPDATE INFO
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "✏️ Update Info":
    st.markdown('<div class="card"><div class="card-title">✏️ Update Account Info</div>', unsafe_allow_html=True)
    acc, pin = auth_fields()

    if "update_user" not in st.session_state:
        st.session_state.update_user = None

    if st.button("Load My Details"):
        if not acc or pin is None:
            st.markdown('<div class="alert-error">⚠️ Please enter your credentials.</div>', unsafe_allow_html=True)
        else:
            user = find_user(data, acc, pin)
            if not user:
                st.markdown('<div class="alert-error">❌ Invalid account number or PIN.</div>', unsafe_allow_html=True)
            else:
                st.session_state.update_user = user
                st.session_state.update_acc  = acc
                st.session_state.update_pin  = pin

    if st.session_state.update_user:
        u = st.session_state.update_user
        st.divider()
        new_name  = st.text_input("Name",  value=u["name"])
        new_email = st.text_input("Email", value=u["email"])
        new_pin_str = st.text_input("New PIN (leave blank to keep)", placeholder="4-digit PIN", max_chars=4)

        if st.button("Save Changes →"):
            u["name"]  = new_name  if new_name  else u["name"]
            u["email"] = new_email if new_email else u["email"]
            if new_pin_str:
                if len(new_pin_str) == 4 and new_pin_str.isdigit():
                    u["pin"] = int(new_pin_str)
                else:
                    st.markdown('<div class="alert-error">❌ PIN must be exactly 4 digits.</div>', unsafe_allow_html=True)
                    st.stop()
            save_data(data)
            st.session_state.update_user = None
            st.markdown('<div class="alert-success">✅ Details updated successfully!</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 6. CLOSE ACCOUNT
# ═══════════════════════════════════════════════════════════════════════════════
elif nav == "🗑️ Close Account":
    st.markdown('<div class="card"><div class="card-title">🗑️ Close Account</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#c0392b;font-size:0.85rem;margin-bottom:1rem;">⚠️ This action is permanent and cannot be undone.</p>', unsafe_allow_html=True)
    acc, pin = auth_fields()
    confirm = st.checkbox("Yes, I understand this will permanently delete my account.")

    if st.button("Close Account →"):
        if not acc or pin is None:
            st.markdown('<div class="alert-error">⚠️ Please enter your credentials.</div>', unsafe_allow_html=True)
        elif not confirm:
            st.markdown('<div class="alert-error">⚠️ Please confirm by checking the box above.</div>', unsafe_allow_html=True)
        else:
            user = find_user(data, acc, pin)
            if not user:
                st.markdown('<div class="alert-error">❌ Invalid account number or PIN.</div>', unsafe_allow_html=True)
            else:
                data.remove(user)
                save_data(data)
                st.markdown('<div class="alert-success">✅ Your account has been closed. We\'re sorry to see you go.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:2.5rem;color:#b0bcd0;font-size:0.75rem;letter-spacing:0.5px;">
    🏦 NeoBank · Built with Python & Streamlit
</div>
""", unsafe_allow_html=True)
