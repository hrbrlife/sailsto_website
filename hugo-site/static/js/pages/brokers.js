// Scripts for brokers.html

        // Broker Earnings Calculator
        function formatCurrency(amount) {
            return '$' + amount.toLocaleString('en-US', { maximumFractionDigits: 0 });
        }

        function parseAmount(str) {
            return parseFloat(str.replace(/[^0-9.-]/g, '')) || 0;
        }

        function calculateBrokerEarnings() {
            const placement = parseAmount(document.getElementById('placementAmount').value);
            const issuerReward = parseFloat(document.getElementById('issuerReward').value) || 0;
            const sailsShare = parseFloat(document.getElementById('sailsShare').value) || 0;
            const turnover = parseFloat(document.getElementById('annualTurnover').value) || 0;
            const participation = parseFloat(document.getElementById('brokerParticipation').value) || 0;
            const commShare = parseFloat(document.getElementById('commissionShare').value) || 0;

            // Primary placement earnings
            const fromIssuer = placement * (issuerReward / 100);
            const fromSails = placement * (sailsShare / 100);
            const totalPrimary = fromIssuer + fromSails;

            // Secondary trading earnings (annual)
            const annualVolume = placement * (turnover / 100);
            const yourDeals = annualVolume * (participation / 100);
            const brokerCommission = yourDeals * 0.005 * (2/3); // 0.5% total, ⅓ platform + ⅓ buy-side + ⅓ sell-side (brokers get ⅔)
            const yourSecondary = brokerCommission * (commShare / 100);

            // Multi-year projection
            const year1 = totalPrimary + yourSecondary;
            const year2 = yourSecondary;
            const year3 = yourSecondary;
            const threeYearTotal = year1 + year2 + year3;

            const resultsDiv = document.getElementById('brokerResults');
            resultsDiv.innerHTML = `
                <div class="result-section">
                    <h4>Primary Placement (One-Time)</h4>
                    <div class="result-row sub">
                        <span class="label">From Issuer (${issuerReward}%)</span>
                        <span class="value">${formatCurrency(fromIssuer)}</span>
                    </div>
                    <div class="result-row sub">
                        <span class="label">From Sails.to (${sailsShare}%)</span>
                        <span class="value">${formatCurrency(fromSails)}</span>
                    </div>
                    <div class="result-row">
                        <span class="label"><strong>Total Primary</strong></span>
                        <span class="value"><strong>${formatCurrency(totalPrimary)}</strong></span>
                    </div>
                </div>
                
                <div class="result-section">
                    <h4>Secondary Trading (Annual)</h4>
                    <div class="result-row sub">
                        <span class="label">Market turnover (${turnover}%)</span>
                        <span class="value">${formatCurrency(annualVolume)}</span>
                    </div>
                    <div class="result-row sub">
                        <span class="label">Your deals (${participation}%)</span>
                        <span class="value">${formatCurrency(yourDeals)}</span>
                    </div>
                    <div class="result-row sub">
                        <span class="label">Broker pool (0.33%)</span>
                        <span class="value">${formatCurrency(brokerCommission)}</span>
                    </div>
                    <div class="result-row">
                        <span class="label"><strong>Your share (${commShare}%)</strong></span>
                        <span class="value"><strong>${formatCurrency(yourSecondary)}/yr</strong></span>
                    </div>
                </div>
                
                <div class="result-section">
                    <h4>3-Year Projection</h4>
                    <div class="result-row sub">
                        <span class="label">Year 1 (placement + secondary)</span>
                        <span class="value">${formatCurrency(year1)}</span>
                    </div>
                    <div class="result-row sub">
                        <span class="label">Year 2 (secondary only)</span>
                        <span class="value">${formatCurrency(year2)}</span>
                    </div>
                    <div class="result-row sub">
                        <span class="label">Year 3 (secondary only)</span>
                        <span class="value">${formatCurrency(year3)}</span>
                    </div>
                </div>
                
                <div class="result-total">
                    <span class="label">3-Year Total Earnings</span>
                    <span class="value">${formatCurrency(threeYearTotal)}</span>
                </div>
            `;
        }

        // Format placement amount input
        document.getElementById('placementAmount').addEventListener('blur', function() {
            const val = parseAmount(this.value);
            this.value = val.toLocaleString('en-US');
            calculateBrokerEarnings();
        });

        // Recalculate on any input change
        document.querySelectorAll('#placementAmount, #issuerReward, #sailsShare, #annualTurnover, #brokerParticipation, #commissionShare').forEach(input => {
            input.addEventListener('input', calculateBrokerEarnings);
        });

        // Initial calculation
        calculateBrokerEarnings();