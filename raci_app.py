import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Initialize session state
if 'raci_data' not in st.session_state:
    st.session_state.raci_data = pd.DataFrame()
if 'functions' not in st.session_state:
    st.session_state.functions = []
if 'stakeholders' not in st.session_state:
    st.session_state.stakeholders = []

# RACI options
RACI_OPTIONS = {
    '': '',
    'R': 'Responsible',
    'A': 'Accountable',
    'C': 'Consulted',
    'I': 'Informed'
}

# Color scheme for RACI
RACI_COLORS = {
    'R': '#FFE5B4',  # Light orange
    'A': '#FFB6C1',  # Light pink
    'C': '#B0E0E6',  # Powder blue
    'I': '#E0E0E0'   # Light gray
}

def create_raci_matrix(functions, stakeholders):
    """Create an empty RACI matrix DataFrame"""
    if not functions or not stakeholders:
        return pd.DataFrame()
    
    # Create matrix with functions as rows and stakeholders as columns
    matrix = pd.DataFrame(
        index=functions,
        columns=stakeholders,
        data=''
    )
    return matrix

def export_to_excel(df, filename='raci_matrix.xlsx'):
    """Export RACI matrix to Excel with formatting"""
    if df.empty:
        raise ValueError("Cannot export empty matrix. Please add functions and stakeholders first.")
    
    output = BytesIO()
    
    try:
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='RACI Matrix', index=True)
            worksheet = writer.sheets['RACI Matrix']
            
            # Set column widths
            worksheet.column_dimensions['A'].width = 25
            for col in range(2, len(df.columns) + 2):
                worksheet.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 15
            
            # Style header row
            header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
            header_font = Font(color='FFFFFF', bold=True, size=11)
            border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )
            
            # Format header
            for cell in worksheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center', vertical='center')
                cell.border = border
            
            # Format index column
            index_fill = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')
            index_font = Font(bold=True, size=11)
            
            for row in range(2, len(df) + 2):
                cell = worksheet[f'A{row}']
                cell.fill = index_fill
                cell.font = index_font
                cell.alignment = Alignment(horizontal='left', vertical='center')
                cell.border = border
            
            # Format data cells with RACI colors
            for row_idx, row in enumerate(df.index, start=2):
                for col_idx, col in enumerate(df.columns, start=2):
                    cell = worksheet.cell(row=row_idx, column=col_idx)
                    value = str(df.loc[row, col]).strip()
                    
                    if value in RACI_COLORS:
                        hex_color = RACI_COLORS[value].replace('#', '')
                        cell.fill = PatternFill(
                            start_color=hex_color,
                            end_color=hex_color,
                            fill_type='solid'
                        )
                    
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                    cell.border = border
                    cell.font = Font(size=11, bold=(value in ['R', 'A']))
            
            # Add legend
            legend_row = len(df) + 3
            worksheet.cell(row=legend_row, column=1, value='Legend:')
            worksheet.cell(row=legend_row, column=1).font = Font(bold=True, size=11)
            
            legend_items = ['R = Responsible', 'A = Accountable', 'C = Consulted', 'I = Informed']
            for idx, item in enumerate(legend_items, start=2):
                cell = worksheet.cell(row=legend_row, column=idx, value=item)
                cell.font = Font(size=10)
    except Exception as e:
        st.error(f"Error exporting to Excel: {str(e)}")
        raise
    
    output.seek(0)
    return output

