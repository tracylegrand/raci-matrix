import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Practice Manager Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# Initialize session state for data
if 'pm_data' not in st.session_state:
    st.session_state.pm_data = None
if 'customer_data' not in st.session_state:
    st.session_state.customer_data = None

def generate_fictional_data():
    """Generate fictional data for Practice Managers and their bookings"""
    
    # Practice Manager names
    practice_managers = [
        "Sarah Chen",
        "Michael Rodriguez",
        "Emily Johnson",
        "David Park",
        "Jennifer Martinez"
    ]
    
    # Manufacturing industry customer accounts
    manufacturing_customers = [
        "Acme Manufacturing Corp",
        "Global Industrial Solutions",
        "Precision Components Inc",
        "Advanced Materials Group",
        "SteelWorks Industries",
        "Automotive Parts Manufacturing",
        "Heavy Machinery Co",
        "Electronics Assembly Systems",
        "Chemical Processing Industries",
        "Aerospace Components Ltd",
        "Textile Manufacturing Group",
        "Food Processing Equipment Co",
        "Pharmaceutical Manufacturing",
        "Semiconductor Fabrication Inc",
        "Renewable Energy Systems"
    ]
    
    # Quarters for the year
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    
    # Generate booking data with incremental quarter-over-quarter growth
    bookings_data = []
    customer_data = []
    
    # Base booking values per quarter (incremental growth)
    base_values = {
        'Q1': 500000,  # Starting point
        'Q2': 650000,  # 30% increase
        'Q3': 850000,  # 31% increase
        'Q4': 1100000  # 29% increase
    }
    
    booking_id = 1
    
    for pm in practice_managers:
        for quarter in quarters:
            # Calculate base for this PM and quarter (with some variation)
            pm_multiplier = np.random.uniform(0.8, 1.2)  # Each PM has different performance
            quarter_base = base_values[quarter] * pm_multiplier
            
            # Generate 3-6 bookings per PM per quarter
            num_bookings = np.random.randint(3, 7)
            
            for _ in range(num_bookings):
                # Select a random customer
                customer = np.random.choice(manufacturing_customers)
                
                # Booking value (distributed across bookings)
                booking_value = quarter_base / num_bookings * np.random.uniform(0.7, 1.3)
                
                # Total bookings
                total_booking = round(booking_value, 2)
                
                # Paid bookings (70-90% of total)
                paid_booking = round(total_booking * np.random.uniform(0.70, 0.90), 2)
                
                # Investment bookings (10-30% of total)
                investment_booking = round(total_booking * np.random.uniform(0.10, 0.30), 2)
                
                # Ensure investment + paid doesn't exceed total (adjust if needed)
                if paid_booking + investment_booking > total_booking:
                    investment_booking = max(0, total_booking - paid_booking)
                
                bookings_data.append({
                    'Booking ID': f'TS-{booking_id:04d}',
                    'Practice Manager': pm,
                    'Quarter': quarter,
                    'Customer Account': customer,
                    'Service Type': 'Technical Services',
                    'Total Bookings': total_booking,
                    'Paid Bookings': paid_booking,
                    'Investment Bookings': investment_booking,
                    'Year': 2024
                })
                
                booking_id += 1
    
    # Create customer account details
    for customer in manufacturing_customers:
        customer_bookings = [b for b in bookings_data if b['Customer Account'] == customer]
        total_value = sum(b['Total Bookings'] for b in customer_bookings)
        num_bookings = len(customer_bookings)
        pms_worked_with = list(set(b['Practice Manager'] for b in customer_bookings))
        
        customer_data.append({
            'Customer Account': customer,
            'Industry': 'Manufacturing',
            'Total Bookings Value': round(total_value, 2),
            'Number of Bookings': num_bookings,
            'Practice Managers': ', '.join(pms_worked_with),
            'Primary Service': 'Technical Services'
        })
    
    return pd.DataFrame(bookings_data), pd.DataFrame(customer_data)

# Generate data if not already generated
if st.session_state.pm_data is None:
    with st.spinner("Generating performance data..."):
        st.session_state.pm_data, st.session_state.customer_data = generate_fictional_data()

# Main dashboard
st.title("📊 Practice Manager Performance Dashboard")
st.markdown("Track and analyze Practice Manager performance by quarter with Technical Services bookings")

# Sidebar for filters
st.sidebar.header("Filters")

