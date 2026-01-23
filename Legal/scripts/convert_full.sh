#!/bin/bash
# convert_full.sh - Complete conversion with cross-linking and navigation
# - Converts [DOC:X] to hyperlinks
# - Strips [TERM:X], [OBL:X], [FLOW:X] markers
# - Removes version history/edit logs from documents  
# - Injects sidebar navigation
# - Creates unified index

set -e

BASE_DIR="/home/user/CCASH/Series Docs"
OUTPUT_DIR="$BASE_DIR/OUTPUT/Converted/HTML"
TEMP_DIR="$BASE_DIR/OUTPUT/.temp_convert"

rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"
mkdir -p "$TEMP_DIR"

echo "=== CCASH Document Conversion ==="

# Document mappings
declare -A DOC_PATHS=(
    ["A1"]="Company/Formation/A1_Articles_of_Organization"
    ["A2"]="Client_Series/Formation/A2_Exhibit_A_Series_List"
    ["A3"]="Client_Series/Formation/A3_Exhibit_B_Series_Operating_Agreements"
    ["B1"]="Company/Governance/B1_Master_Operating_Agreement"
    ["B2"]="Company/Governance/B2_Officer_Appointment_Resolution"
    ["B3"]="Company/Governance/B3_Officer_Rotation_Succession_Policy"
    ["B4"]="Company/Compliance/B4_Record_Keeping_Policy"
    ["B5"]="Company/Compliance/B5_BSA_AML_Program"
    ["B6"]="Company/Compliance/B6_IT_Security_Incident_BCP_DRP"
    ["B7"]="Company/Compliance/B7_Acceptable_Client_Use_Policy"
    ["B8"]="Company/Compliance/B8_Privacy_Data_Protection_Policy"
    ["B9"]="Company/Compliance/B9_Fit_and_Proper_Screening_Policy"
    ["B10"]="Company/Governance/B10_Insurance_and_Capital_Policy"
    ["B11"]="Client_Series/Client/B11_Client_Services_and_Licensing_Framework"
    ["B12"]="Company/Compliance/B12_Partner_Due_Diligence_Standard"
    ["C1"]="Internal/Registration/C1_ABN_Registration_CCASH"
    ["C2"]="Internal/Registration/C2_ABN_Template_Client_Series"
    ["C3"]="Internal/Registration/C3_Pricing_and_Routing_Schedule"
    ["D1"]="Client_Series/Formation/D1_Articles_of_Amendment_Add_Series"
    ["E1"]="Internal/Checklist/E1_Filing_Checklist_and_Instructions"
    ["E2"]="Internal/Checklist/E2_Securities_and_MTL_Checklist"
    ["F1"]="Client_Series/Client/F1_Client_Services_Agreement"
    ["F2"]="Client_Series/Client/F2_End_Customer_Terms_Template"
    ["N1"]="Client_Series/Schedule/N1_Partner_MSB_Agreement"
    ["N3"]="Client_Series/Schedule/N3_Approved_States_Schedule"
    ["N4"]="Client_Series/Schedule/N4_Partner_MSB_Directory"
    ["N5"]="Client_Series/Schedule/N5_Client_FinCEN_Filing_Guide"
    ["00_README"]="Company/Overview/00_README"
    ["00_Business_Model"]="Company/Overview/00_Business_Model"
)

declare -A DOC_TITLES=(
    ["A1"]="Articles of Organization"
    ["A2"]="Exhibit A — Series List"
    ["A3"]="Exhibit B — Series Operating Agreements"
    ["B1"]="Master Operating Agreement"
    ["B2"]="Officer Appointment Resolution"
    ["B3"]="Officer Rotation & Succession Policy"
    ["B4"]="Record Keeping Policy"
    ["B5"]="BSA/AML Program"
    ["B6"]="IT Security / BCP / DRP"
    ["B7"]="Acceptable Client Use Policy"
    ["B8"]="Privacy & Data Protection Policy"
    ["B9"]="Fit & Proper Screening Policy"
    ["B10"]="Insurance & Capital Policy"
    ["B11"]="Client Services Framework"
    ["B12"]="Partner Due Diligence Standard"
    ["C1"]="ABN Registration (CCASH)"
    ["C2"]="ABN Template (Client Series)"
    ["C3"]="Pricing & Routing Schedule"
    ["D1"]="Articles of Amendment"
    ["E1"]="Filing Checklist"
    ["E2"]="Securities & MTL Checklist"
    ["F1"]="Client Services Agreement"
    ["F2"]="End Customer Terms"
    ["N1"]="Partner MSB Agreement"
    ["N3"]="Approved States Schedule"
    ["N4"]="Partner MSB Directory"
    ["N5"]="FinCEN Filing Guide"
    ["00_README"]="Document Overview"
    ["00_Business_Model"]="Business Model"
)

