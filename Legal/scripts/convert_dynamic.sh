#!/bin/bash
# convert_dynamic.sh - Dynamic document conversion from central registry
# All document metadata comes from _schema/registry.dat
# Placeholders populated from _schema/data/*.dat

set -e

BASE_DIR="/home/user/CCASH/Series Docs"
REGISTRY="$BASE_DIR/_schema/registry.dat"
DATA_DIR="$BASE_DIR/_schema/data"
OUTPUT_DIR="$BASE_DIR/OUTPUT/Converted/HTML"
TEMP_DIR="$BASE_DIR/OUTPUT/.temp_convert"

# Verify registry exists
[[ -f "$REGISTRY" ]] || { echo "ERROR: Registry not found: $REGISTRY"; exit 1; }

rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR" "$TEMP_DIR"

echo "=== CCASH Dynamic Document Conversion ==="
echo "Registry: $REGISTRY"
echo "Data Dir: $DATA_DIR"
echo ""

# ============================================================================
# STEP 0: Load data from central data files
# ============================================================================

declare -A DATA

# Load company data
if [[ -f "$DATA_DIR/company.dat" ]]; then
    while IFS='=' read -r key value; do
        [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
        DATA["$key"]="$value"
    done < "$DATA_DIR/company.dat"
    echo "Loaded company data: ${#DATA[@]} entries"
fi

# Load fees data
if [[ -f "$DATA_DIR/fees.dat" ]]; then
    while IFS='=' read -r key value; do
        [[ "$key" =~ ^#.*$ || -z "$key" ]] && continue
        DATA["$key"]="$value"
    done < "$DATA_DIR/fees.dat"
    echo "Loaded fees data"
fi

# Load first client for template examples
if [[ -f "$DATA_DIR/clients.dat" ]]; then
    while IFS='|' read -r code name dba ein fincen contact email date status support_email phone address; do
        [[ "$code" =~ ^#.*$ || -z "$code" ]] && continue
        # Store first active client as example
        if [[ "$status" == "active" && -z "${DATA[EXAMPLE_CLIENT_CODE]}" ]]; then
            DATA["EXAMPLE_CLIENT_CODE"]="$code"
            DATA["EXAMPLE_CLIENT_NAME"]="$name"
            DATA["EXAMPLE_CLIENT_DBA"]="$dba"
            DATA["EXAMPLE_CLIENT_EIN"]="$ein"
            DATA["EXAMPLE_CLIENT_FINCEN"]="$fincen"
            DATA["EXAMPLE_CLIENT_CONTACT"]="$contact"
            DATA["EXAMPLE_CLIENT_EMAIL"]="$email"
            DATA["EXAMPLE_CLIENT_DATE"]="$date"
            DATA["EXAMPLE_CLIENT_SUPPORT_EMAIL"]="$support_email"
            DATA["EXAMPLE_CLIENT_PHONE"]="$phone"
            DATA["EXAMPLE_CLIENT_ADDRESS"]="$address"
        fi
    done < "$DATA_DIR/clients.dat"
    echo "Loaded client data"
fi

# ============================================================================
# STEP 1: Load registry into associative arrays
# ============================================================================

declare -A DOC_PATHS DOC_TITLES DOC_CATEGORIES DOC_VERSIONS DOC_DEPS
declare -a DOC_CODES  # Ordered list of codes

while IFS='|' read -r code path title category version deps; do
    # Skip comments and empty lines
    [[ "$code" =~ ^#.*$ || -z "$code" ]] && continue
    
    DOC_CODES+=("$code")
    DOC_PATHS["$code"]="$path"
    DOC_TITLES["$code"]="$title"
    DOC_CATEGORIES["$code"]="$category"
    DOC_VERSIONS["$code"]="$version"
    DOC_DEPS["$code"]="$deps"
done < "$REGISTRY"

echo "Loaded ${#DOC_CODES[@]} documents from registry"

# ============================================================================
# STEP 2: Get git info for all documents
# ============================================================================

declare -A DOC_DATES DOC_HASHES

cd "$BASE_DIR"
for code in "${DOC_CODES[@]}"; do
    src="${DOC_PATHS[$code]}.md"
    if [[ -f "$src" ]]; then
        DOC_HASHES["$code"]=$(git log -1 --format="%h" -- "$src" 2>/dev/null || echo "N/A")
        DOC_DATES["$code"]=$(git log -1 --format="%cs" -- "$src" 2>/dev/null || echo "N/A")
    else
        DOC_HASHES["$code"]="N/A"
        DOC_DATES["$code"]="N/A"
    fi
done

# ============================================================================
# STEP 3: Generate navigation HTML template
# ============================================================================

generate_nav() {
    local prefix="$1"
    
    cat << NAVSTART
<nav class="nav-sidebar">
  <div class="nav-header"><a href="${prefix}index.html" class="logo">📋 CCASH Legal</a></div>
NAVSTART

    # Group documents by category and location
    local current_section="" current_group=""
    
    # Company Overview
    echo '  <div class="nav-section-title">🏢 Company</div>'
    echo '  <div class="nav-group-title">Overview</div>'
    for code in "${DOC_CODES[@]}"; do
        [[ "${DOC_PATHS[$code]}" == Company/Overview/* ]] || continue
        local short=$(echo "${DOC_TITLES[$code]}" | cut -c1-14)
        echo "  <a class=\"nav-link\" href=\"${prefix}${DOC_PATHS[$code]}.html\"><span class=\"code\">${code%%_*}</span>${short}</a>"
    done
    
    # Company Formation
    echo '  <div class="nav-group-title">Formation</div>'
    for code in "${DOC_CODES[@]}"; do
        [[ "${DOC_PATHS[$code]}" == Company/Formation/* ]] || continue
        local short=$(echo "${DOC_TITLES[$code]}" | cut -c1-14)
        echo "  <a class=\"nav-link\" href=\"${prefix}${DOC_PATHS[$code]}.html\"><span class=\"code\">$code</span>${short}</a>"
    done
    
    # Company Governance
    echo '  <div class="nav-group-title">Governance</div>'
    for code in "${DOC_CODES[@]}"; do
        [[ "${DOC_PATHS[$code]}" == Company/Governance/* ]] || continue
        local short=$(echo "${DOC_TITLES[$code]}" | cut -c1-14)
        echo "  <a class=\"nav-link\" href=\"${prefix}${DOC_PATHS[$code]}.html\"><span class=\"code\">$code</span>${short}</a>"
    done
    
    # Company Compliance
    echo '  <div class="nav-group-title">Compliance</div>'
    for code in "${DOC_CODES[@]}"; do
        [[ "${DOC_PATHS[$code]}" == Company/Compliance/* ]] || continue
        local short=$(echo "${DOC_TITLES[$code]}" | cut -c1-14)
        echo "  <a class=\"nav-link\" href=\"${prefix}${DOC_PATHS[$code]}.html\"><span class=\"code\">$code</span>${short}</a>"
    done
    
    # Client Series
    echo '  <div class="nav-section-title">👥 Client Series</div>'
    echo '  <div class="nav-group-title">Formation</div>'
    for code in "${DOC_CODES[@]}"; do
        [[ "${DOC_PATHS[$code]}" == Client_Series/Formation/* ]] || continue
        local short=$(echo "${DOC_TITLES[$code]}" | cut -c1-14)
        echo "  <a class=\"nav-link\" href=\"${prefix}${DOC_PATHS[$code]}.html\"><span class=\"code\">$code</span>${short}</a>"
    done
    
    echo '  <div class="nav-group-title">Client</div>'
    for code in "${DOC_CODES[@]}"; do
        [[ "${DOC_PATHS[$code]}" == Client_Series/Client/* ]] || continue
        local short=$(echo "${DOC_TITLES[$code]}" | cut -c1-14)
        echo "  <a class=\"nav-link\" href=\"${prefix}${DOC_PATHS[$code]}.html\"><span class=\"code\">$code</span>${short}</a>"
    done
    
    echo '  <div class="nav-group-title">Schedules</div>'
    for code in "${DOC_CODES[@]}"; do
        [[ "${DOC_PATHS[$code]}" == Client_Series/Schedule/* ]] || continue
        local short=$(echo "${DOC_TITLES[$code]}" | cut -c1-14)
        echo "  <a class=\"nav-link\" href=\"${prefix}${DOC_PATHS[$code]}.html\"><span class=\"code\">$code</span>${short}</a>"
    done
    
    # Internal
    echo '  <div class="nav-section-title">🔒 Internal</div>'
    echo '  <div class="nav-group-title">Checklists</div>'
    for code in "${DOC_CODES[@]}"; do
        [[ "${DOC_PATHS[$code]}" == Internal/Checklist/* ]] || continue
        local short=$(echo "${DOC_TITLES[$code]}" | cut -c1-14)
        echo "  <a class=\"nav-link\" href=\"${prefix}${DOC_PATHS[$code]}.html\"><span class=\"code\">$code</span>${short}</a>"
    done
    
    echo '  <div class="nav-group-title">Registration</div>'
    for code in "${DOC_CODES[@]}"; do
        [[ "${DOC_PATHS[$code]}" == Internal/Registration/* ]] || continue
        local short=$(echo "${DOC_TITLES[$code]}" | cut -c1-14)
        echo "  <a class=\"nav-link\" href=\"${prefix}${DOC_PATHS[$code]}.html\"><span class=\"code\">$code</span>${short}</a>"
    done
    
    echo '</nav>'
}

# ============================================================================
# STEP 4: Generate CSS
# ============================================================================

cat > "$OUTPUT_DIR/style.css" << 'CSSEOF'
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: "Liberation Serif", "Times New Roman", serif; font-size: 12pt; line-height: 1.5; background: #f8f9fa; }
.nav-sidebar { position: fixed; top: 0; left: 0; width: 260px; height: 100vh; background: #1a365d; color: white; overflow-y: auto; padding: 1rem 0; z-index: 1000; }
.nav-header { padding: 0.75rem 1rem; border-bottom: 1px solid rgba(255,255,255,0.2); margin-bottom: 0.5rem; }
.nav-header .logo { font-size: 1.1rem; font-weight: bold; color: white; text-decoration: none; }
.nav-section-title { color: #90cdf4; font-size: 0.7rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px; padding: 0.75rem 1rem 0.25rem; font-family: sans-serif; }
.nav-group-title { color: #a0aec0; font-size: 0.65rem; text-transform: uppercase; padding: 0.3rem 1rem 0.2rem 1.25rem; font-family: sans-serif; }
.nav-link { display: block; color: #e2e8f0; text-decoration: none; padding: 0.3rem 1rem 0.3rem 1.75rem; font-size: 0.8rem; transition: background 0.15s; font-family: sans-serif; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
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
.doc-code { font-family: monospace; font-weight: bold; color: #2c5282; background: #edf2f7; padding: 0.1rem 0.35rem; border-radius: 3px; font-size: 0.85rem; }
.doc-link { color: #2c5282; text-decoration: none; font-weight: 500; }
.doc-link:hover { text-decoration: underline; }
.version { font-family: monospace; color: #718096; font-size: 0.9rem; }
.date { color: #4a5568; white-space: nowrap; font-size: 0.9rem; }
.hash { font-family: monospace; font-size: 0.75rem; color: #a0aec0; background: #f7fafc; padding: 0.1rem 0.25rem; border-radius: 2px; }
.category { font-size: 0.65rem; padding: 0.1rem 0.35rem; border-radius: 3px; font-weight: 500; text-transform: uppercase; font-family: sans-serif; }
.cat-formation { background: #c6f6d5; color: #276749; }
.cat-governance { background: #bee3f8; color: #2c5282; }
.cat-compliance { background: #feebc8; color: #c05621; }
.cat-client { background: #e9d8fd; color: #6b46c1; }
.cat-schedule { background: #e9d8fd; color: #6b46c1; }
.cat-internal { background: #fed7d7; color: #c53030; }
.cat-overview { background: #e2e8f0; color: #4a5568; }
@media print { .nav-sidebar { display: none; } .main-content { margin-left: 0; } }
CSSEOF

# ============================================================================
# STEP 5: Process each document
# ============================================================================

process_document() {
    local code="$1"
    local path="${DOC_PATHS[$code]}"
    local title="${DOC_TITLES[$code]}"
    local src="$BASE_DIR/${path}.md"
    
    [[ -f "$src" ]] || { echo "  SKIP: Source not found for $code"; return; }
    
    local outdir="$OUTPUT_DIR/$(dirname "$path")"
    local outfile="$OUTPUT_DIR/${path}.html"
    local tempmd="$TEMP_DIR/${code}.md"
    local temphtml="$TEMP_DIR/${code}.html"
    
    mkdir -p "$outdir"
    
    # Calculate relative path prefix
    local depth=$(echo "$path" | tr -cd '/' | wc -c)
    local prefix=""
    for ((i=0; i<depth; i++)); do prefix="../$prefix"; done
    
    # Copy and clean markdown
    cp "$src" "$tempmd"
    
    # Remove VERSION HISTORY sections (multiple patterns)
    # Pattern: ## VERSION HISTORY followed by table until next ## or end
    perl -i -0pe 's/##\s*VERSION HISTORY.*?(?=\n##[^#]|\n#[^#]|\Z)//gs' "$tempmd"
    perl -i -0pe 's/##\s*Version History.*?(?=\n##[^#]|\n#[^#]|\Z)//gs' "$tempmd"
    perl -i -0pe 's/###\s*Version History.*?(?=\n##|\n#[^#]|\Z)//gs' "$tempmd"
    
    # Remove CHANGELOG / Edit Log sections at end
    perl -i -0pe 's/##\s*CHANGELOG.*//gs' "$tempmd"
    perl -i -0pe 's/##\s*Edit Log.*//gs' "$tempmd"
    perl -i -0pe 's/##\s*Revision History.*//gs' "$tempmd"
    
    # Remove schema/metadata comments
    sed -i '/^<!--.*schema:/d' "$tempmd"
    sed -i '/^<!--.*Cross-references:/d' "$tempmd"
    sed -i '/^<!--.*\[FLOW:/d' "$tempmd"
    sed -i '/^<!--.*REMEDIATED/d' "$tempmd"
    sed -i '/^<!--.*\[OBL:/d' "$tempmd"
    sed -i '/^<!--/d' "$tempmd"
    
    # Fix standalone [DOC:X] on their own lines - append to previous line with "See "
    # Pattern: line ending, then [DOC:X] alone on next line
    perl -i -0pe 's/\.\n+\[DOC:([^\]]+)\]\n/. See [DOC:\1].\n/g' "$tempmd"
    perl -i -0pe 's/([^.\n])\n+\[DOC:([^\]]+)\]\n/\1 (see [DOC:\2]).\n/g' "$tempmd"
    
    # Convert [DOC:X] and [DOC:X §Y] to links - use registry data
    for target_code in "${DOC_CODES[@]}"; do
        local target_path="${DOC_PATHS[$target_code]}"
        # [DOC:X §Y] with section
        sed -i "s|\[DOC:${target_code} §\([^]]*\)\]|[${target_code} §\1](${prefix}${target_path}.html)|g" "$tempmd"
        # [DOC:X] plain
        sed -i "s|\[DOC:${target_code}\]|[${target_code}](${prefix}${target_path}.html)|g" "$tempmd"
    done
    
    # ========================================================================
    # TERM MARKER PROCESSING
    # Pattern A: [TERM:X] DISPLAY TEXT - strip marker, keep display text
    # Pattern B: [TERM:X] standalone - convert marker to readable name
    # ========================================================================
    
    # Strip markers that have uppercase display text following (Pattern A)
    # e.g., [TERM:Series_T1] SERIES T-1 → SERIES T-1
    sed -i 's/\[TERM:[^]]*\] \([A-Z]\)/\1/g' "$tempmd"
    
    # Officer titles - standalone (no display text following)
    sed -i 's/\[TERM:CEO\]/CEO/g' "$tempmd"
    sed -i 's/\[TERM:CFO\]/CFO/g' "$tempmd"
    sed -i 's/\[TERM:CTO\]/CTO/g' "$tempmd"
    sed -i 's/\[TERM:CCO\]/CCO/g' "$tempmd"
    sed -i 's/\[TERM:CMO\]/CMO/g' "$tempmd"
    sed -i 's/\[TERM:COO\]/COO/g' "$tempmd"
    
    # Series terms - standalone
    sed -i 's/\[TERM:Series_T1\]/Treasury Series (T-1)/g' "$tempmd"
    sed -i 's/\[TERM:Series_T2\]/Crypto Custody Series (T-2)/g' "$tempmd"
    sed -i 's/\[TERM:Series_T3\]/Operational Expenses Series (T-3)/g' "$tempmd"
    sed -i 's/\[TERM:Series_T4\]/Technology Infrastructure Series (T-4)/g' "$tempmd"
    sed -i 's/\[TERM:Series_T5\]/Series T-5/g' "$tempmd"
    sed -i 's/\[TERM:Series_P1\]/Compliance Series (P-1)/g' "$tempmd"
    sed -i 's/\[TERM:Series_P2\]/Pricing Series (P-2)/g' "$tempmd"
    sed -i 's/\[TERM:Series_B1\]/Brand Licensing Series (B-1)/g' "$tempmd"
    sed -i 's/\[TERM:Series_B2\]/Platform IP Series (B-2)/g' "$tempmd"
    
    # Context-aware entity term replacement
    # "of the [TERM:Company]" → "of the Company" (not "of the the Company")
    sed -i 's/of the \[TERM:Company\]/of the Company/g' "$tempmd"
    sed -i 's/of the \[TERM:Manager\]/of the Manager/g' "$tempmd"
    sed -i 's/of the \[TERM:Officers\]/of the Officers/g' "$tempmd"
    
    # "other [TERM:Officers]" → "other Officers" (not "other the Officers")
    sed -i 's/other \[TERM:Officers\]/other Officers/g' "$tempmd"
    sed -i 's/other \[TERM:Series\]/other Series/g' "$tempmd"
    
    # "any [TERM:X]" → "any X"
    sed -i 's/any \[TERM:Company\]/any Company/g' "$tempmd"
    sed -i 's/any \[TERM:Series\]/any Series/g' "$tempmd"
    sed -i 's/any \[TERM:Member\]/any Member/g' "$tempmd"
    sed -i 's/any \[TERM:Manager\]/any Manager/g' "$tempmd"
    
    # "each [TERM:X]" → "each X" (singular!)
    sed -i 's/[Ee]ach \[TERM:Officers\]/each Officer/g' "$tempmd"
    sed -i 's/each \[TERM:Series\]/each Series/g' "$tempmd"
    sed -i 's/each \[TERM:Member\]/each Member/g' "$tempmd"
    
    # "requires [TERM:Manager]" → "requires Manager" (not "requires the Manager")
    sed -i 's/requires \[TERM:Manager\]/requires Manager/g' "$tempmd"
    sed -i 's/prior \[TERM:Manager\]/prior Manager/g' "$tempmd"
    
    # "the [TERM:Officers]'" → "the Officers'" (possessive after the)
    sed -i "s/the \[TERM:Officers\]'/the Officers'/g" "$tempmd"
    
    # Possessive forms
    sed -i "s/\[TERM:Company\]'s/the Company's/g" "$tempmd"
    sed -i "s/\[TERM:Officers\]'s/the Officers'/g" "$tempmd"
    sed -i "s/\[TERM:Manager\]'s/the Manager's/g" "$tempmd"
    
    # Standalone at sentence start or after period - add "the"
    sed -i 's/\. \[TERM:Company\]/. The Company/g' "$tempmd"
    sed -i 's/\. \[TERM:Manager\]/. The Manager/g' "$tempmd"
    sed -i 's/\. \[TERM:Officers\]/. The Officers/g' "$tempmd"
    
    # Generic standalone (not after "the", "of the", "other", "any", "each")
    # Just strip the marker, keep what follows or use term name
    sed -i 's/\[TERM:Company\]/the Company/g' "$tempmd"
    sed -i 's/\[TERM:Manager\]/the Manager/g' "$tempmd"
    sed -i 's/\[TERM:Member\]/Member/g' "$tempmd"
    sed -i 's/\[TERM:Series\]/Series/g' "$tempmd"
    sed -i 's/\[TERM:Officers\]/Officers/g' "$tempmd"
    
    # Clean up any remaining TERM markers (catch-all)
    sed -i 's/\[TERM:[^]]*\] *//g' "$tempmd"
    sed -i 's/\[OBL:[^]]*\] *//g' "$tempmd"
    sed -i 's/\[FLOW:[^]]*\] *//g' "$tempmd"
    
    # ========================================================================
    # ROLE MARKER SUBSTITUTION
    # ========================================================================
    
    # Company officers - display names
    sed -i "s|\[ROLE:company.ceo.display_name\]|${DATA[CEO_NAME]:-John A. Smith}|g" "$tempmd"
    sed -i "s|\[ROLE:company.cfo.display_name\]|${DATA[CFO_NAME]:-Jane B. Doe}|g" "$tempmd"
    sed -i "s|\[ROLE:company.cto.display_name\]|${DATA[CTO_NAME]:-Sarah D. Williams}|g" "$tempmd"
    sed -i "s|\[ROLE:company.cco.display_name\]|${DATA[CCO_NAME]:-Robert C. Johnson}|g" "$tempmd"
    sed -i "s|\[ROLE:company.cmo.display_name\]|${DATA[CMO_NAME]:-Michael E. Brown}|g" "$tempmd"
    
    # Company officers - addresses
    sed -i "s|\[ROLE:company.ceo.address_formatted\]|${DATA[CEO_ADDRESS]:-456 Oak Avenue, Billings, MT 59101}|g" "$tempmd"
    sed -i "s|\[ROLE:company.cfo.address_formatted\]|${DATA[CFO_ADDRESS]:-789 Pine Street, Helena, MT 59601}|g" "$tempmd"
    sed -i "s|\[ROLE:company.cto.address_formatted\]|${DATA[CTO_ADDRESS]:-654 Maple Court, Missoula, MT 59801}|g" "$tempmd"
    sed -i "s|\[ROLE:company.cco.address_formatted\]|${DATA[CCO_ADDRESS]:-321 Elm Drive, Great Falls, MT 59401}|g" "$tempmd"
    sed -i "s|\[ROLE:company.cmo.address_formatted\]|${DATA[CMO_ADDRESS]:-987 Cedar Lane, Bozeman, MT 59715}|g" "$tempmd"
    
    # Manager (same as CEO for this company)
    sed -i "s|\[ROLE:company.manager.display_name\]|${DATA[CEO_NAME]:-John A. Smith}|g" "$tempmd"
    sed -i "s|\[ROLE:company.manager.address_formatted\]|${DATA[CEO_ADDRESS]:-456 Oak Avenue, Billings, MT 59101}|g" "$tempmd"
    
    # Organizer / Initial Member
    sed -i "s|\[ROLE:company.organizer.display_name\]|${DATA[ORGANIZER_NAME]:-John A. Smith}|g" "$tempmd"
    sed -i "s|\[ROLE:company.organizer.address_formatted\]|${DATA[ORGANIZER_ADDRESS]:-456 Oak Avenue}, ${DATA[ORGANIZER_CITY]:-Billings}, ${DATA[ORGANIZER_STATE]:-MT} ${DATA[ORGANIZER_ZIP]:-59101}|g" "$tempmd"
    sed -i "s|\[ROLE:company.member.display_name\]|${DATA[ORGANIZER_NAME]:-John A. Smith}|g" "$tempmd"
    sed -i "s|\[ROLE:company.member.address_formatted\]|${DATA[ORGANIZER_ADDRESS]:-456 Oak Avenue}, ${DATA[ORGANIZER_CITY]:-Billings}, ${DATA[ORGANIZER_STATE]:-MT} ${DATA[ORGANIZER_ZIP]:-59101}|g" "$tempmd"
    sed -i "s|\[ROLE:company.member.ownership_percentage\]|${DATA[INITIAL_MEMBER_OWNERSHIP_PERCENT]:-100}|g" "$tempmd"
    
    # Registered agent
    sed -i "s|\[ROLE:company.registered_agent.display_name\]|${DATA[REG_AGENT_NAME]:-InCorp Services Inc.}|g" "$tempmd"
    sed -i "s|\[ROLE:company.registered_agent.address_formatted\]|${DATA[REG_AGENT_STREET]:-3755 Avondale Ln}, ${DATA[REG_AGENT_CITY]:-Billings}, MT ${DATA[REG_AGENT_ZIP]:-59101}|g" "$tempmd"
    
    # Clean up any remaining ROLE markers (catch-all fallback)
    sed -i 's/\[ROLE:[^]]*\]/[ROLE NOT FOUND]/g' "$tempmd"
    
    # ========================================================================
    # CONFIG MARKER SUBSTITUTION
    # ========================================================================
    
    # Principal office address
    sed -i "s|\[CONFIG:company.principal_office.street\]|${DATA[PRINCIPAL_STREET]:-100 Main Street}|g" "$tempmd"
    sed -i "s|\[CONFIG:company.principal_office.city\]|${DATA[PRINCIPAL_CITY]:-Billings}|g" "$tempmd"
    sed -i "s|\[CONFIG:company.principal_office.state\]|${DATA[PRINCIPAL_STATE]:-MT}|g" "$tempmd"
    sed -i "s|\[CONFIG:company.principal_office.zip\]|${DATA[PRINCIPAL_ZIP]:-59101}|g" "$tempmd"
    
    # Mailing address
    sed -i "s|\[CONFIG:company.mailing_address.street\]|${DATA[MAILING_STREET]:-PO Box 1234}|g" "$tempmd"
    sed -i "s|\[CONFIG:company.mailing_address.city\]|${DATA[MAILING_CITY]:-Billings}|g" "$tempmd"
    sed -i "s|\[CONFIG:company.mailing_address.state\]|${DATA[MAILING_STATE]:-MT}|g" "$tempmd"
    sed -i "s|\[CONFIG:company.mailing_address.zip\]|${DATA[MAILING_ZIP]:-59101}|g" "$tempmd"
    
    # Contact info
    sed -i "s|\[CONFIG:company.phone\]|${DATA[COMPANY_PHONE]:-1-406-555-0100}|g" "$tempmd"
    sed -i "s|\[CONFIG:company.email\]|${DATA[COMPANY_EMAIL]:-legal@ccash.io}|g" "$tempmd"
    sed -i "s|\[CONFIG:company.formation_date\]|${DATA[COMPANY_FORMATION_DATE]:-2024-01-15}|g" "$tempmd"
    
    # Clean up any remaining CONFIG markers
    sed -i 's/\[CONFIG:[^]]*\]/[CONFIG NOT FOUND]/g' "$tempmd"
    
    # ========================================================================
    # RIGHT/DECISION/SOURCE MARKER CLEANUP
    # ========================================================================
    
    # These markers are for schema reference - remove them from output
    sed -i 's/\[RIGHT:[^]]*\]//g' "$tempmd"
    sed -i 's/\[DECISION:[^]]*\]//g' "$tempmd"
    sed -i 's/\[SOURCE:[^]]*\]//g' "$tempmd"
    
    # ========================================================================
    # STATUS MARKERS - Convert to styled text
    # ========================================================================
    
    # [REQUIRED] and [RECOMMENDED] are intentional status indicators - keep as styled
    sed -i 's/\[REQUIRED\]/**[REQUIRED]**/g' "$tempmd"
    sed -i 's/\[RECOMMENDED\]/**[RECOMMENDED]**/g' "$tempmd"
    
    # ========================================================================
    # GENERIC PLACEHOLDER MARKERS
    # ========================================================================
    
    # Registered agent placeholder (MUST come before generic [City] replacement)
    # This handles the full noncommercial registered agent address pattern
    sed -i "s|agent is \[________________\], with a physical address in Montana at \[________________\], \[City\], Montana \[ZIP\], and a mailing address at \[________________\], \[City\], Montana \[ZIP\]|agent is ${DATA[REG_AGENT_NAME]:-Northwest Registered Agent LLC}, with a physical address in Montana at ${DATA[REG_AGENT_ADDRESS]:-2030 11th Ave N}, ${DATA[REG_AGENT_CITY]:-Great Falls}, Montana ${DATA[REG_AGENT_ZIP]:-59401}, and a mailing address at ${DATA[REG_AGENT_ADDRESS]:-2030 11th Ave N}, ${DATA[REG_AGENT_CITY]:-Great Falls}, Montana ${DATA[REG_AGENT_ZIP]:-59401}|g" "$tempmd"
    
    # Business mailing address pattern (MUST come before generic [City] replacement)
    sed -i "s|business mailing address is \[________________\], \[City\], \[State\] \[ZIP\]|business mailing address is ${DATA[MAILING_STREET]:-PO Box 1234}, ${DATA[MAILING_CITY]:-Helena}, ${DATA[MAILING_STATE]:-MT} ${DATA[MAILING_ZIP]:-59601}|g" "$tempmd"
    
    # Address component placeholders
    sed -i "s|\[ZIP\]|${DATA[PRINCIPAL_ZIP]:-59101}|g" "$tempmd"
    sed -i "s|\[STATE\]|${DATA[PRINCIPAL_STATE]:-MT}|g" "$tempmd"
    sed -i "s|\[State\]|${DATA[PRINCIPAL_STATE]:-MT}|g" "$tempmd"
    sed -i "s|\[City\]|${DATA[PRINCIPAL_CITY]:-Billings}|g" "$tempmd"
    sed -i "s|\[AMOUNT\]|[Amount to be determined]|g" "$tempmd"
    
    # Partner MSB template placeholders (keep as template markers)
    sed -i "s|\[PARTNER MSB NAME\]|[Partner MSB Name]|g" "$tempmd"
    sed -i "s|\[PARTNER MSB LEGAL NAME\]|[Partner MSB Legal Name]|g" "$tempmd"
    
    # Client/Series template placeholders - fill with example data
    sed -i "s|\[Series Name\]|${DATA[EXAMPLE_CLIENT_NAME]:-Example Client LLC}|g" "$tempmd"
    sed -i "s|\[Client Series Name\]|${DATA[EXAMPLE_CLIENT_NAME]:-Example Client LLC}|g" "$tempmd"
    sed -i "s|\[Client Series\]|${DATA[EXAMPLE_CLIENT_CODE]:-C-001}|g" "$tempmd"
    sed -i "s|\[Client Brand\]|${DATA[EXAMPLE_CLIENT_DBA]:-Example Brand}|g" "$tempmd"
    
    # Generic name/address/date placeholders in signature blocks - keep blank
    sed -i 's|\[Name\]|[Name]|g' "$tempmd"
    sed -i 's|\[Address\]|[Address]|g' "$tempmd"
    sed -i 's|\[Date\]|[Date]|g' "$tempmd"
    sed -i 's|\[Email\]|[Email]|g' "$tempmd"
    
    # Time/date range placeholders
    sed -i 's|\[Start Date\]|[Start Date]|g' "$tempmd"
    sed -i 's|\[End Date\]|[End Date]|g' "$tempmd"
    sed -i 's|\[TIME PERIOD\]|[Time Period]|g' "$tempmd"
    
    # Signature title placeholders
    sed -i 's|\[CEO / Authorized Officer\]|Managing Member|g' "$tempmd"
    sed -i 's|\[Authorized Representative\]|Authorized Representative|g' "$tempmd"
    sed -i 's|\[Designation\]|Managing Member|g' "$tempmd"
    
    # Option placeholders - pick sensible defaults
    sed -i 's|\[does / does not\]|does|g' "$tempmd"
    sed -i 's|\[Wire/ACH\]|ACH|g' "$tempmd"
    
    # Section reference placeholders
    sed -i 's|\[X\.X\]|[See Section]|g' "$tempmd"
    
    # Description placeholders - keep as template
    sed -i 's|\[Describe your services\]|[Description of Services]|g' "$tempmd"
    sed -i 's|\[Describe your fee structure\]|[Fee Structure Description]|g' "$tempmd"
    
    # Email placeholders - use actual emails
    sed -i "s|\[support@ccash.us\]|support@ccash.us|g" "$tempmd"
    sed -i "s|\[operations@ccash.us\]|operations@ccash.us|g" "$tempmd"
    sed -i "s|\[compliance@ccash.us\]|compliance@ccash.us|g" "$tempmd"
    
    # Checkbox placeholders - remove brackets
    sed -i 's/\[ \]/☐/g' "$tempmd"
    sed -i 's/\[x\]/☑/g' "$tempmd"
    sed -i 's/\[X\]/☑/g' "$tempmd"
    
    # Short underscore placeholders in brackets
    sed -i 's/\[________\]/________/g' "$tempmd"
    
    # Numeric placeholders - remove brackets but keep number
    sed -i 's/\[10\]/10/g' "$tempmd"
    sed -i 's/\[2\]/2/g' "$tempmd"
    sed -i 's/\[5\]/5/g' "$tempmd"
    sed -i 's/\[30\]/30/g' "$tempmd"
    sed -i 's/\[5-10\]/5-10/g' "$tempmd"
    
    # CFR references - remove brackets but keep reference
    sed -i 's/\[31 CFR Part 501\]/31 CFR Part 501/g' "$tempmd"
    sed -i 's/\[31 CFR §1010.410(f)\]/31 CFR §1010.410(f)/g' "$tempmd"
    
    # Status markers
    sed -i 's/\[None currently approved\]/None currently approved/g' "$tempmd"
    
    # Fix double "the the" that might have been created
    sed -i 's/the the /the /g' "$tempmd"
    sed -i 's/The the /The /g' "$tempmd"
    
    # Fix "Officers's" → "Officers'"
    sed -i "s/Officers's/Officers'/g" "$tempmd"
    
    # Fix lowercase sentence starts
    sed -i 's/^each Officer/Each Officer/g' "$tempmd"
    sed -i 's/\. each Officer/. Each Officer/g' "$tempmd"
    perl -i -pe 's/^(\d+\.\d+\.\d*\.?) each Officer/$1 Each Officer/g' "$tempmd"
    
    # ========================================================================
    # PLACEHOLDER SUBSTITUTION
    # ========================================================================
    
    # Specific officer appointments (match context from B2 document)
    # CEO - 2.1
    sed -i "s|Chief Executive Officer is \[________________\], with an address at \[________________\]|Chief Executive Officer is ${DATA[CEO_NAME]}, with an address at ${DATA[CEO_ADDRESS]}|g" "$tempmd"
    # CTO - 2.3
    sed -i "s|Chief Technology Officer is \[________________\], with an address at \[________________\]|Chief Technology Officer is ${DATA[CTO_NAME]}, with an address at ${DATA[CTO_ADDRESS]}|g" "$tempmd"
    # CMO - 2.4
    sed -i "s|Chief Marketing Officer is \[________________\], with an address at \[________________\]|Chief Marketing Officer is ${DATA[CMO_NAME]}, with an address at ${DATA[CMO_ADDRESS]}|g" "$tempmd"
    # CFO - 2.5
    sed -i "s|Chief Financial Officer is \[________________\], with an address at \[________________\]|Chief Financial Officer is ${DATA[CFO_NAME]}, with an address at ${DATA[CFO_ADDRESS]}|g" "$tempmd"
    # CCO - 2.6
    sed -i "s|Chief Compliance Officer, who also serves as the BSA/AML Officer, is \[________________\], with an address at \[________________\]|Chief Compliance Officer, who also serves as the BSA/AML Officer, is ${DATA[CCO_NAME]}, with an address at ${DATA[CCO_ADDRESS]}|g" "$tempmd"
    
    # Generic officer placeholder (fallback)
    sed -i "s|\[________________\], with an address at \[________________\]|${DATA[CEO_NAME]:-[NAME]}, with an address at ${DATA[PRINCIPAL_FULL]:-[ADDRESS]}|g" "$tempmd"
    
    # ========================================================================
    # FINANCIAL THRESHOLDS AND AMOUNTS
    # ========================================================================
    
    # Contract/hiring/capex thresholds (B2 Section 4)
    sed -i "s|contract with a value exceeding \[________________\] dollars|contract with a value exceeding ${DATA[CONTRACT_THRESHOLD]:-25,000} dollars|g" "$tempmd"
    sed -i "s|hiring with annual compensation exceeding \[________________\] dollars|hiring with annual compensation exceeding ${DATA[HIRING_THRESHOLD]:-75,000} dollars|g" "$tempmd"
    sed -i "s|capital expenditure exceeding \[________________\] dollars|capital expenditure exceeding ${DATA[CAPEX_THRESHOLD]:-10,000} dollars|g" "$tempmd"
    
    # Officer salaries (B2 Section 5)
    sed -i "s|base salary of \[________________\] dollars|base salary of ${DATA[CEO_SALARY]:-150,000} dollars|g" "$tempmd"
    sed -i "s|\[________________\] dollars, plus such other compensation|${DATA[CEO_SALARY]:-150,000} dollars, plus such other compensation|g" "$tempmd"
    
    # Capital contributions
    sed -i "s|capital contribution of \[________________\]|capital contribution of \$${DATA[CAPITAL_CONTRIBUTION]:-100,000}|g" "$tempmd"
    sed -i 's|\$\[________________\]|\$100,000|g' "$tempmd"
    
    # Signature blocks - fill with Manager name
    sed -i "s|Printed Name: \[________________\]|Printed Name: ${DATA[CEO_NAME]:-John A. Smith}|g" "$tempmd"
    sed -i "s|Title: \[________________\]|Title: Managing Member|g" "$tempmd"
    
    # ========================================================================
    # CONTACT AND ADDRESS PLACEHOLDERS
    # ========================================================================
    
    # Phone/email/address patterns
    sed -i "s|telephone number is \[________________\]|telephone number is ${DATA[COMPANY_PHONE]:-(406) 555-0100}|g" "$tempmd"
    sed -i "s|daytime telephone number is ________________|daytime telephone number is ${DATA[COMPANY_PHONE]:-(406) 555-0100}|g" "$tempmd"
    sed -i "s|email address is \[________________\]|email address is ${DATA[COMPANY_EMAIL]:-legal@ccash.io}|g" "$tempmd"
    sed -i "s|email address is ________________|email address is ${DATA[COMPANY_EMAIL]:-legal@ccash.io}|g" "$tempmd"
    
    # Mailing address pattern
    sed -i "s|mailing address is \[________________\], \[City\]|mailing address is ${DATA[PRINCIPAL_ADDRESS]}, ${DATA[PRINCIPAL_CITY]}|g" "$tempmd"
    sed -i "s|mailing address is ________________, \[City\]|mailing address is ${DATA[PRINCIPAL_ADDRESS]}, ${DATA[PRINCIPAL_CITY]}|g" "$tempmd"
    
    # Initial member patterns
    sed -i "s|initial member of this series is \[________________\]|initial member of this series is ${DATA[ORGANIZER_NAME]}|g" "$tempmd"
    sed -i "s|initial member of this series is ________________|initial member of this series is ${DATA[ORGANIZER_NAME]}|g" "$tempmd"
    sed -i "s|Member type is \[________________\]|Member type is ${DATA[INITIAL_MEMBER_TYPE]:-Individual}|g" "$tempmd"
    sed -i "s|Member type is ________________|Member type is ${DATA[INITIAL_MEMBER_TYPE]:-Individual}|g" "$tempmd"
    sed -i "s|Member jurisdiction is \[________________\]|Member jurisdiction is ${DATA[INITIAL_MEMBER_JURISDICTION]:-Montana}|g" "$tempmd"
    sed -i "s|Member jurisdiction is ________________|Member jurisdiction is ${DATA[INITIAL_MEMBER_JURISDICTION]:-Montana}|g" "$tempmd"
    
    # Client-specific form fields
    sed -i "s|client legal name is \[________________\]|client legal name is ${DATA[EXAMPLE_CLIENT_NAME]:-ABC Payments LLC}|g" "$tempmd"
    sed -i "s|client legal name is ________________|client legal name is ${DATA[EXAMPLE_CLIENT_NAME]:-ABC Payments LLC}|g" "$tempmd"
    sed -i "s|client jurisdiction is \[________________\]|client jurisdiction is Delaware|g" "$tempmd"
    sed -i "s|client jurisdiction is ________________|client jurisdiction is Delaware|g" "$tempmd"
    sed -i "s|client services agreement date is \[________________\]|client services agreement date is ${DATA[EXAMPLE_CLIENT_DATE]:-2024-03-01}|g" "$tempmd"
    sed -i "s|client services agreement date is ________________|client services agreement date is ${DATA[EXAMPLE_CLIENT_DATE]:-2024-03-01}|g" "$tempmd"
    
    # Filing dates
    sed -i "s|effective on \[________________\]|effective on ${DATA[COMPANY_FORMATION_DATE]:-2024-01-15}|g" "$tempmd"
    sed -i "s|effective on ________________|effective on ${DATA[COMPANY_FORMATION_DATE]:-2024-01-15}|g" "$tempmd"
    sed -i "s|filed with ________________|filed with the Montana Secretary of State|g" "$tempmd"
    sed -i "s|\[________________\] (Date the original|${DATA[COMPANY_FORMATION_DATE]:-2024-01-15} (Date the original|g" "$tempmd"
    sed -i "s|________________ (Date the original|${DATA[COMPANY_FORMATION_DATE]:-2024-01-15} (Date the original|g" "$tempmd"
    
    # Agreement dates - fill with placeholder format (with brackets first, then without)
    sed -i "s|\[________________\], 20___|[Date to be completed]|g" "$tempmd"
    sed -i "s|________________, 20___|[Date to be completed]|g" "$tempmd"
    sed -i "s|\[________________\], 20_|[Date to be completed]|g" "$tempmd"
    sed -i "s|________________, 20_|[Date to be completed]|g" "$tempmd"
    sed -i "s|________________, 2025|January 15, 2025|g" "$tempmd"
    
    # Partner MSB placeholders
    sed -i "s|\[____________________\]|[To Be Completed]|g" "$tempmd"
    sed -i "s|\[____________________________\]|[To Be Completed]|g" "$tempmd"
    
    # Signature blocks with Name:/By:/Title: patterns - fill from data
    # Must handle both bracketed and non-bracketed versions
    sed -i "s|Name: \[________________\]|Name: ${DATA[CEO_NAME]:-John A. Smith}|g" "$tempmd"
    sed -i "s|Name: ________________|Name: ${DATA[CEO_NAME]:-John A. Smith}|g" "$tempmd"
    sed -i "s|Name: _________________________|Name: ${DATA[CEO_NAME]:-John A. Smith}|g" "$tempmd"
    sed -i "s|Title: \[________________\]|Title: Managing Member|g" "$tempmd"
    sed -i "s|Title: _____________|Title: Managing Member|g" "$tempmd"
    sed -i "s|Email: \[________________\]|Email: ${DATA[COMPANY_EMAIL]:-legal@ccash.io}|g" "$tempmd"
    sed -i "s|Email: ________________|Email: ${DATA[COMPANY_EMAIL]:-legal@ccash.io}|g" "$tempmd"
    
    # Entity ID from Montana SOS
    sed -i "s|entity ID number from the Montana Secretary of State is ________________|entity ID number from the Montana Secretary of State is ${DATA[MT_SOS_ID]:-E1234567}|g" "$tempmd"
    sed -i "s|entity ID number from the Montana Secretary of State is \[________________\]|entity ID number from the Montana Secretary of State is ${DATA[MT_SOS_ID]:-E1234567}|g" "$tempmd"
    
    # Adopted date (multiple patterns)
    sed -i "s|\*\*Adopted:\*\* \[________________\], 2025|**Adopted:** January 15, 2025|g" "$tempmd"
    sed -i "s|Adopted:\*\* ________________, 2025|Adopted:** January 15, 2025|g" "$tempmd"
    sed -i 's|Adopted:</strong> ________________, 2025|Adopted:</strong> January 15, 2025|g' "$tempmd"
    sed -i 's|\*\*Adopted:\*\* ________________, 2025|**Adopted:** January 15, 2025|g' "$tempmd"
    
    # By: and Address lines should stay as signature blanks (30 underscores = signature line)
    # Keep these as visual blanks since they're meant for actual signatures
    
    # Generic remaining [________________] brackets - convert to visual underlines
    sed -i "s|\[________________\]|________________|g" "$tempmd"
    
    # Company placeholders
    sed -i "s|\[COMPANY_NAME\]|${DATA[COMPANY_LEGAL_NAME]}|g" "$tempmd"
    sed -i "s|\[COMPANY_EIN\]|${DATA[COMPANY_EIN]}|g" "$tempmd"
    sed -i "s|\[COMPANY_ADDRESS\]|${DATA[PRINCIPAL_FULL]}|g" "$tempmd"
    sed -i "s|\[REGISTERED_AGENT\]|${DATA[REG_AGENT_NAME]}|g" "$tempmd"
    sed -i "s|\[FORMATION_DATE\]|${DATA[COMPANY_FORMATION_DATE]}|g" "$tempmd"
    
    # Generic series code placeholder - use example client
    sed -i "s|C-\[###\]|${DATA[EXAMPLE_CLIENT_CODE]:-C-001}|g" "$tempmd"
    sed -i "s|C-\[___\]|${DATA[EXAMPLE_CLIENT_CODE]:-C-001}|g" "$tempmd"
    sed -i "s|C-\[____\]|${DATA[EXAMPLE_CLIENT_CODE]:-C-001}|g" "$tempmd"
    sed -i "s|Series C-###|Series ${DATA[EXAMPLE_CLIENT_CODE]:-C-001}|g" "$tempmd"
    
    # Client placeholders
    sed -i "s|\[CLIENT BRAND NAME\]|${DATA[EXAMPLE_CLIENT_DBA]:-Example Brand}|g" "$tempmd"
    sed -i "s|\[CLIENT BRAND\]|${DATA[EXAMPLE_CLIENT_DBA]:-Example Brand}|g" "$tempmd"
    sed -i "s|\[CLIENT SERIES NAME\]|${DATA[EXAMPLE_CLIENT_NAME]:-Example Client LLC}|g" "$tempmd"
    sed -i "s|\[Client Name\]|${DATA[EXAMPLE_CLIENT_NAME]:-Example Client LLC}|g" "$tempmd"
    sed -i "s|\[CLIENT_NAME\]|${DATA[EXAMPLE_CLIENT_NAME]:-Example Client LLC}|g" "$tempmd"
    
    # Client contact placeholders
    sed -i "s|\[CLIENT BRAND EMAIL\]|${DATA[EXAMPLE_CLIENT_SUPPORT_EMAIL]:-support@example.com}|g" "$tempmd"
    sed -i "s|\[CLIENT BRAND SUPPORT EMAIL\]|${DATA[EXAMPLE_CLIENT_SUPPORT_EMAIL]:-support@example.com}|g" "$tempmd"
    sed -i "s|\[CLIENT BRAND CONTACT EMAIL\]|${DATA[EXAMPLE_CLIENT_SUPPORT_EMAIL]:-support@example.com}|g" "$tempmd"
    sed -i "s|\[CLIENT BRAND PHONE\]|${DATA[EXAMPLE_CLIENT_PHONE]:-1-800-555-0100}|g" "$tempmd"
    sed -i "s|\[CLIENT BRAND ADDRESS\]|${DATA[EXAMPLE_CLIENT_ADDRESS]:-123 Main St, City, ST 00000}|g" "$tempmd"
    sed -i "s|\[CLIENT BRAND CONTACT\]|${DATA[EXAMPLE_CLIENT_SUPPORT_EMAIL]:-support@example.com}|g" "$tempmd"
    
    # Fee placeholders (tables)
    sed -i "s|\$\[____\]|\$${DATA[FEE_DOMESTIC_FLAT]:-2.99}|g" "$tempmd"
    sed -i "s|\[____\]%|${DATA[FEE_DOMESTIC_PERCENT]:-0.5}%|g" "$tempmd"
    sed -i "s|\[___\]%|${DATA[FRAUD_ALLOC_CLIENT]:-80}%|g" "$tempmd"
    
    # Settlement placeholders
    sed -i "s|\[Weekly/Daily\]|Daily|g" "$tempmd"
    sed -i "s|\[Yes/No\]|Yes|g" "$tempmd"
    
    # Fill empty table cells with dash
    sed -i 's/| \[____\] |/| — |/g' "$tempmd"
    sed -i 's/|\[____\]|/|—|/g' "$tempmd"
    
    # Form field blanks - convert to styled underline
    sed -i 's/\[____\]/_____________/g' "$tempmd"
    sed -i 's/\[___\]/__________/g' "$tempmd"
    sed -i 's/\[________________\]/_______________________________/g' "$tempmd"
    
    # Convert to HTML (no --number-sections since docs have explicit numbering)
    pandoc "$tempmd" -f markdown -t html5 --standalone --toc --toc-depth=3 \
        --metadata title="$title" \
        --css="${prefix}style.css" \
        -o "$temphtml"
    
    # Inject navigation
    local nav_html=$(generate_nav "$prefix")
    
    {
        sed -n '1,/<body>/p' "$temphtml"
        echo "$nav_html"
        echo '<div class="main-content">'
        sed -n '/<body>/,/<\/body>/p' "$temphtml" | sed '1d;$d'
        echo '</div>'
        echo '</body>'
        echo '</html>'
    } > "$outfile"
    
    echo "  ✓ $code - ${title}"
}

echo ""
echo "Converting documents..."

for code in "${DOC_CODES[@]}"; do
    process_document "$code"
done

# ============================================================================
# STEP 6: Generate index.html dynamically
# ============================================================================

echo ""
echo "Generating index..."

generate_index() {
    cat << 'HEADER'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CCASH Legal Documents</title>
  <link rel="stylesheet" href="style.css">
  <style>
    .main-content { max-width: 1000px; }
    .subtitle { color: #4a5568; margin-bottom: 2rem; }
    h2 { font-size: 1.15rem; }
    table { font-size: 0.9rem; margin: 0.75rem 0 1.5rem; }
    th { padding: 0.5rem 0.6rem; }
    td { padding: 0.4rem 0.6rem; }
    footer { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #e2e8f0; color: #a0aec0; font-size: 0.8rem; }
  </style>
</head>
<body>
HEADER

    generate_nav ""
    
    cat << 'CONTENT_START'
  <div class="main-content">
    <header id="title-block-header">
      <h1 class="title">CCASH Money Services (US) Series LLC</h1>
    </header>
CONTENT_START

    echo "    <p class=\"subtitle\">Legal Document Registry — ${#DOC_CODES[@]} Documents</p>"
    
    # Generate tables by category
    local categories=("formation:Formation Documents" "governance:Governance Documents" "compliance:Compliance Documents" "client:Client Agreements" "schedule:Schedules & Exhibits" "internal:Internal Documents" "overview:Overview")
    
    local section_num=1
    for cat_entry in "${categories[@]}"; do
        local cat_key="${cat_entry%%:*}"
        local cat_name="${cat_entry#*:}"
        
        # Check if any docs in this category
        local has_docs=false
        for code in "${DOC_CODES[@]}"; do
            [[ "${DOC_CATEGORIES[$code]}" == "$cat_key" ]] && has_docs=true && break
        done
        [[ "$has_docs" == "false" ]] && continue
        
        echo ""
        echo "    <h2>${section_num}. ${cat_name}</h2>"
        echo "    <table>"
        echo "      <thead><tr><th>Code</th><th>Document</th><th>Cat</th><th>Ver</th><th>Updated</th><th>Hash</th></tr></thead>"
        echo "      <tbody>"
        
        for code in "${DOC_CODES[@]}"; do
            [[ "${DOC_CATEGORIES[$code]}" == "$cat_key" ]] || continue
            
            local path="${DOC_PATHS[$code]}"
            local title="${DOC_TITLES[$code]}"
            local version="${DOC_VERSIONS[$code]}"
            local date="${DOC_DATES[$code]}"
            local hash="${DOC_HASHES[$code]}"
            local cat_class="cat-${cat_key}"
            local cat_short="${cat_key:0:4}"
            [[ "$cat_short" == "form" ]] && cat_short="Form"
            [[ "$cat_short" == "gove" ]] && cat_short="Gov"
            [[ "$cat_short" == "comp" ]] && cat_short="Comp"
            [[ "$cat_short" == "clie" ]] && cat_short="Client"
            [[ "$cat_short" == "sche" ]] && cat_short="Sched"
            [[ "$cat_short" == "inte" ]] && cat_short="Int"
            [[ "$cat_short" == "over" ]] && cat_short="Over"
            
            local display_code="${code%%_*}"
            [[ "$code" == 00_* ]] && display_code="00"
            
            echo "        <tr><td><span class=\"doc-code\">$display_code</span></td><td><a class=\"doc-link\" href=\"${path}.html\">$title</a></td><td><span class=\"category $cat_class\">$cat_short</span></td><td class=\"version\">$version</td><td class=\"date\">$date</td><td><span class=\"hash\">$hash</span></td></tr>"
        done
        
        echo "      </tbody>"
        echo "    </table>"
        ((section_num++))
    done
    
    cat << FOOTER
    <footer>
      <p>Generated: $(date '+%B %d, %Y') • CCASH Money Services (US) Series LLC</p>
      <p>Source: _schema/registry.dat • Git hashes reference last commit per document.</p>
    </footer>
  </div>
</body>
</html>
FOOTER
}

generate_index > "$OUTPUT_DIR/index.html"

# ============================================================================
# STEP 7: Cleanup
# ============================================================================

rm -rf "$TEMP_DIR"

echo ""
echo "=== Complete ==="
echo "Output: $OUTPUT_DIR"
echo "Documents: ${#DOC_CODES[@]}"
echo "Index: $OUTPUT_DIR/index.html"
