# Streamlit Phone-Style Matrix, Determinant & Trigonometry Calculator
# Save this file as app.py and run: streamlit run app.py

import streamlit as st
import numpy as np
import math

st.set_page_config(page_title="PocketCalc — Matrix & Trig", layout="centered")

# --- Styles (phone-like card) ---
st.markdown(
    """
    <style>
    .phone-card {
        max-width: 420px;
        margin: 20px auto;
        background: linear-gradient(180deg, #111827 0%, #1f2937 100%);
        border-radius: 28px;
        padding: 18px;
        box-shadow: 0 12px 30px rgba(2,6,23,0.5);
        border: 1px solid rgba(255,255,255,0.05);
        font-family: 'Segoe UI', Roboto, Arial, sans-serif;
        color:#f9fafb;
    }
    .phone-header {
        display:flex;align-items:center;justify-content:space-between;margin-bottom:12px
    }
    .dot {width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:6px}
    .dot.red{background:#ff5f56}
    .dot.yellow{background:#ffbd2e}
    .dot.green{background:#27c93f}
    .section-title{font-weight:700;font-size:18px;margin:6px 0}
    .muted{color:#9ca3af;font-size:13px}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Custom Result Box ---
def show_result(label, value, color="#10b981"):
    """Custom styled result box with better alignment"""
    st.markdown(f"""
        <div style="
            background:#1f2937;
            color:{color};
            padding:14px 16px;
            border-radius:10px;
            margin:10px 0;
            font-family:Consolas, monospace;
            font-size:15px;
            line-height:1.6;
        ">
            <div style="font-weight:bold; margin-bottom:6px; color:#f9fafb">{label}</div>
            <pre style="margin:0; white-space:pre-wrap; word-wrap:break-word;">{value}</pre>
        </div>
    """, unsafe_allow_html=True)

def parse_matrix(text):
    try:
        rows = [row.strip() for row in text.strip().splitlines() if row.strip()]
        mat = [[float(x) for x in row.replace(',', ' ').split()] for row in rows]
        widths = [len(r) for r in mat]
        if len(set(widths)) != 1:
            raise ValueError("Rows have unequal length")
        return np.array(mat)
    except Exception:
        raise ValueError("Invalid format. Use rows separated by newlines, numbers separated by space.")

def pretty_matrix(a):
    return '\n'.join('  '.join(f"{x:.4g}" for x in row) for row in a)

with st.container():
    st.markdown('<div class="phone-card">', unsafe_allow_html=True)

    # Header
    st.markdown(
        '<div class="phone-header"><div style="display:flex;align-items:center"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></div><div style="font-weight:700">PocketCalc</div><div class="muted">v1.2</div></div>',
        unsafe_allow_html=True,
    )

    # --- MATRIX SECTION ---
    st.markdown('<div class="section-title">Matrix Operations</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Matrix Ops", "Determinant & Inverse"])

    # Matrix Ops Tab
    with tab1:
        st.markdown('<div class="muted">Enter matrices A and B for operations.</div>', unsafe_allow_html=True)
        colA, colB = st.columns(2)
        with colA:
            matA_text = st.text_area("Matrix A", value="1 2\n3 4", height=150)
        with colB:
            matB_text = st.text_area("Matrix B", value="5 6\n7 8", height=150)

        op = st.selectbox("Operation", ["Add", "Subtract", "Multiply (A @ B)", "Element-wise Multiply", "Transpose A", "Rank A"])
        if st.button("Compute Matrix Operation"):
            try:
                A = parse_matrix(matA_text)
                R = None
                if op in ("Add", "Subtract", "Multiply (A @ B)", "Element-wise Multiply"):
                    B = parse_matrix(matB_text)
                if op == "Add":
                    R = A + B
                elif op == "Subtract":
                    R = A - B
                elif op == "Multiply (A @ B)":
                    R = A.dot(B)
                elif op == "Element-wise Multiply":
                    R = A * B
                elif op == "Transpose A":
                    R = A.T
                elif op == "Rank A":
                    show_result("Rank(A)", np.linalg.matrix_rank(A))
                if R is not None:
                    show_result("Result", pretty_matrix(R))
            except Exception as e:
                st.error(f"Error: {e}")

    # Determinant & Inverse Tab
    with tab2:
        mat_text = st.text_area("Matrix", value="2 1\n5 3", height=180)
        if st.button("Compute Determinant & Inverse"):
            try:
                M = parse_matrix(mat_text)
                if M.shape[0] != M.shape[1]:
                    raise ValueError("Matrix must be square")
                det = float(np.linalg.det(M))
                show_result("Determinant", round(det, 10))
                if abs(det) < 1e-12:
                    st.warning("Matrix is singular. No inverse.")
                else:
                    inv = np.linalg.inv(M)
                    show_result("Inverse", pretty_matrix(inv))
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown('<hr/>', unsafe_allow_html=True)

    # --- TRIG SECTION ---
    st.markdown('<div class="section-title">Trigonometry</div>', unsafe_allow_html=True)

    trig_tab1, trig_tab2 = st.tabs(["Single Function", "Expression"])

    with trig_tab1:
        func = st.selectbox("Function", ["sin","cos","tan","asin","acos","atan","sinh","cosh","tanh"], key="sf")
        angle_unit = st.selectbox("Units", ["Degrees","Radians"], key="units")
        angle = st.text_input("Angle", value="30")
        if st.button("Compute Trig", key="sf_btn"):
            try:
                x = float(angle)
                if angle_unit == "Degrees":
                    x = math.radians(x)
                res = getattr(math, func)(x)
                show_result(func, res, color="#3b82f6")
            except Exception as e:
                st.error(f"Error: {e}")

    with trig_tab2:
        expr = st.text_input("Expression", value="sin(pi/6) + cos(pi/3)")
        if st.button("Evaluate Expression", key="exp_btn"):
            safe_dict = {k: getattr(math, k) for k in ['sin','cos','tan','asin','acos','atan','sinh','cosh','tanh','sqrt','log','exp','pi','e']}
            try:
                if "__" in expr:
                    raise ValueError("Invalid expression")
                result = eval(expr, {"__builtins__":None}, safe_dict)
                show_result("Expression Result", result, color="#f59e0b")
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# End of app