def export_to_powerpoint(df, filename='raci_matrix.pptx'):
    """Export RACI matrix to PowerPoint presentation"""
    if df.empty:
        raise ValueError("Cannot export empty matrix. Please add functions and stakeholders first.")
    
    try:
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)
        
        # Use blank layout
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # Add title
        title_left = Inches(0.5)
        title_top = Inches(0.3)
        title_width = Inches(9)
        title_height = Inches(0.5)
        
        title_box = slide.shapes.add_textbox(title_left, title_top, title_width, title_height)
        title_frame = title_box.text_frame
        title_frame.text = "RACI Matrix"
        title_para = title_frame.paragraphs[0]
        title_para.font.size = Pt(24)
        title_para.font.bold = True
        title_para.alignment = PP_ALIGN.CENTER
        
        # Calculate table dimensions
        table_left = Inches(0.5)
        table_top = Inches(1)
        table_width = Inches(9)
        table_height = Inches(5)
        
        # Create table
        num_rows = len(df) + 1  # +1 for header
        num_cols = len(df.columns) + 1  # +1 for index column
        
        table = slide.shapes.add_table(num_rows, num_cols, table_left, table_top, table_width, table_height).table
        
        # Set column widths
        index_col_width = table_width / num_cols * 1.5
        data_col_width = (table_width - index_col_width) / (num_cols - 1)
        
        # Fill header row
        table.cell(0, 0).text = "Function"
        table.cell(0, 0).fill.solid()
        table.cell(0, 0).fill.fore_color.rgb = RGBColor(54, 96, 146)
        
        for col_idx, stakeholder in enumerate(df.columns, start=1):
            cell = table.cell(0, col_idx)
            cell.text = stakeholder
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(54, 96, 146)
        
        # Fill data rows
        for row_idx, function in enumerate(df.index, start=1):
            # Index column
            table.cell(row_idx, 0).text = function
            table.cell(row_idx, 0).fill.solid()
            table.cell(row_idx, 0).fill.fore_color.rgb = RGBColor(217, 225, 242)
            
            # Data cells
            for col_idx, stakeholder in enumerate(df.columns, start=1):
                cell = table.cell(row_idx, col_idx)
                value = str(df.loc[function, stakeholder]).strip()
                cell.text = value
                
                if value in RACI_COLORS:
                    color = RACI_COLORS[value]
                    rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(*rgb)
        
        # Format all cells
        for row in range(num_rows):
            for col in range(num_cols):
                cell = table.cell(row, col)
                cell.text_frame.paragraphs[0].font.size = Pt(10)
                cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
                if row == 0 or col == 0:
                    cell.text_frame.paragraphs[0].font.bold = True
                    if row == 0:
                        cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
                    else:
                        cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
        
        # Add legend
        legend_top = Inches(6.5)
        legend_left = Inches(0.5)
        legend_width = Inches(9)
        legend_height = Inches(0.5)
        
        legend_box = slide.shapes.add_textbox(legend_left, legend_top, legend_width, legend_height)
        legend_frame = legend_box.text_frame
        legend_frame.text = "Legend: R = Responsible | A = Accountable | C = Consulted | I = Informed"
        legend_para = legend_frame.paragraphs[0]
        legend_para.font.size = Pt(9)
        legend_para.alignment = PP_ALIGN.CENTER
        
        output = BytesIO()
        prs.save(output)
        output.seek(0)
        return output
    except Exception as e:
        st.error(f"Error exporting to PowerPoint: {str(e)}")
        raise

# Streamlit UI
st.set_page_config(page_title="RACI Matrix Builder", page_icon="📊", layout="wide")

st.title("📊 Interactive RACI Matrix Builder")
st.markdown("Build and manage your RACI (Responsible, Accountable, Consulted, Informed) matrix interactively.")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    # Add functions
    st.subheader("Functions (Rows)")
    new_function = st.text_input("Add new function", key="new_function")
    if st.button("➕ Add Function", key="add_function"):
        if new_function and new_function not in st.session_state.functions:
            st.session_state.functions.append(new_function)
            st.rerun()
    
    # Display and remove functions
    if st.session_state.functions:
        st.write("**Current Functions:**")
        for idx, func in enumerate(st.session_state.functions):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{idx + 1}. {func}")
            with col2:
                if st.button("🗑️", key=f"del_func_{idx}"):
                    st.session_state.functions.pop(idx)
                    st.rerun()
    
    st.divider()
    
    # Add stakeholders
    st.subheader("Stakeholders (Columns)")
    new_stakeholder = st.text_input("Add new stakeholder", key="new_stakeholder")
    if st.button("➕ Add Stakeholder", key="add_stakeholder"):
        if new_stakeholder and new_stakeholder not in st.session_state.stakeholders:
            st.session_state.stakeholders.append(new_stakeholder)
            st.rerun()
    
    # Display and remove stakeholders
    if st.session_state.stakeholders:
        st.write("**Current Stakeholders:**")
        for idx, stake in enumerate(st.session_state.stakeholders):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{idx + 1}. {stake}")
            with col2:
                if st.button("🗑️", key=f"del_stake_{idx}"):
                    st.session_state.stakeholders.pop(idx)
                    st.rerun()
    
    st.divider()
    
    # Clear all button
    if st.button("🗑️ Clear All", type="secondary"):
        st.session_state.functions = []
        st.session_state.stakeholders = []
        st.session_state.raci_data = pd.DataFrame()
        st.rerun()

