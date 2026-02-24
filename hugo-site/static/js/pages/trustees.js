// Scripts for trustees page

const nav = document.querySelector('nav');
window.addEventListener('scroll', () => {
    if (window.pageYOffset > 60) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});

// Trustee Revenue Calculator
function formatCurrency(amount) {
    return '$' + amount.toLocaleString('en-US', { maximumFractionDigits: 0 });
}

function parseAmount(str) {
    return parseFloat(str.replace(/[^0-9.-]/g, '')) || 0;
}

function updateSliderBackground() {
    const slider = document.getElementById('issuanceSlider');
    const min = parseFloat(slider.min);
    const max = parseFloat(slider.max);
    const val = parseFloat(slider.value);
    const pct = ((val - min) / (max - min)) * 100;
    slider.style.setProperty('--slider-pct', pct + '%');
}

function calculateTrusteeRevenue() {
    const issuanceValue = parseAmount(document.getElementById('issuanceValue').value);

    // 1% annual trust & admin fee, trustee gets 2/3
    const totalFee = issuanceValue * 0.01;
    const trusteeFee = totalFee * 2 / 3;

    // Also calculate deposit oversight value (3% of issuance)
    const depositValue = issuanceValue * 0.03;

    document.getElementById('trusteeResult').innerHTML = `
        <div class="label">Your Annual Trustee Revenue</div>
        <div class="amount">${formatCurrency(trusteeFee)}</div>
        <div class="breakdown">
            <span>Issuance value: ${formatCurrency(issuanceValue)}</span>
            <span>Annual fee (1%): ${formatCurrency(totalFee)}</span>
            <span>Your ⅔ share: <strong>${formatCurrency(trusteeFee)}</strong>/yr</span>
            <span style="margin-top:8px; padding-top:8px; border-top: 1px solid rgba(255,255,255,0.15);">Security deposits under oversight: ${formatCurrency(depositValue)}</span>
        </div>
    `;
}

// Slider controls the input
document.getElementById('issuanceSlider').addEventListener('input', function() {
    const val = parseFloat(this.value);
    document.getElementById('issuanceValue').value = val.toLocaleString('en-US');
    updateSliderBackground();
    calculateTrusteeRevenue();
});

// Initial calculation and slider position
updateSliderBackground();
calculateTrusteeRevenue();
