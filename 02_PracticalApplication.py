"""
Probability Tree Visualizer - Streamlit Implementation
"""

import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

# ----------------------------------------------------------------------
# Page Config
# ----------------------------------------------------------------------
st.set_page_config(page_title="Probability Tree Visualizer", layout="wide")

# ----------------------------------------------------------------------
# 1. Probability Tree Logic
# ----------------------------------------------------------------------
def compute_tree(p_A, p_B_given_A, p_B_given_notA):

    p_notA = 1 - p_A   
    p_A_and_B = p_A * p_B_given_A 
    p_A_and_notB = p_A * (1 - p_B_given_A) 
    p_notA_and_B = p_notA * p_B_given_notA 
    p_notA_and_notB = p_notA * (1 - p_B_given_notA) 

    p_B = p_A_and_B + p_notA_and_B 
    p_notB = 1 - p_B 

    independent = np.isclose(p_A_and_B, p_A * p_B, atol=1e-6) 

    return {
        'p_A': p_A,
        'p_notA': p_notA,
        'p_B_given_A': p_B_given_A,
        'p_B_given_notA': p_B_given_notA,
        'p_A_and_B': p_A_and_B,
        'p_A_and_notB': p_A_and_notB,
        'p_notA_and_B': p_notA_and_B,
        'p_notA_and_notB': p_notA_and_notB,
        'p_B': p_B,
        'p_notB': p_notB,
        'independent': independent
    }

