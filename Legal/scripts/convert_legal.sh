#!/bin/bash
# CCASH Legal Document Conversion
# Converts only the legal documents (A, B, C, D, E, F, N, 00 series) to HTML and DOCX
# With dynamic numbering like LibreOffice

BASE_DIR="/home/user/CCASH/Series Docs"
OUTPUT_DIR="$BASE_DIR/OUTPUT/Converted"

# Create clean output directories
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/HTML"
mkdir -p "$OUTPUT_DIR/DOCX"

echo "=== CCASH Legal Document Conversion ==="
echo ""

# Create CSS for HTML output (LibreOffice style)
cat > "$OUTPUT_DIR/style.css" << 'CSSEOF'
body {
    font-family: 'Times New Roman', 'Liberation Serif', serif;
    font-size: 12pt;
    line-height: 1.5;
    max-width: 8.5in;
    margin: 1in auto;
    padding: 0 0.5in;
    color: #000;
}
h1, h2, h3, h4, h5, h6 {
    font-family: Arial, 'Liberation Sans', sans-serif;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    page-break-after: avoid;
}
h1 { font-size: 18pt; border-bottom: 2px solid #000; padding-bottom: 0.3em; }
h2 { font-size: 16pt; }
h3 { font-size: 14pt; }
h4 { font-size: 12pt; }
p { margin: 0.5em 0; text-align: justify; }
ul, ol { margin: 0.5em 0; padding-left: 2em; }
li { margin: 0.25em 0; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 11pt; }
th, td { border: 1px solid #000; padding: 0.4em 0.6em; text-align: left; vertical-align: top; }
th { background-color: #E6E6E6; font-weight: bold; }
code { font-family: 'Courier New', 'Liberation Mono', monospace; font-size: 10pt; background: #F5F5F5; padding: 0.1em 0.3em; }
pre { background: #F5F5F5; border: 1px solid #DDD; padding: 1em; overflow-x: auto; font-size: 10pt; }
blockquote { margin: 1em 2em; padding-left: 1em; border-left: 3px solid #CCC; font-style: italic; }
hr { border: none; border-top: 1px solid #000; margin: 2em 0; }
#TOC { background: #F9F9F9; border: 1px solid #DDD; padding: 1em; margin-bottom: 2em; }
#TOC ul { list-style: none; padding-left: 1em; }
#TOC > ul { padding-left: 0; }
@media print { 
    body { margin: 0; padding: 0; max-width: none; }
    #TOC { page-break-after: always; }
}
CSSEOF

echo "Converting legal documents with dynamic numbering..."
echo ""

# Define the document patterns
DOCS=(
    "Company/Formation/A1_Articles_of_Organization.md"
    "Company/Governance/B1_Master_Operating_Agreement.md"
    "Company/Governance/B2_Officer_Appointment_Resolution.md"
    "Company/Governance/B3_Officer_Rotation_Succession_Policy.md"
    "Company/Governance/B10_Insurance_and_Capital_Policy.md"
    "Company/Compliance/B4_Record_Keeping_Policy.md"
    "Company/Compliance/B5_BSA_AML_Program.md"
    "Company/Compliance/B6_IT_Security_Incident_BCP_DRP.md"
    "Company/Compliance/B7_Acceptable_Client_Use_Policy.md"
    "Company/Compliance/B8_Privacy_Data_Protection_Policy.md"
    "Company/Compliance/B9_Fit_and_Proper_Screening_Policy.md"
    "Company/Compliance/B12_Partner_Due_Diligence_Standard.md"
    "Company/Overview/00_Business_Model.md"
    "Company/Overview/00_README.md"
    "Client_Series/Client/B11_Client_Services_and_Licensing_Framework.md"
    "Client_Series/Client/F1_Client_Services_Agreement.md"
    "Client_Series/Client/F2_End_Customer_Terms_Template.md"
    "Client_Series/Formation/A2_Exhibit_A_Series_List.md"
    "Client_Series/Formation/A3_Exhibit_B_Series_Operating_Agreements.md"
    "Client_Series/Formation/D1_Articles_of_Amendment_Add_Series.md"
    "Client_Series/Schedule/N1_Partner_MSB_Agreement.md"
    "Client_Series/Schedule/N3_Approved_States_Schedule.md"
    "Client_Series/Schedule/N4_Partner_MSB_Directory.md"
    "Client_Series/Schedule/N5_Client_FinCEN_Filing_Guide.md"
    "Internal/Checklist/E1_Filing_Checklist_and_Instructions.md"
    "Internal/Checklist/E2_Securities_and_MTL_Checklist.md"
    "Internal/Registration/C1_ABN_Registration_CCASH.md"
    "Internal/Registration/C2_ABN_Template_Client_Series.md"
    "Internal/Registration/C3_Pricing_and_Routing_Schedule.md"
)

count=0
for rel in "${DOCS[@]}"; do
    src="$BASE_DIR/$rel"
    
    if [ ! -f "$src" ]; then
        echo "  ⚠ Not found: $rel"
        continue
    fi
    
    name=$(basename "$src" .md)
    dir=$(dirname "$rel")
    
    mkdir -p "$OUTPUT_DIR/HTML/$dir"
    mkdir -p "$OUTPUT_DIR/DOCX/$dir"
    
    echo "  $name"
    
    # HTML with numbered sections and TOC
    pandoc "$src" \
        --from markdown \
        --to html5 \
        --standalone \
        --number-sections \
        --toc \
        --toc-depth=3 \
        --css="style.css" \
        --metadata title="$name" \
        -o "$OUTPUT_DIR/HTML/$dir/$name.html" 2>/dev/null
    
    # DOCX with numbered sections and TOC  
    pandoc "$src" \
        --from markdown \
        --to docx \
        --number-sections \
        --toc \
        --toc-depth=3 \
        -o "$OUTPUT_DIR/DOCX/$dir/$name.docx" 2>/dev/null
    
    ((count++))
done

# Copy CSS to each HTML subdirectory for relative path access
for dir in $(find "$OUTPUT_DIR/HTML" -type d); do
    cp "$OUTPUT_DIR/style.css" "$dir/" 2>/dev/null || true
done

echo ""
echo "=== Conversion Complete ==="
echo "Documents converted: $count"
echo ""
echo "Output locations:"
echo "  HTML: $OUTPUT_DIR/HTML/"
echo "  DOCX: $OUTPUT_DIR/DOCX/"
echo ""
echo "Key documents:"
ls -la "$OUTPUT_DIR/DOCX/Company/Governance/" 2>/dev/null | head -10
