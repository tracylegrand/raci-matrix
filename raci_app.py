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
if 'function_input_key' not in st.session_state:
    st.session_state.function_input_key = 0
if 'stakeholder_input_key' not in st.session_state:
    st.session_state.stakeholder_input_key = 0
if 'refocus_function' not in st.session_state:
    st.session_state.refocus_function = False
if 'refocus_stakeholder' not in st.session_state:
    st.session_state.refocus_stakeholder = False
if 'last_raci_data_hash' not in st.session_state:
    st.session_state.last_raci_data_hash = None

# RACI options - keys are what get stored, values are what display in dropdown
RACI_OPTIONS = {
    '': '',
    'R': 'R - Responsible',
    'A': 'A - Accountable',
    'C': 'C - Consulted',
    'I': 'I - Informed'
}

# RACI labels for display (maps letter to full label)
RACI_LABELS = {
    'R': 'R - Responsible',
    'A': 'A - Accountable',
    'C': 'C - Consulted',
    'I': 'I - Informed'
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

def validate_raci_row(row_data):
    """Validate that a row has at most one 'A' (Accountable) role"""
    accountable_count = sum(1 for val in row_data if str(val).strip() == 'A')
    return accountable_count <= 1

def validate_raci_matrix(df):
    """Validate the entire RACI matrix for correctness"""
    errors = []
    for function in df.index:
        row_data = df.loc[function].values
        # Extract letter from value (could be 'A' or 'A - Accountable')
        accountable_count = 0
        for val in row_data:
            val_str = str(val).strip()
            # Check if it starts with 'A' (could be 'A' or 'A - Accountable')
            if val_str and (val_str == 'A' or val_str.startswith('A -')):
                accountable_count += 1
        if accountable_count > 1:
            errors.append(f"Function '{function}' has {accountable_count} Accountable stakeholders. Only 1 is allowed.")
    return errors

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
                    
                    # Extract letter and convert to label for display
                    raci_letter = ''
                    display_value = value
                    if value:
                        if value.startswith('R -') or value == 'R':
                            raci_letter = 'R'
                            display_value = 'R - Responsible'
                        elif value.startswith('A -') or value == 'A':
                            raci_letter = 'A'
                            display_value = 'A - Accountable'
                        elif value.startswith('C -') or value == 'C':
                            raci_letter = 'C'
                            display_value = 'C - Consulted'
                        elif value.startswith('I -') or value == 'I':
                            raci_letter = 'I'
                            display_value = 'I - Informed'
                        elif len(value) == 1 and value in ['R', 'A', 'C', 'I']:
                            raci_letter = value
                            display_value = RACI_LABELS.get(value, value)
                        else:
                            raci_letter = value[0] if len(value) > 0 else ''
                            if raci_letter in RACI_LABELS:
                                display_value = RACI_LABELS[raci_letter]
                    
                    cell.value = display_value
                    
                    if raci_letter in RACI_COLORS:
                        hex_color = RACI_COLORS[raci_letter].replace('#', '')
                        cell.fill = PatternFill(
                            start_color=hex_color,
                            end_color=hex_color,
                            fill_type='solid'
                        )
                    
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                    cell.border = border
                    cell.font = Font(size=11, bold=(raci_letter in ['R', 'A']))
            
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
                
                # Value could be just letter ('R') or full label ('R - Responsible')
                # Extract the letter for color matching
                raci_letter = ''
                display_text = value
                
                if value:
                    # Check if it's a full label format
                    if value.startswith('R -') or value == 'R - Responsible':
                        raci_letter = 'R'
                        display_text = 'R - Responsible'
                    elif value.startswith('A -') or value == 'A - Accountable':
                        raci_letter = 'A'
                        display_text = 'A - Accountable'
                    elif value.startswith('C -') or value == 'C - Consulted':
                        raci_letter = 'C'
                        display_text = 'C - Consulted'
                    elif value.startswith('I -') or value == 'I - Informed':
                        raci_letter = 'I'
                        display_text = 'I - Informed'
                    elif len(value) == 1 and value in ['R', 'A', 'C', 'I']:
                        # Just the letter - convert to full label
                        raci_letter = value
                        display_text = RACI_LABELS.get(value, value)
                    else:
                        # Try to extract first character
                        raci_letter = value[0] if len(value) > 0 else ''
                        if raci_letter in RACI_LABELS:
                            display_text = RACI_LABELS[raci_letter]
                
                cell.text = display_text
                
                # Apply color based on the letter
                if raci_letter in RACI_COLORS:
                    color = RACI_COLORS[raci_letter]
                    rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(*rgb)
        
        # Format all cells with larger font
        for row in range(num_rows):
            for col in range(num_cols):
                cell = table.cell(row, col)
                # Increased font size for data cells (was Pt(10), now Pt(14))
                # Header and index keep larger size
                if row == 0 or col == 0:
                    # Header and index cells
                    cell.text_frame.paragraphs[0].font.size = Pt(12)
                    cell.text_frame.paragraphs[0].font.bold = True
                    if row == 0:
                        cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
                    else:
                        cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
                else:
                    # Data cells - larger font
                    cell.text_frame.paragraphs[0].font.size = Pt(14)
                    cell.text_frame.paragraphs[0].font.bold = False
                cell.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        
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

# Version and author info
VERSION = "1.0.0"
AUTHOR = "TL"

# Custom CSS for version and author display in upper right
st.markdown(f"""
    <style>
    .version-info {{
        position: fixed;
        top: 10px;
        right: 20px;
        background-color: rgba(255, 255, 255, 0.9);
        padding: 8px 12px;
        border-radius: 5px;
        font-size: 12px;
        color: #666;
        z-index: 999;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    </style>
    <div class="version-info">
        <strong>v{VERSION}</strong> | Author: {AUTHOR}
    </div>
""", unsafe_allow_html=True)

# Custom CSS and JavaScript to change cell selection color from red to light blue
st.markdown("""
    <style>
    /* Override Streamlit's default red selection color - change to light blue */
    /* Target all possible selection states */
    div[data-baseweb="data-table"] tbody tr td:focus,
    div[data-baseweb="data-table"] tbody tr td.selected,
    div[data-baseweb="data-table"] tbody tr td[aria-selected="true"],
    div[data-baseweb="data-table"] tbody tr td[data-selected="true"] {
        background-color: #e3f2fd !important;
        border: 2px solid #2196f3 !important;
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2) !important;
    }
    
    /* Change focus ring color to light blue */
    div[data-baseweb="data-table"] tbody tr td:focus-visible {
        outline: 2px solid #2196f3 !important;
        outline-offset: -2px;
        background-color: #e3f2fd !important;
    }
    
    /* Remove red border/outline from selected cells - use light blue */
    .stDataEditor [data-baseweb="data-table"] tbody tr td[aria-selected="true"],
    .stDataEditor [data-baseweb="data-table"] tbody tr td.selected,
    .stDataEditor [data-baseweb="data-table"] tbody tr td:focus {
        background-color: #e3f2fd !important;
        border-color: #2196f3 !important;
        box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2) !important;
    }
    
    /* Override Streamlit's red selection box */
    div[data-baseweb="data-table"] tbody tr td[style*="background-color"]:focus,
    div[data-baseweb="data-table"] tbody tr td[style*="rgb(255"] {
        background-color: #e3f2fd !important;
        border-color: #2196f3 !important;
    }
    
    /* Override any red colors in the selection */
    div[data-baseweb="data-table"] tbody tr td {
        --selection-color: #2196f3 !important;
    }
    
    /* Target the cell editor specifically */
    .stDataEditor div[data-baseweb="data-table"] tbody tr td:focus {
        background-color: #e3f2fd !important;
        border: 2px solid #2196f3 !important;
    }
    
    /* Override selectbox dropdown when cell is selected */
    div[data-baseweb="data-table"] tbody tr td div[data-baseweb="select"]:focus {
        background-color: #e3f2fd !important;
    }
    </style>
    <script>
    // Watch for red background colors and change them to light blue
    function fixRedSelection() {
        var cells = document.querySelectorAll('div[data-baseweb="data-table"] tbody tr td');
        cells.forEach(function(cell) {
            var style = window.getComputedStyle(cell);
            var bgColor = style.backgroundColor;
            // Check if it's red or red-like (rgb(255, ...) or similar)
            if (bgColor.includes('rgb(255') || bgColor.includes('rgb(255, 0, 0)') || 
                bgColor.includes('rgb(255,0,0)') || bgColor.includes('rgba(255')) {
                if (cell === document.activeElement || cell.contains(document.activeElement)) {
                    cell.style.backgroundColor = '#e3f2fd';
                    cell.style.borderColor = '#2196f3';
                    cell.style.borderWidth = '2px';
                }
            }
        });
    }
    
    // Run on load and periodically
    setInterval(fixRedSelection, 100);
    
    // Also watch for focus events
    document.addEventListener('focusin', function(e) {
        var cell = e.target.closest('td');
        if (cell && cell.closest('[data-baseweb="data-table"]')) {
            setTimeout(function() {
                cell.style.backgroundColor = '#e3f2fd';
                cell.style.borderColor = '#2196f3';
                cell.style.borderWidth = '2px';
            }, 10);
        }
    }, true);
    </script>
""", unsafe_allow_html=True)

st.title("📊 Interactive RACI Matrix Builder")
st.markdown("Build and manage your RACI (Responsible, Accountable, Consulted, Informed) matrix interactively.")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    
    # Add functions
    st.subheader("Functions (Rows)")
    with st.form("add_function_form", clear_on_submit=False):
        new_function = st.text_input("Add new function", key=f"function_input_{st.session_state.function_input_key}")
        submitted_func = st.form_submit_button("➕ Add Function", use_container_width=True)
        if submitted_func:
            # Capture value
            function_value = new_function.strip() if new_function else ""
            if function_value:
                if function_value not in st.session_state.functions:
                    st.session_state.functions.append(function_value)
                    # Clear input by incrementing key
                    st.session_state.function_input_key += 1
                    # Set flag to refocus
                    st.session_state.refocus_function = True
                    st.rerun()
                else:
                    st.warning("Function already exists!")
            else:
                st.warning("Please enter a function name.")
    
    # JavaScript to refocus input after form submission
    if st.session_state.refocus_function:
        st.session_state.refocus_function = False
        st.markdown("""
            <script>
            function refocusFunctionInput() {
                var inputs = document.querySelectorAll('input[type="text"]');
                for (var i = 0; i < inputs.length; i++) {
                    var input = inputs[i];
                    var label = input.closest('div')?.querySelector('label');
                    if (label && (label.textContent.includes('function') || 
                        input.placeholder?.toLowerCase().includes('function'))) {
                        setTimeout(function() {
                            input.focus();
                            input.select();
                        }, 50);
                        return;
                    }
                }
                // Fallback: find by placeholder
                setTimeout(function() {
                    var allInputs = document.querySelectorAll('input[type="text"]');
                    for (var j = 0; j < allInputs.length; j++) {
                        if (allInputs[j].placeholder && allInputs[j].placeholder.toLowerCase().includes('function')) {
                            allInputs[j].focus();
                            allInputs[j].select();
                            break;
                        }
                    }
                }, 100);
            }
            refocusFunctionInput();
            </script>
        """, unsafe_allow_html=True)
    
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
    with st.form("add_stakeholder_form", clear_on_submit=False):
        new_stakeholder = st.text_input("Add new stakeholder", key=f"stakeholder_input_{st.session_state.stakeholder_input_key}")
        submitted_stake = st.form_submit_button("➕ Add Stakeholder", use_container_width=True)
        if submitted_stake:
            # Capture value
            stakeholder_value = new_stakeholder.strip() if new_stakeholder else ""
            if stakeholder_value:
                if stakeholder_value not in st.session_state.stakeholders:
                    st.session_state.stakeholders.append(stakeholder_value)
                    # Clear input by incrementing key
                    st.session_state.stakeholder_input_key += 1
                    # Set flag to refocus
                    st.session_state.refocus_stakeholder = True
                    st.rerun()
                else:
                    st.warning("Stakeholder already exists!")
            else:
                st.warning("Please enter a stakeholder name.")
    
    # JavaScript to refocus input after form submission
    if st.session_state.refocus_stakeholder:
        st.session_state.refocus_stakeholder = False
        st.markdown("""
            <script>
            function refocusStakeholderInput() {
                var inputs = document.querySelectorAll('input[type="text"]');
                for (var i = 0; i < inputs.length; i++) {
                    var input = inputs[i];
                    var label = input.closest('div')?.querySelector('label');
                    if (label && (label.textContent.includes('stakeholder') || 
                        input.placeholder?.toLowerCase().includes('stakeholder'))) {
                        setTimeout(function() {
                            input.focus();
                            input.select();
                        }, 50);
                        return;
                    }
                }
                // Fallback: find by placeholder
                setTimeout(function() {
                    var allInputs = document.querySelectorAll('input[type="text"]');
                    for (var j = 0; j < allInputs.length; j++) {
                        if (allInputs[j].placeholder && allInputs[j].placeholder.toLowerCase().includes('stakeholder')) {
                            allInputs[j].focus();
                            allInputs[j].select();
                            break;
                        }
                    }
                }, 100);
            }
            refocusStakeholderInput();
            </script>
        """, unsafe_allow_html=True)
    
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
        st.session_state.function_input_key = 0
        st.session_state.stakeholder_input_key = 0
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
    st.caption("⚠️ Each function must have exactly 1 Accountable (A) stakeholder. Multiple Responsible (R), Consulted (C), or Informed (I) roles are allowed.")
    
    # Validate current matrix and show warnings
    validation_errors = validate_raci_matrix(st.session_state.raci_data)
    if validation_errors:
        for error in validation_errors:
            st.warning(error)
    
    # Create interactive matrix using st.data_editor
    # Check if matrix structure changed (new functions/stakeholders added)
    if st.session_state.raci_data.empty or \
       list(st.session_state.raci_data.index) != st.session_state.functions or \
       list(st.session_state.raci_data.columns) != st.session_state.stakeholders:
        # Recreate matrix with new structure
        st.session_state.raci_data = create_raci_matrix(
            st.session_state.functions,
            st.session_state.stakeholders
        )
    
    # Prepare data for editor - ensure consistent format
    # Use a fresh copy to avoid reference issues
    data_for_editor = st.session_state.raci_data.copy()
    # Normalize empty values to empty strings for consistency
    data_for_editor = data_for_editor.fillna('')
    
    # Create the data editor WITHOUT a key
    # Removing the key prevents widget state caching that causes every 2nd edit to revert
    # Session state will maintain the data between renders
    # Use the full labels as options so they display in the dropdown
    edited_df = st.data_editor(
        data_for_editor,
        column_config={
            col: st.column_config.SelectboxColumn(
                col,
                width="medium",
                options=list(RACI_OPTIONS.values()),  # Use values (labels) for display
                help=f"Select RACI role for {col}. Note: Only 1 'A' per function!"
            )
            for col in st.session_state.raci_data.columns
        },
        use_container_width=True,
        height=400,
        hide_index=False
        # NO KEY - this prevents widget state caching that causes reverts
    )
    
    # CRITICAL FIX: Always update session state from editor's return value
    # Do this immediately and unconditionally to prevent reverts
    if edited_df is not None:
        # Normalize empty values to empty strings
        edited_clean = edited_df.fillna('')
        
        # Compare to see if we need to update
        current_str = data_for_editor.astype(str).to_string()
        edited_str = edited_clean.astype(str).to_string()
        
        # Update session state if changed
        if current_str != edited_str:
            # Update session state immediately - this is the source of truth
            st.session_state.raci_data = edited_clean.copy()
            # Force a rerun to ensure UI reflects the change immediately
            st.rerun()
    
    # Check validation status AFTER updating session state
    # Use the updated session state for validation
    validation_errors = validate_raci_matrix(st.session_state.raci_data)
    
    # Use a container to manage validation messages so they clear properly
    validation_container = st.container()
    with validation_container:
        if validation_errors:
            # Show errors - these will clear when validation passes
            for error in validation_errors:
                st.error(error)
        else:
            # Only show success if we have actual data entries (not all empty)
            has_data = False
            if not st.session_state.raci_data.empty:
                # Check if any cell has a non-empty value
                has_data = (st.session_state.raci_data.fillna('').astype(str) != '').any().any()
            
            if has_data:
                st.success("✅ All functions have valid RACI assignments!")
    
    # Display styled matrix
    st.subheader("Visual Matrix")
    styled_df = st.session_state.raci_data.copy()
    
    # Apply styling function
    def style_raci(val):
        # Extract letter from value (could be 'R' or 'R - Responsible')
        val_str = str(val).strip()
        raci_letter = ''
        if val_str:
            if val_str.startswith('R -') or val_str == 'R':
                raci_letter = 'R'
            elif val_str.startswith('A -') or val_str == 'A':
                raci_letter = 'A'
            elif val_str.startswith('C -') or val_str == 'C':
                raci_letter = 'C'
            elif val_str.startswith('I -') or val_str == 'I':
                raci_letter = 'I'
            elif len(val_str) == 1 and val_str in ['R', 'A', 'C', 'I']:
                raci_letter = val_str
            else:
                raci_letter = val_str[0] if len(val_str) > 0 else ''
        
        if raci_letter in RACI_COLORS:
            return f'background-color: {RACI_COLORS[raci_letter]}'
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