# Practice Manager selection (multi-select)
all_pms = sorted(st.session_state.pm_data['Practice Manager'].unique())
selected_pms = st.sidebar.multiselect(
    "Select Practice Manager(s)",
    options=all_pms,
    default=all_pms,
    help="Select one or more Practice Managers to view their performance"
)

# Quarter filter
all_quarters = sorted(st.session_state.pm_data['Quarter'].unique())
selected_quarters = st.sidebar.multiselect(
    "Select Quarter(s)",
    options=all_quarters,
    default=all_quarters
)

# Filter data based on selections
filtered_data = st.session_state.pm_data[
    (st.session_state.pm_data['Practice Manager'].isin(selected_pms)) &
    (st.session_state.pm_data['Quarter'].isin(selected_quarters))
]

if filtered_data.empty:
    st.warning("No data available for the selected filters. Please adjust your selections.")
else:
    # Summary metrics
    st.subheader("Performance Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_bookings = filtered_data['Total Bookings'].sum()
        st.metric("Total Bookings", f"${total_bookings:,.2f}")
    
    with col2:
        paid_bookings = filtered_data['Paid Bookings'].sum()
        st.metric("Paid Bookings", f"${paid_bookings:,.2f}")
    
    with col3:
        investment_bookings = filtered_data['Investment Bookings'].sum()
        st.metric("Investment Bookings", f"${investment_bookings:,.2f}")
    
    with col4:
        num_bookings = len(filtered_data)
        st.metric("Number of Bookings", num_bookings)
    
    st.divider()
    
    # Performance by Quarter
    st.subheader("Performance by Quarter")
    
    # Aggregate by quarter
    quarterly_summary = filtered_data.groupby('Quarter').agg({
        'Total Bookings': 'sum',
        'Paid Bookings': 'sum',
        'Investment Bookings': 'sum'
    }).reset_index()
    
    # Sort quarters in order
    quarter_order = ['Q1', 'Q2', 'Q3', 'Q4']
    quarterly_summary['Quarter'] = pd.Categorical(quarterly_summary['Quarter'], categories=quarter_order, ordered=True)
    quarterly_summary = quarterly_summary.sort_values('Quarter')
    
    # Create bar chart
    fig_quarterly = go.Figure()
    
    fig_quarterly.add_trace(go.Bar(
        name='Total Bookings',
        x=quarterly_summary['Quarter'],
        y=quarterly_summary['Total Bookings'],
        marker_color='#1f77b4'
    ))
    
    fig_quarterly.add_trace(go.Bar(
        name='Paid Bookings',
        x=quarterly_summary['Quarter'],
        y=quarterly_summary['Paid Bookings'],
        marker_color='#2ca02c'
    ))
    
    fig_quarterly.add_trace(go.Bar(
        name='Investment Bookings',
        x=quarterly_summary['Quarter'],
        y=quarterly_summary['Investment Bookings'],
        marker_color='#ff7f0e'
    ))
    
    fig_quarterly.update_layout(
        title="Bookings by Quarter",
        xaxis_title="Quarter",
        yaxis_title="Booking Value ($)",
        barmode='group',
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_quarterly, use_container_width=True)
    
    # Performance by Practice Manager
    if len(selected_pms) > 1:
        st.subheader("Performance by Practice Manager")
        
        pm_summary = filtered_data.groupby('Practice Manager').agg({
            'Total Bookings': 'sum',
            'Paid Bookings': 'sum',
            'Investment Bookings': 'sum',
            'Booking ID': 'count'
        }).reset_index()
        pm_summary.columns = ['Practice Manager', 'Total Bookings', 'Paid Bookings', 'Investment Bookings', 'Number of Bookings']
        pm_summary = pm_summary.sort_values('Total Bookings', ascending=False)
        
        # Create horizontal bar chart
        fig_pm = go.Figure()
        
        fig_pm.add_trace(go.Bar(
            name='Total Bookings',
            y=pm_summary['Practice Manager'],
            x=pm_summary['Total Bookings'],
            orientation='h',
            marker_color='#1f77b4'
        ))
        
        fig_pm.update_layout(
            title="Total Bookings by Practice Manager",
            xaxis_title="Booking Value ($)",
            yaxis_title="Practice Manager",
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig_pm, use_container_width=True)
        
        # Display PM summary table
        st.dataframe(
            pm_summary.style.format({
                'Total Bookings': '${:,.2f}',
                'Paid Bookings': '${:,.2f}',
                'Investment Bookings': '${:,.2f}'
            }),
            use_container_width=True,
            hide_index=True
        )
    
    st.divider()
    
    # Detailed bookings table
    st.subheader("Detailed Bookings")
    
    # Display options
    display_cols = ['Booking ID', 'Practice Manager', 'Quarter', 'Customer Account', 
                   'Total Bookings', 'Paid Bookings', 'Investment Bookings']
    
    detailed_table = filtered_data[display_cols].copy()
    detailed_table = detailed_table.sort_values(['Quarter', 'Practice Manager', 'Total Bookings'], 
                                                ascending=[True, True, False])
    
    st.dataframe(
        detailed_table.style.format({
            'Total Bookings': '${:,.2f}',
            'Paid Bookings': '${:,.2f}',
            'Investment Bookings': '${:,.2f}'
        }),
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()
    
    # Customer accounts section
    st.subheader("Customer Accounts")
    
    # Get unique customers from filtered data
    filtered_customers = filtered_data['Customer Account'].unique()
    customer_summary = st.session_state.customer_data[
        st.session_state.customer_data['Customer Account'].isin(filtered_customers)
    ].copy()
    
    # Add additional metrics from filtered data
    customer_metrics = filtered_data.groupby('Customer Account').agg({
        'Total Bookings': 'sum',
        'Paid Bookings': 'sum',
        'Investment Bookings': 'sum',
        'Booking ID': 'count',
        'Practice Manager': lambda x: ', '.join(sorted(set(x)))
    }).reset_index()
    
    customer_metrics.columns = ['Customer Account', 'Total Bookings', 'Paid Bookings', 
                               'Investment Bookings', 'Number of Bookings', 'Practice Managers']
    
    customer_summary = customer_summary.merge(
        customer_metrics[['Customer Account', 'Total Bookings', 'Paid Bookings', 
                         'Investment Bookings', 'Number of Bookings', 'Practice Managers']],
        on='Customer Account',
        how='left',
        suffixes=('_old', '')
    )
    
    # Drop old columns if they exist
    customer_summary = customer_summary.drop(columns=[col for col in customer_summary.columns 
                                                      if col.endswith('_old')], errors='ignore')
    
    customer_summary = customer_summary.sort_values('Total Bookings', ascending=False)
    
    st.dataframe(
        customer_summary.style.format({
            'Total Bookings': '${:,.2f}',
            'Paid Bookings': '${:,.2f}',
            'Investment Bookings': '${:,.2f}',
            'Total Bookings Value': '${:,.2f}'
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # Trend line chart showing incremental growth
    st.divider()
    st.subheader("Quarter-over-Quarter Growth Trend")
    
    # Calculate growth percentage
    quarterly_summary['Growth %'] = quarterly_summary['Total Bookings'].pct_change() * 100
    quarterly_summary['Growth %'] = quarterly_summary['Growth %'].fillna(0)
    
    # Create line chart
    fig_trend = go.Figure()
    
    fig_trend.add_trace(go.Scatter(
        x=quarterly_summary['Quarter'],
        y=quarterly_summary['Total Bookings'],
        mode='lines+markers',
        name='Total Bookings',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=10),
        text=[f"${val:,.0f}" for val in quarterly_summary['Total Bookings']],
        textposition='top center',
        hovertemplate='<b>%{x}</b><br>Total Bookings: $%{y:,.2f}<extra></extra>'
    ))
    
    fig_trend.update_layout(
        title="Quarter-over-Quarter Booking Growth",
        xaxis_title="Quarter",
        yaxis_title="Total Booking Value ($)",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Show growth percentages
    growth_cols = st.columns(len(quarterly_summary))
    for idx, row in quarterly_summary.iterrows():
        with growth_cols[idx]:
            if row['Growth %'] > 0:
                st.metric(
                    f"{row['Quarter']} Growth",
                    f"+{row['Growth %']:.1f}%",
                    delta=f"${row['Total Bookings']:,.0f}"
                )
            else:
                st.metric(
                    f"{row['Quarter']} Growth",
                    f"{row['Growth %']:.1f}%",
                    delta=f"${row['Total Bookings']:,.0f}"
                )

# Footer
st.divider()
st.caption("📊 Practice Manager Performance Dashboard - Technical Services Bookings | Manufacturing Industry")

