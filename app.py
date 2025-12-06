import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io
from ai_heuristics import AIHeuristicEngine, generate_playbook_pdf

# Page config
st.set_page_config(
    page_title="Cyber-Resilience Fallback Assistant",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚨 Cyber-Resilience Fallback Assistant")
st.markdown("**Smart Warehouse Incident Response Tool** | AI-Powered Decision Support")
st.markdown("---")

# Sidebar: Warehouse Profile
st.sidebar.header("🏭 Warehouse Profile")
warehouse_name = st.sidebar.text_input("Warehouse Name", "DC-Alpha")
staff_total = st.sidebar.slider("Total Staff Available", 10, 150, 50)
amr_count = st.sidebar.slider("AMR Fleet", 0, 50, 20)
avg_order_value = st.sidebar.slider("Avg Order Value ($)", 50, 1000, 250)

# Main content tabs
tab1, tab2, tab3 = st.tabs(["📊 Generate Plan", "📈 Results Comparison", "📋 Playbooks"])

with tab1:
    st.header("Generate Incident Response Plan")
    
    # Incident inputs
    col1, col2 = st.columns(2)
    with col1:
        incident_type = st.selectbox(
            "Incident Type", 
            ["WMS Outage", "Automation Down", "IoT Offline", "Extended Outage", "Partial Degradation"]
        )
        orders_waiting = st.slider("Orders Waiting", 20, 800, 120)
        vip_orders_pct = st.slider("VIP Orders (%)", 0, 40, 10)
    
    with col2:
        staff_available = st.slider("Staff On Shift", 10, staff_total, 40)
        sla_critical_pct = st.slider("SLA Critical Orders (%)", 0, 50, 15)
        estimated_duration = st.slider("Expected Duration (hours)", 2, 72, 12)
    
    if st.button("🧠 **GENERATE FALBACK PLAN**", type="primary", use_container_width=True):
        with st.spinner("AI analyzing incident scenario..."):
            # Generate plan using AI heuristics
            plan = AIHeuristicEngine.generate_fallback_plan(
                incident_type=incident_type,
                staff_available=staff_available,
                orders_waiting=orders_waiting,
                vip_pct=vip_orders_pct,
                sla_critical_pct=sla_critical_pct,
                duration_hours=estimated_duration,
                warehouse_name=warehouse_name
            )
        
        # Results section
        st.success(f"✅ **Plan Generated for {warehouse_name}** | {datetime.now().strftime('%H:%M:%S')}")
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Process Now", f"{plan['priority_orders']}/{orders_waiting}", f"+{plan['throughput_improvement']}%")
        col2.metric("Staff Efficiency", f"{plan['utilization']:.0%}", f"{staff_available} staff")
        col3.metric("Est. Delay", f"+{plan['delay_hours']:.1f}h")
        col4.metric("Cost Savings", f"${plan['cost_savings']:,.0f}", f"{plan['cost_reduction']}%")
        
        # Staff allocation table
        st.subheader("👥 **Staff Allocation**")
        allocation_df = pd.DataFrame(plan['staff_allocation'])
        st.dataframe(allocation_df, use_container_width=True)
        
        # Immediate actions
        st.subheader("✅ **IMMEDIATE ACTIONS (Next 2 Hours)**")
        for i, action in enumerate(plan['immediate_actions'], 1):
            st.success(f"{i}. {action}")
        
        # Download buttons
        col1, col2 = st.columns(2)
        with col1:
            pdf_buffer = generate_playbook_pdf(plan)
            st.download_button(
                "📄 Download Playbook (PDF)",
                data=pdf_buffer,
                file_name=f"{warehouse_name}_{incident_type.replace(' ', '_')}_Playbook.pdf",
                mime="application/pdf"
            )
        with col2:
            csv_buffer = io.StringIO()
            allocation_df.to_csv(csv_buffer, index=False)
            st.download_button(
                "📊 Download Staff Roster (CSV)",
                data=csv_buffer.getvalue(),
                file_name=f"{warehouse_name}_Staff_Allocation.csv",
                mime="text/csv"
            )

with tab2:
    st.header("📈 Scenario Comparison")
    st.markdown("**Reactive vs AI-Guided Response**")
    
    # Sample results from your simulation
    comparison_data = {
        'Scenario': ['WMS Outage (12h)', 'Automation Down (6h)', 'Extended (48h)', 'Partial Degradation'],
        'Reactive Throughput': [1.8, 2.1, 1.2, 2.5],
        'AI Throughput': [3.2, 3.4, 2.8, 3.8],
        'Improvement (%)': [78, 62, 133, 52],
        'Cost Savings (%)': [51, 52, 52, 45]
    }
    df_comparison = pd.DataFrame(comparison_data)
    
    # Chart 1: Throughput comparison
    fig1 = px.bar(df_comparison, x='Scenario', y=['Reactive Throughput', 'AI Throughput'],
                  barmode='group', title="Throughput: Reactive vs AI-Guided",
                  color_discrete_map={'Reactive Throughput': '#ef4444', 'AI Throughput': '#10b981'})
    st.plotly_chart(fig1, use_container_width=True)
    
    # Chart 2: Improvement metrics
    fig2 = px.bar(df_comparison.melt(id_vars='Scenario'), 
                  x='Scenario', y='value', color='variable',
                  title="Performance Improvement", barmode='group')
    st.plotly_chart(fig2, use_container_width=True)
    
    st.dataframe(df_comparison, use_container_width=True)

with tab3:
    st.header("📋 Pre-Generated Playbooks")
    playbook_type = st.selectbox("Select Playbook", 
                                ["WMS Outage (12h)", "Automation Down (6h)", "Extended Outage (48h)"])
    
    if playbook_type == "WMS Outage (12h)":
        st.markdown("""
        ### **WMS OUTAGE PLAYBOOK (12 HOURS)**
        **IMMEDIATE ACTIONS (0-30 min):**
        1. Activate Incident Response Team
        2. Print last known inventory snapshot
        3. Identify feasible orders (VIP + SLA critical)
        
        **STAFFING:** Zone A: 15 (priority picks), Zone B: 20 (standard), Zone C: 10 (sort/pack)
        **EXPECTED:** Process 45/100 orders, 84% on-time, +7.1h delay
        """)
    # Add other playbooks...

# Footer
st.markdown("---")
st.markdown("""
**Cyber-Resilience Fallback Assistant v1.0**  
*Built for Logistics & Warehousing Management Course* | *December 2025*
""")