# Main area - RACI Matrix
if st.session_state.functions and st.session_state.stakeholders:
    # Create or update matrix
    if st.session_state.raci_data.empty or \
       list(st.session_state.raci_data.index) != st.session_state.functions or \
       list(st.session_state.raci_data.columns) != st.session_state.stakeholders:
        st.session_state.raci_data = create_raci_matrix(
            st.session_state.functions,
            st.session_state.stakeholders
        )
    
    st.subheader("RACI Matrix")
    st.caption("Select R (Responsible), A (Accountable), C (Consulted), or I (Informed) for each cell")
    
    # Create interactive matrix using st.data_editor
    edited_df = st.data_editor(
        st.session_state.raci_data,
        column_config={
            col: st.column_config.SelectboxColumn(
                col,
                width="medium",
                options=list(RACI_OPTIONS.keys()),
                help=f"Select RACI role for {col}"
            )
            for col in st.session_state.raci_data.columns
        },
        use_container_width=True,
        height=400,
        hide_index=False
    )
    
    # Update session state if changed
    if not edited_df.equals(st.session_state.raci_data):
        st.session_state.raci_data = edited_df
    
    # Display styled matrix
    st.subheader("Visual Matrix")
    styled_df = st.session_state.raci_data.copy()
    
    # Apply styling function
    def style_raci(val):
        if val in RACI_COLORS:
            return f'background-color: {RACI_COLORS[val]}'
        return ''
    
    # Use map instead of applymap (applymap deprecated in pandas 2.1.0+)
    try:
        styled_display = styled_df.style.map(style_raci)
    except AttributeError:
        # Fallback for older pandas versions
        styled_display = styled_df.style.applymap(style_raci)
    st.dataframe(styled_display, use_container_width=True, height=400)
    
    # Export section
    st.divider()
    st.subheader("Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Export to Spreadsheet**")
        try:
            excel_buffer = export_to_excel(st.session_state.raci_data)
            st.download_button(
                label="📊 Download Excel File",
                data=excel_buffer,
                file_name="raci_matrix.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Cannot export to Excel: {str(e)}")
        
        try:
            csv = st.session_state.raci_data.to_csv()
            st.download_button(
                label="📄 Download CSV File",
                data=csv,
                file_name="raci_matrix.csv",
                mime="text/csv",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Cannot export to CSV: {str(e)}")
    
    with col2:
        st.markdown("**Export to Presentation**")
        try:
            pptx_buffer = export_to_powerpoint(st.session_state.raci_data)
            st.download_button(
                label="📽️ Download PowerPoint File",
                data=pptx_buffer,
                file_name="raci_matrix.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Cannot export to PowerPoint: {str(e)}")
    
    # Legend
    st.divider()
    st.markdown("**Legend:**")
    legend_cols = st.columns(4)
    with legend_cols[0]:
        st.markdown(f"<div style='background-color: {RACI_COLORS['R']}; padding: 10px; border-radius: 5px; text-align: center;'><b>R</b> - Responsible</div>", unsafe_allow_html=True)
    with legend_cols[1]:
        st.markdown(f"<div style='background-color: {RACI_COLORS['A']}; padding: 10px; border-radius: 5px; text-align: center;'><b>A</b> - Accountable</div>", unsafe_allow_html=True)
    with legend_cols[2]:
        st.markdown(f"<div style='background-color: {RACI_COLORS['C']}; padding: 10px; border-radius: 5px; text-align: center;'><b>C</b> - Consulted</div>", unsafe_allow_html=True)
    with legend_cols[3]:
        st.markdown(f"<div style='background-color: {RACI_COLORS['I']}; padding: 10px; border-radius: 5px; text-align: center;'><b>I</b> - Informed</div>", unsafe_allow_html=True)

else:
    st.info("👈 Start by adding functions and stakeholders in the sidebar to create your RACI matrix.")