# Generate sidebar navigation HTML
generate_nav() {
    local prefix="$1"
    cat << 'NAVEOF'
<nav class="nav-sidebar">
  <div class="nav-header"><a href="PREFIX_PLACEHOLDERindex.html" class="logo">📋 CCASH Legal</a></div>
  <div class="nav-section-title">🏢 Company</div>
  <div class="nav-group-title">Overview</div>
  <a class="nav-link" href="PREFIX_PLACEHOLDERCompany/Overview/00_README.html"><span class="code">00</span>Overview</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERCompany/Overview/00_Business_Model.html"><span class="code">00</span>Business Model</a>
  <div class="nav-group-title">Formation</div>
  <a class="nav-link" href="PREFIX_PLACEHOLDERCompany/Formation/A1_Articles_of_Organization.html"><span class="code">A1</span>Articles of Org</a>
  <div class="nav-group-title">Governance</div>
  <a class="nav-link" href="PREFIX_PLACEHOLDERCompany/Governance/B1_Master_Operating_Agreement.html"><span class="code">B1</span>Master Op Agree</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERCompany/Governance/B2_Officer_Appointment_Resolution.html"><span class="code">B2</span>Officer Appt</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERCompany/Governance/B3_Officer_Rotation_Succession_Policy.html"><span class="code">B3</span>Rotation Policy</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERCompany/Governance/B10_Insurance_and_Capital_Policy.html"><span class="code">B10</span>Insurance/Capital</a>
  <div class="nav-group-title">Compliance</div>
  <a class="nav-link" href="PREFIX_PLACEHOLDERCompany/Compliance/B4_Record_Keeping_Policy.html"><span class="code">B4</span>Record Keeping</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERCompany/Compliance/B5_BSA_AML_Program.html"><span class="code">B5</span>BSA/AML</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERCompany/Compliance/B6_IT_Security_Incident_BCP_DRP.html"><span class="code">B6</span>IT/BCP/DRP</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERCompany/Compliance/B7_Acceptable_Client_Use_Policy.html"><span class="code">B7</span>Client Use</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERCompany/Compliance/B8_Privacy_Data_Protection_Policy.html"><span class="code">B8</span>Privacy</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERCompany/Compliance/B9_Fit_and_Proper_Screening_Policy.html"><span class="code">B9</span>Screening</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERCompany/Compliance/B12_Partner_Due_Diligence_Standard.html"><span class="code">B12</span>Partner DD</a>
  <div class="nav-section-title">👥 Client Series</div>
  <div class="nav-group-title">Formation</div>
  <a class="nav-link" href="PREFIX_PLACEHOLDERClient_Series/Formation/A2_Exhibit_A_Series_List.html"><span class="code">A2</span>Series List</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERClient_Series/Formation/A3_Exhibit_B_Series_Operating_Agreements.html"><span class="code">A3</span>Series Op Agree</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERClient_Series/Formation/D1_Articles_of_Amendment_Add_Series.html"><span class="code">D1</span>Amend Series</a>
  <div class="nav-group-title">Client</div>
  <a class="nav-link" href="PREFIX_PLACEHOLDERClient_Series/Client/B11_Client_Services_and_Licensing_Framework.html"><span class="code">B11</span>Client Framework</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERClient_Series/Client/F1_Client_Services_Agreement.html"><span class="code">F1</span>Client Agree</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERClient_Series/Client/F2_End_Customer_Terms_Template.html"><span class="code">F2</span>End Customer</a>
  <div class="nav-group-title">Schedules</div>
  <a class="nav-link" href="PREFIX_PLACEHOLDERClient_Series/Schedule/N1_Partner_MSB_Agreement.html"><span class="code">N1</span>Partner MSB</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERClient_Series/Schedule/N3_Approved_States_Schedule.html"><span class="code">N3</span>States Schedule</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERClient_Series/Schedule/N4_Partner_MSB_Directory.html"><span class="code">N4</span>Partner Directory</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERClient_Series/Schedule/N5_Client_FinCEN_Filing_Guide.html"><span class="code">N5</span>FinCEN Guide</a>
  <div class="nav-section-title">🔒 Internal</div>
  <div class="nav-group-title">Checklists</div>
  <a class="nav-link" href="PREFIX_PLACEHOLDERInternal/Checklist/E1_Filing_Checklist_and_Instructions.html"><span class="code">E1</span>Filing Checklist</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERInternal/Checklist/E2_Securities_and_MTL_Checklist.html"><span class="code">E2</span>Securities/MTL</a>
  <div class="nav-group-title">Registration</div>
  <a class="nav-link" href="PREFIX_PLACEHOLDERInternal/Registration/C1_ABN_Registration_CCASH.html"><span class="code">C1</span>ABN CCASH</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERInternal/Registration/C2_ABN_Template_Client_Series.html"><span class="code">C2</span>ABN Template</a>
  <a class="nav-link" href="PREFIX_PLACEHOLDERInternal/Registration/C3_Pricing_and_Routing_Schedule.html"><span class="code">C3</span>Pricing/Routing</a>
</nav>
NAVEOF
}