# ----------------------------------------------------------------------
# 2.  Tree Drawing Function
# ----------------------------------------------------------------------
def draw_tree(probs, figsize=(16, 10)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("#FFFFFF")

    ax.set_xlim(-9.0, 10.0)   
    ax.set_ylim(-10.5, 3.0) 
    ax.set_aspect('equal')
    ax.axis('off')

    # ---- Node positions ----
    root = (0, 0)
    pos_A = (-3.5, -2.8)
    pos_notA = (3.5, -2.8)
    pos_A_B = (-5.2, -5.6)
    pos_A_notB = (-1.8, -5.6)
    pos_notA_B = (1.8, -5.6)
    pos_notA_notB = (5.2, -5.6)

    labels = {
        root: 'Start',
        pos_A: 'A', 
        pos_notA: 'Not A',
        pos_A_B: 'B',
        pos_A_notB: 'Not B',
        pos_notA_B: 'B',
        pos_notA_notB: 'Not B'
    }

    edge_probs = {
        (root, pos_A): f'{probs["p_A"]:.2f}',
        (root, pos_notA): f'{probs["p_notA"]:.2f}',
        (pos_A, pos_A_B): f'{probs["p_B_given_A"]:.2f}',
        (pos_A, pos_A_notB): f'{1 - probs["p_B_given_A"]:.2f}',
        (pos_notA, pos_notA_B): f'{probs["p_B_given_notA"]:.2f}',
        (pos_notA, pos_notA_notB): f'{1 - probs["p_B_given_notA"]:.2f}'
    }

    leaf_probs = {
        pos_A_B: fr'$P(A \cap B) = {probs["p_A_and_B"]:.3f}$',
        pos_A_notB: fr'$P(A \cap \neg B) = {probs["p_A_and_notB"]:.3f}$',
        pos_notA_B: fr'$P(\neg A \cap B) = {probs["p_notA_and_B"]:.3f}$',
        pos_notA_notB: fr'$P(\neg A \cap \neg B) = {probs["p_notA_and_notB"]:.3f}$'
    }

    # ----- Draw edges -----
    for (start, end), prob in edge_probs.items(): 
        x1, y1 = start 
        x2, y2 = end
        # Softer slate gray edges
        ax.plot([x1, x2], [y1, y2], color='#94A3B8', lw=2.5, alpha=0.8, zorder=1)

        mx, my = (x1 + x2) / 2, (y1 + y2) / 2 
        dx, dy = x2 - x1, y2 - y1
        norm = np.sqrt(dx**2 + dy**2)
        if norm > 0:
            offset_x = -dy / norm * 0.3
            offset_y = dx / norm * 0.3
        else:
            offset_x, offset_y = 0, 0

        # Modern minimalist edge text box
        bbox_props = dict(boxstyle="round,pad=0.3", facecolor='#FFFFFF',
                          edgecolor='#E2E8F0', lw=1.5, alpha=0.95)
        ax.text(mx + offset_x, my + offset_y, prob,
                fontsize=11, ha='center', va='center', color='#475569',
                fontweight='semibold', bbox=bbox_props, zorder=3)

    # ----- Draw nodes -----
    for node, label in labels.items():
        x, y = node
        # Modern Indigo nodes with thicker crisp border
        circle = plt.Circle((x, y), 0.5, facecolor='#6366F1',
                            edgecolor='#FFFFFF', lw=2.5, zorder=2)
        ax.add_patch(circle)
        ax.text(x, y, label, fontsize=13, ha='center', va='center',
                color='#FFFFFF', fontweight='bold', zorder=3)

    # ----- Draw leaf boxes -----
    for leaf, prob_text in leaf_probs.items():
        x, y = leaf
        y_shifted = y - 1.2
        
        # Clean slate data-card look
        rect = FancyBboxPatch((x - 1.2, y_shifted - 0.35), 2.4, 0.7,
                              boxstyle="round,pad=0.15",
                              facecolor='#F8FAFC', edgecolor='#CBD5E1',
                              lw=1.5, zorder=2)
        ax.add_patch(rect)
        ax.text(x, y_shifted, prob_text, fontsize=11, ha='center',
                va='center', color='#1E293B', fontweight='medium', zorder=3)

    # ----- Title -----
    ax.text(0, 1.7, 'Probability Tree Visualizer', fontsize=24, ha='center',
            va='center', fontweight='bold', color='#0F172A')

    # ----- Metrics Panel -----
    metrics_x = 7.5
    metrics_y_start = 0.8

    panel = FancyBboxPatch((metrics_x - 2.0, metrics_y_start - 5.2),
                           4.0, 6.0,
                           boxstyle="round,pad=0.4",
                           facecolor='#FFFFFF', edgecolor='#E2E8F0',
                           lw=1.5, alpha=0.95, zorder=0)
    ax.add_patch(panel)

    ax.text(metrics_x, metrics_y_start + 0.3, 'Metrics', fontsize=17,
            ha='center', va='center', fontweight='bold', color='#0F172A')

    metrics = [
        (f'P(A)', f'{probs["p_A"]:.3f}'),
        (f'P(B|A)', f'{probs["p_B_given_A"]:.3f}'),
        (f'P(B|¬A)', f'{probs["p_B_given_notA"]:.3f}'),
        (f'P(B)', f'{probs["p_B"]:.3f}'),
        (f'Independent', 'Yes' if probs['independent'] else 'No'),
    ]

    y_offset = metrics_y_start - 0.8
    for label, value in metrics:
        ax.text(metrics_x - 1.5, y_offset, label, fontsize=13,
                ha='left', va='center', color='#475569', fontweight='semibold')
        
        # Soft modern Emerald and Rose colors
        color = '#059669' if (label == 'Independent' and value == 'Yes') else \
                '#E11D48' if (label == 'Independent' and value == 'No') else '#0F172A'
        ax.text(metrics_x + 1.5, y_offset, value, fontsize=14,
                ha='right', va='center', color=color, fontweight='bold')
        y_offset -= 0.9

    # ----- Outcomes section -----
    outcome_label_y = -8.2
    ax.text(0, outcome_label_y, 'Outcomes', fontsize=16, ha='center',
            va='center', fontweight='bold', color='#0F172A')

    outcome_texts = [
        fr'$P(A \cap B): {probs["p_A_and_B"]:.3f}$',
        fr'$P(A \cap \neg B): {probs["p_A_and_notB"]:.3f}$',
        fr'$P(\neg A \cap B): {probs["p_notA_and_B"]:.3f}$',
        fr'$P(\neg A \cap \neg B): {probs["p_notA_and_notB"]:.3f}$',
    ]

    x_positions = [-4.5, -1.5, 1.5, 4.5]
    box_center_y = outcome_label_y - 0.8 

    for x_pos, text in zip(x_positions, outcome_texts):
        # Emerald accent style for final outcomes
        rect = FancyBboxPatch((x_pos - 1.2, box_center_y - 0.275), 2.4, 0.55,
                              boxstyle="round,pad=0.15",
                              facecolor='#F0FDF4', edgecolor='#BBF7D0',
                              lw=1.5, zorder=2)
        ax.add_patch(rect)
        ax.text(x_pos, box_center_y, text, fontsize=11, ha='center',
                va='center', color='#14532D', fontweight='medium', zorder=3)

    return fig

# ----------------------------------------------------------------------
# 3. Streamlit UI & Interactivity
# ----------------------------------------------------------------------

st.info("**Probability Tree Visualizer:** Adjust the sliders in the sidebar to change branch probabilities. The tree, metrics, and outcomes update in real-time.")

st.sidebar.header("Adjust Probabilities")
p_A = st.sidebar.slider("P(A):", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
p_B_given_A = st.sidebar.slider("P(B|A):", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
p_B_given_notA = st.sidebar.slider("P(B|¬A):", min_value=0.0, max_value=1.0, value=0.5, step=0.01)

st.sidebar.markdown("---")
st.sidebar.subheader("Legends & Definitions")
st.sidebar.markdown("""
* **$P(A)$**: The baseline probability of Event A occurring.
* **$P(B|A)$**: The conditional probability of Event B occurring, given that Event A has already occurred.
* **$P(B|\\neg A)$**: The conditional probability of Event B occurring, given that Event A did *not* occur.
* **$P(A \\cap B)$**: The joint probability of both Event A and Event B occurring together (Intersection).
* **Independent**: Events A and B are independent if the outcome of Event A does not affect the probability of Event B happening. Mathematically, this is true when $P(A \\cap B) = P(A) \\times P(B)$.
""")

probs = compute_tree(p_A, p_B_given_A, p_B_given_notA)

fig = draw_tree(probs)
st.pyplot(fig)

# ----------------------------------------------------------------------
# 4. Example Scenarios (Optional Expander)
# ----------------------------------------------------------------------
with st.expander("View Example Scenarios"):
    st.markdown("""
    **🔹 Scenario 1: Independent Events**
    * P(A) = 0.5, P(B|A) = 0.5, P(B|¬A) = 0.5
    * Setting the sliders to these values will show the Independent metric as Yes.
    
    **🔹 Scenario 2: Dependent Events**
    * P(A) = 0.4, P(B|A) = 0.8, P(B|¬A) = 0.2
    
    **🔹 Scenario 3: B depends strongly on A**
    * P(A) = 0.6, P(B|A) = 0.1, P(B|¬A) = 0.9
    """)

# ----------------------------------------------------------------------
# 5. Case Study: Diagnosing the Pipeline
# ----------------------------------------------------------------------
with st.expander("Case Study: Diagnosing a Consultant's Pipeline"):
    st.markdown("""
    ### The Problem
    Sarah is a Cord Blood & Genetics Consultant needing 10 enrollments per month. She receives 50 referrals monthly but only closes 5. She believes her leads are low quality. We can use the Multiplication Law of Probability to diagnose the structural bottleneck in her pipeline.
    
    ### The Scenario (Dependent Events)
    A client cannot enroll without first attending a consultation. 
    *   **Event A:** The client attends the consultation. Sarah's current rate is 50%.
    *   **Event B:** The client enrolls. If they attend, Sarah's close rate is 20%. If they do not attend, the close rate is 0%.
    
    ### Using the Visualizer
    **1. Set the Baseline:** Adjust the sidebar sliders to match Sarah's current performance:
    *   `P(A) = 0.50`
    *   `P(B|A) = 0.20`
    *   `P(B|¬A) = 0.00`
    
    Look at the **Outcomes** panel for **$P(A \\cap B)$**. It reads **0.100** (10%). Multiplying her 50 referrals by a 10% total conversion rate mathematically explains why she is stuck at 5 enrollments.
    
    **2. Simulate the Solution:** Sarah needs 10 enrollments from 50 leads, meaning her target $P(A \\cap B)$ is **0.200**. 
    Leave `P(A)` at 0.50. Slowly slide `P(B|A)` upward until $P(A \\cap B)$ hits 0.200. 
    
    **The Insight:** The math proves Sarah doesn't need *more* leads; she needs to improve her consultative selling skills to push her consultation close rate to 40%.
    """)

    # ----------------------------------------------------------------------
# 6. The Answer & Structural Takeaway
# ----------------------------------------------------------------------
with st.expander(" The Answer & Structural Takeaway"):
    st.markdown("""
    ### The Math Basis
    The Multiplication Law of Probability dictates that in a dependent sequence, the probability of the final outcome is the product of its individual steps: 
    $$P(A \\cap B) = P(A) \\times P(B|A)$$

    ### Conclusion
    When diagnosing performance, it is common to blame external factors like "bad referrals" for a missed quota. By mapping the sales funnel to a probability tree, we remove the emotion and isolate the exact mechanical bottleneck.

    The visualizer proves that to double total enrollments from 5 to 10 (achieving a target $P(A \\cap B)$ of 0.20), the consultant has two mathematical options:
    1. **Increase $P(A)$ to 1.0:** Force 100% of doctor referrals to attend a consultation. (Functionally impossible).
    2. **Increase $P(B|A)$ to 0.40:** Improve consultative sales skills to close 4 out of 10 meetings instead of 2 out of 10. (Highly achievable).

    **The Answer:** The pipeline problem is not lead generation; it is lead *conversion*. The consultant must focus their professional development entirely on improving clinical explanations and ethical sales techniques during the consultation phase.
    """)

    # ----------------------------------------------------------------------
# 7. Disclaimer
# ----------------------------------------------------------------------
st.markdown("---")
st.caption("""
⚠️ **Disclaimer:** The Cord Blood & Genetics Consultant case study, including all stated conversion rates and metrics, is a purely hypothetical scenario. It is designed exclusively as a mathematical model to illustrate the Multiplication Law of Probability in a clinical sales context. It does not represent actual performance data, specific company metrics, or guaranteed outcomes.
""")