# CSS for documents
cat > "$TEMP_DIR/style.css" << 'CSSEOF'
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: "Liberation Serif", "Times New Roman", serif; font-size: 12pt; line-height: 1.5; background: #f8f9fa; }
.nav-sidebar { position: fixed; top: 0; left: 0; width: 260px; height: 100vh; background: #1a365d; color: white; overflow-y: auto; padding: 1rem 0; z-index: 1000; }
.nav-header { padding: 0.75rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.2); margin-bottom: 0.5rem; }
.nav-header .logo { font-size: 1.1rem; font-weight: bold; color: white; text-decoration: none; }
.nav-section-title { color: #90cdf4; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; padding: 0.75rem 1rem 0.25rem; font-family: sans-serif; }
.nav-group-title { color: #a0aec0; font-size: 0.65rem; text-transform: uppercase; padding: 0.3rem 1rem 0.2rem 1.25rem; font-family: sans-serif; }
.nav-link { display: block; color: #e2e8f0; text-decoration: none; padding: 0.3rem 1rem 0.3rem 1.75rem; font-size: 0.8rem; transition: background 0.15s; font-family: sans-serif; }
.nav-link:hover { background: rgba(255,255,255,0.1); }
.nav-link.active { background: #3182ce; font-weight: bold; }
.nav-link .code { color: #90cdf4; font-family: monospace; font-size: 0.75rem; margin-right: 0.3rem; }
.main-content { margin-left: 260px; padding: 2rem 2.5rem; max-width: 900px; background: white; min-height: 100vh; }
header#title-block-header { margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 2px solid #2c5282; }
header#title-block-header h1.title { font-size: 1.5rem; color: #1a365d; }
nav#TOC { background: #f7fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 1rem 1.5rem; margin-bottom: 2rem; }
nav#TOC::before { content: "Contents"; display: block; font-weight: bold; color: #2c5282; margin-bottom: 0.5rem; }
nav#TOC ul { list-style: none; padding-left: 0; }
nav#TOC ul ul { padding-left: 1.5rem; }
nav#TOC li { margin: 0.25rem 0; }
nav#TOC a { color: #3182ce; text-decoration: none; }
nav#TOC a:hover { text-decoration: underline; }
h1, h2, h3, h4 { color: #1a365d; margin-top: 1.5rem; margin-bottom: 0.75rem; }
h1 { font-size: 1.4rem; } h2 { font-size: 1.2rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.3rem; }
h3 { font-size: 1.1rem; } h4 { font-size: 1rem; }
p { margin-bottom: 1rem; text-align: justify; }
ul, ol { margin-bottom: 1rem; padding-left: 2rem; }
li { margin-bottom: 0.25rem; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
th, td { border: 1px solid #cbd5e0; padding: 0.5rem 0.75rem; text-align: left; }
th { background: #edf2f7; font-weight: bold; }
a { color: #3182ce; }
code { background: #edf2f7; padding: 0.1rem 0.3rem; border-radius: 3px; font-family: monospace; font-size: 0.9em; }
blockquote { border-left: 4px solid #3182ce; margin: 1rem 0; padding: 0.5rem 1rem; background: #f7fafc; }
@media print { .nav-sidebar { display: none; } .main-content { margin-left: 0; } }
CSSEOF

process_document() {
    local src="$1"
    local doccode="$2"
    local outpath="${DOC_PATHS[$doccode]}"
    
    [[ -z "$outpath" ]] && { echo "  SKIP: No mapping for $doccode"; return; }
    
    local outdir="$OUTPUT_DIR/$(dirname "$outpath")"
    local outfile="$OUTPUT_DIR/${outpath}.html"
    local tempmd="$TEMP_DIR/${doccode}.md"
    local temphtml="$TEMP_DIR/${doccode}.html"
    
    mkdir -p "$outdir"
    
    # Calculate relative path prefix
    local depth=$(echo "$outpath" | tr -cd '/' | wc -c)
    local prefix=""
    for ((i=0; i<depth; i++)); do prefix="../$prefix"; done
    
    # Copy and clean markdown
    cp "$src" "$tempmd"
    
    # Remove VERSION HISTORY sections
    sed -i '/^##\s*VERSION HISTORY/,/^##[^#]/{ /^##[^#]/!d; }' "$tempmd"
    sed -i '/^##\s*Version History/,/^##[^#]/{ /^##[^#]/!d; }' "$tempmd"
    sed -i '/^###\s*Version History/,/^##/{ /^##/!d; }' "$tempmd"
    
    # Remove schema/metadata comments
    sed -i '/^<!--.*schema:/d' "$tempmd"
    sed -i '/^<!--.*Cross-references:/d' "$tempmd"
    sed -i '/^<!--.*\[FLOW:/d' "$tempmd"
    sed -i '/^<!--.*REMEDIATED/d' "$tempmd"
    sed -i '/^<!--.*\[OBL:/d' "$tempmd"
    
    # Remove edit logs at end
    sed -i '/^##\s*CHANGELOG/,$d' "$tempmd"
    sed -i '/^##\s*Edit Log/,$d' "$tempmd"
    sed -i '/^##\s*Revision History/,$d' "$tempmd"
    sed -i '/^---$/,/^---$/d' "$tempmd"  # Remove YAML frontmatter if any
    
    # Convert [DOC:X] to links (handle both [DOC:X] and [DOC:X §Y])
    for code in "${!DOC_PATHS[@]}"; do
        local target="${DOC_PATHS[$code]}"
        local title="${DOC_TITLES[$code]}"
        # [DOC:X §Y] -> linked with section reference
        sed -i "s|\[DOC:${code} §\([^]]*\)\]|[${code} §\1](${prefix}${target}.html)|g" "$tempmd"
        # [DOC:X] -> linked
        sed -i "s|\[DOC:${code}\]|[${code}](${prefix}${target}.html)|g" "$tempmd"
    done
    
    # Strip marker syntax (keep text)
    sed -i 's/\[TERM:\([^]]*\)\]/\1/g' "$tempmd"
    sed -i 's/\[OBL:\([^]]*\)\]/\1/g' "$tempmd"
    sed -i 's/\[FLOW:\([^]]*\)\]/\1/g' "$tempmd"
    
    # Convert to HTML
    pandoc "$tempmd" -f markdown -t html5 --standalone --number-sections --toc --toc-depth=3 \
        --metadata title="${DOC_TITLES[$doccode]:-$doccode}" \
        --css="${prefix}style.css" \
        -o "$temphtml"
    
    # Generate navigation with correct prefix
    local nav_html=$(generate_nav | sed "s|PREFIX_PLACEHOLDER|$prefix|g")
    
    # Inject navigation and wrapper
    {
        sed -n '1,/<body>/p' "$temphtml"
        echo "$nav_html"
        echo '<div class="main-content">'
        sed -n '/<body>/,/<\/body>/p' "$temphtml" | sed '1d;$d'
        echo '</div>'
        echo '</body>'
        echo '</html>'
    } > "$outfile"
    
    echo "  ✓ $doccode"
}

echo ""
echo "Converting documents..."

cd "$BASE_DIR"

# Process all documents
for f in Company/Overview/*.md Company/Formation/*.md Company/Governance/*.md Company/Compliance/*.md \
         Client_Series/Client/*.md Client_Series/Formation/*.md Client_Series/Schedule/*.md \
         Internal/Checklist/*.md Internal/Registration/*.md; do
    [[ -f "$f" ]] || continue
    bn=$(basename "$f" .md)
    if [[ "$bn" == 00_* ]]; then
        code="$bn"
    else
        code=$(echo "$bn" | sed 's/_.*$//')
    fi
    process_document "$f" "$code"
done

# Copy stylesheet
cp "$TEMP_DIR/style.css" "$OUTPUT_DIR/"

# Copy index (already created separately)
# The index.html should already exist from previous step

echo ""
echo "=== Complete ==="
echo "Output: $OUTPUT_DIR"
echo "Open index.html to browse"

rm -rf "$TEMP_DIR"
