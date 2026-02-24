// Scripts for pricing.html

// Constants
        const INCREMENT = 150000;

        // DOM Elements
        const softCapInput = document.getElementById('softCap');
        const hardCapInput = document.getElementById('hardCap');
        const actualRaiseSlider = document.getElementById('actualRaise');
        const ownPlacementSlider = document.getElementById('ownPlacement');
        const brokerPlacementSlider = document.getElementById('brokerPlacement');
        const earlyBirdCheckbox = document.getElementById('earlyBirdDiscount');
        const discountGroup = document.getElementById('discountGroup');
        const discountRateInput = document.getElementById('discountRate');
        const brokerRewardCheckbox = document.getElementById('brokerReward');
        const brokerRewardGroup = document.getElementById('brokerRewardGroup');
        const brokerRewardRateInput = document.getElementById('brokerRewardRate');
        const couponRateInput = document.getElementById('couponRate');
        const termYearsInput = document.getElementById('termYears');
        const paymentFreqSelect = document.getElementById('paymentFreq');
        const resultsDiv = document.getElementById('results');
        const sliderValueDiv = document.getElementById('sliderValue');
        const minLabel = document.getElementById('minLabel');
        const maxLabel = document.getElementById('maxLabel');
        const softCapMarker = document.getElementById('softCapMarker');
        const softCapWritten = document.getElementById('softCapWritten');
        const hardCapWritten = document.getElementById('hardCapWritten');
        
        // Sourcing visual elements
        const ownSegment = document.getElementById('ownSegment');
        const brokerSegment = document.getElementById('brokerSegment');
        const generalSegment = document.getElementById('generalSegment');
        const ownPercent = document.getElementById('ownPercent');
        const brokerPercent = document.getElementById('brokerPercent');
        const ownAmount = document.getElementById('ownAmount');
        const brokerAmount = document.getElementById('brokerAmount');
        const generalAmount = document.getElementById('generalAmount');
        const remainingPercent = document.getElementById('remainingPercent');

        // Number to words conversion
        function numberToWords(num) {
            if (num === 0) return 'Zero Dollars';
            
            const ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
                'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen'];
            const tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety'];
            
            function convertGroup(n) {
                if (n === 0) return '';
                if (n < 20) return ones[n];
                if (n < 100) return tens[Math.floor(n / 10)] + (n % 10 ? ' ' + ones[n % 10] : '');
                return ones[Math.floor(n / 100)] + ' Hundred' + (n % 100 ? ' ' + convertGroup(n % 100) : '');
            }
            
            let result = '';
            
            if (num >= 1000000000) {
                result += convertGroup(Math.floor(num / 1000000000)) + ' Billion ';
                num %= 1000000000;
            }
            if (num >= 1000000) {
                result += convertGroup(Math.floor(num / 1000000)) + ' Million ';
                num %= 1000000;
            }
            if (num >= 1000) {
                result += convertGroup(Math.floor(num / 1000)) + ' Thousand ';
                num %= 1000;
            }
            if (num > 0) {
                result += convertGroup(num);
            }
            
            return result.trim() + ' Dollars';
        }

        // Format number with commas
        function formatWithCommas(num) {
            return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        }

        // Parse number from formatted string
        function parseFormattedNumber(str) {
            return parseInt(str.replace(/,/g, ''), 10) || 0;
        }

        // Round to nearest increment
        function roundToIncrement(value) {
            return Math.round(value / INCREMENT) * INCREMENT;
        }

        // Format currency
        function formatCurrency(amount) {
            return '$' + formatWithCommas(Math.round(amount));
        }

        // Format percent
        function formatPercent(percent) {
            return percent.toFixed(2) + '%';
        }

        // Update amount input display and written form
        function updateAmountInput(input, writtenElem) {
            let value = parseFormattedNumber(input.value);
            value = roundToIncrement(value);
            if (value < 0) value = 0;
            input.value = formatWithCommas(value);
            writtenElem.textContent = numberToWords(value);
        }

        // Handle increment buttons
        document.querySelectorAll('.increment-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const targetId = this.dataset.target;
                const direction = this.dataset.dir;
                const input = document.getElementById(targetId);
                let value = parseFormattedNumber(input.value);
                
                if (direction === 'up') {
                    value += INCREMENT;
                } else {
                    value = Math.max(0, value - INCREMENT);
                }
                
                input.value = formatWithCommas(value);
                const writtenElem = document.getElementById(targetId + 'Written');
                writtenElem.textContent = numberToWords(value);
                
                // Enforce hard cap >= soft cap
                enforceCapConstraints();
                
                updateSliderPosition();
                calculateCosts();
            });
        });

        // Ensure hard cap >= soft cap
        function enforceCapConstraints() {
            const softCap = parseFormattedNumber(softCapInput.value);
            const hardCap = parseFormattedNumber(hardCapInput.value);
            
            if (hardCap < softCap) {
                hardCapInput.value = formatWithCommas(softCap);
                hardCapWritten.textContent = numberToWords(softCap);
            }
        }

        // Handle manual input
        softCapInput.addEventListener('blur', function() {
            updateAmountInput(this, softCapWritten);
            enforceCapConstraints();
            updateSliderPosition();
            calculateCosts();
        });
        
        softCapInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') this.blur();
        });

        hardCapInput.addEventListener('blur', function() {
            updateAmountInput(this, hardCapWritten);
            enforceCapConstraints();
            updateSliderPosition();
            calculateCosts();
        });
        
        hardCapInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') this.blur();
        });

        function updateSliderPosition() {
            const softCap = parseFormattedNumber(softCapInput.value);
            const hardCap = parseFormattedNumber(hardCapInput.value);
            const percent = parseFloat(actualRaiseSlider.value) || 0;
            
            // Slider goes from 0 to hardCap
            const actualAmount = Math.round((hardCap * percent) / 100);
            const roundedAmount = roundToIncrement(actualAmount);
            
            sliderValueDiv.textContent = formatCurrency(roundedAmount);
            sliderValueDiv.style.left = percent + '%';
            
            minLabel.textContent = '$0';
            maxLabel.textContent = formatCurrency(hardCap);
            
            // Position soft cap marker
            if (hardCap > 0) {
                const softCapPercent = (softCap / hardCap) * 100;
                softCapMarker.style.left = softCapPercent + '%';
                softCapMarker.style.display = 'block';
            } else {
                softCapMarker.style.display = 'none';
            }
            
            // Update sourcing visual
            updateSourcingVisual(roundedAmount);
        }
        
        function updateSourcingVisual(actualAmount) {
            const ownPct = parseFloat(ownPlacementSlider.value) || 0;
            const brokerPct = parseFloat(brokerPlacementSlider.value) || 0;
            
            // Calculate amounts
            const ownAmt = actualAmount * (ownPct / 100);
            const remainingAmt = actualAmount - ownAmt;
            const brokerAmt = remainingAmt * (brokerPct / 100);
            const generalAmt = remainingAmt - brokerAmt;
            
            // Update visual bar
            ownSegment.style.width = ownPct + '%';
            const brokerWidth = (100 - ownPct) * (brokerPct / 100);
            brokerSegment.style.width = brokerWidth + '%';
            generalSegment.style.width = (100 - ownPct - brokerWidth) + '%';
            
            // Update labels
            ownPercent.textContent = ownPct + '%';
            brokerPercent.textContent = brokerPct + '%';
            remainingPercent.textContent = (100 - ownPct) + '%';
            
            // Update amounts
            ownAmount.textContent = formatCurrency(ownAmt);
            brokerAmount.textContent = formatCurrency(brokerAmt);
            generalAmount.textContent = formatCurrency(generalAmt);
        }

        function calculateCosts() {
            const softCap = parseFormattedNumber(softCapInput.value);
            const hardCap = parseFormattedNumber(hardCapInput.value);
            const percent = parseFloat(actualRaiseSlider.value) || 0;
            const actualAmount = roundToIncrement(Math.round((hardCap * percent) / 100));
            
            // Sourcing percentages
            const ownPct = parseFloat(ownPlacementSlider.value) || 0;
            const brokerPct = parseFloat(brokerPlacementSlider.value) || 0;
            
            const hasDiscount = earlyBirdCheckbox.checked;
            const discountRate = parseFloat(discountRateInput.value) || 0;
            const hasBrokerReward = brokerRewardCheckbox.checked;
            const brokerRewardRate = parseFloat(brokerRewardRateInput.value) || 0;
            const couponRate = parseFloat(couponRateInput.value) || 0;
            const termYears = parseFloat(termYearsInput.value) || 3;
            const paymentFreq = parseFloat(paymentFreqSelect.value) || 2;

            let html = '';

            // SCENARIO: Didn't reach soft cap
            if (actualAmount < softCap) {
                const brokerageFee = actualAmount * 0.005;
                
                html = `
                    <div class="status-box failed">
                        <strong>✗ Soft Cap Not Reached</strong>
                        <p>Offering fails. Principal returned to investors minus non-refundable fees.</p>
                    </div>
                    
                    <div class="result-row">
                        <span class="result-label">Amount Raised</span>
                        <span class="result-value">${formatCurrency(actualAmount)}</span>
                    </div>
                    <div class="result-row">
                        <span class="result-label" style="font-style: italic;">Written</span>
                        <span class="result-value" style="font-style: italic; font-size: 0.85rem;">${numberToWords(actualAmount)}</span>
                    </div>
                    <div class="result-row">
                        <span class="result-label">Soft Cap Required</span>
                        <span class="result-value">${formatCurrency(softCap)}</span>
                    </div>
                    <div class="result-row">
                        <span class="result-label">Shortfall</span>
                        <span class="result-value" style="color: var(--crimson);">${formatCurrency(softCap - actualAmount)}</span>
                    </div>
                    
                    <div class="breakdown-section">
                        <h4>Non-Refundable Fees (Investor Pays)</h4>
                        <div class="result-row">
                            <span class="result-label">Brokerage Fee (0.5%)</span>
                            <span class="result-value">${formatCurrency(brokerageFee)}</span>
                        </div>
                        <div class="result-row">
                            <span class="result-label">Clearstream Fees</span>
                            <span class="result-value">Variable (if Channel 3 used)</span>
                        </div>
                    </div>
                    
                    <div class="breakdown-section">
                        <h4>Issuer Cost</h4>
                        <div class="result-row">
                            <span class="result-label">Distribution Fee</span>
                            <span class="result-value" style="color: var(--gold);">$0 (not charged)</span>
                        </div>
                    </div>
                `;
            } else {
                // SCENARIO: Soft cap reached - success!
                
                // Calculate investor sourcing amounts
                const ownAmount = actualAmount * (ownPct / 100);
                const remainingAmount = actualAmount - ownAmount;
                const brokerPlacedAmount = remainingAmount * (brokerPct / 100);
                const generalDistAmount = remainingAmount - brokerPlacedAmount;

                // Brokerage fee (0.5% on all) - split ⅓ platform, ⅓ buy-side broker, ⅓ sell-side broker
                const brokerageFee = actualAmount * 0.005;
                const brokerageToBrokers = brokerageFee * (2/3); // both broker sides combined
                const brokerageToSails = brokerageFee * (1/3);   // platform share

                // Distribution fees breakdown
                // Own network (1%): all to Sails.to
                const ownDistFee = ownAmount * 0.01;
                const ownDistToSails = ownDistFee;
                
                // Broker placed (6%): ~3% to broker, ~3% to Sails
                const brokerDistFee = brokerPlacedAmount * 0.06;
                const brokerDistToBroker = brokerDistFee * 0.5;  // 3% to broker
                const brokerDistToSails = brokerDistFee * 0.5;   // 3% to Sails
                
                // General distribution (6%): ~3% to broker network, ~3% to Sails
                const generalDistFee = generalDistAmount * 0.06;
                const generalDistToBroker = generalDistFee * 0.5;
                const generalDistToSails = generalDistFee * 0.5;
                
                const totalDistFee = ownDistFee + brokerDistFee + generalDistFee;

                // Security deposit (3% of issuance)
                const securityDeposit = actualAmount * 0.03;

                // Early bird discount (applied on soft cap amount)
                // This is a discount given to early investors - issuer pays now, investor gets full value at maturity
                let discountCost = 0;
                let discountedPrincipalAtMaturity = 0;
                if (hasDiscount) {
                    const discountedAmount = Math.min(actualAmount, softCap);
                    discountCost = discountedAmount * (discountRate / 100);
                    // At maturity, these investors get reimbursed at full face value
                    discountedPrincipalAtMaturity = discountCost; // The extra they receive at maturity
                }

                // Broker placement reward (on broker-placed amount up to soft cap)
                let brokerRewardCost = 0;
                if (hasBrokerReward) {
                    const softCapBrokerPortion = Math.min(brokerPlacedAmount, softCap * (brokerPct / 100) * ((100 - ownPct) / 100));
                    brokerRewardCost = softCapBrokerPortion * (brokerRewardRate / 100);
                }

                // TOTALS BY RECIPIENT
                const totalToSails = brokerageToSails + ownDistToSails + brokerDistToSails + generalDistToSails;
                const totalToBrokers = brokerageToBrokers + brokerDistToBroker + generalDistToBroker + brokerRewardCost;

                // Total upfront fees
                const totalUpfrontFees = brokerageFee + totalDistFee + securityDeposit + discountCost + brokerRewardCost;

                // Net proceeds received
                const netProceeds = actualAmount - totalUpfrontFees;

                // Payment calculations
                const totalPeriods = termYears * paymentFreq;
                const periodicRate = (couponRate / 100) / paymentFreq;
                const periodicPayment = actualAmount * periodicRate;
                const totalCouponPayments = periodicPayment * totalPeriods;

                // 1% annual trust & admin fee (paid to trust + platform)
                const annualTrustAdminFee = actualAmount * 0.01;
                const totalTrustAdminFees = annualTrustAdminFee * termYears;
                const trustAdminToTrust = totalTrustAdminFees * 0.5;
                const trustAdminToSails = totalTrustAdminFees * 0.5;

                // Totals
                const capitalReimbursement = actualAmount;
                const depositReimbursed = securityDeposit;
                const totalReceived = netProceeds;
                // Total repaid includes: coupons + trust fees + principal + discount reimbursement - deposit back
                const totalRepaid = totalCouponPayments + totalTrustAdminFees + capitalReimbursement + discountedPrincipalAtMaturity - depositReimbursed;
                const totalCostOfCredit = totalRepaid - totalReceived;
                const effectiveAnnualRate = netProceeds > 0 ? ((totalCostOfCredit / netProceeds) / termYears) * 100 : 0;

                const freqText = {1: 'Annual', 2: 'Semi-Annual', 4: 'Quarterly', 12: 'Monthly'}[paymentFreq];
                const isAboveSoftCap = actualAmount > softCap;
                
                html = `
                    <div class="status-box ${isAboveSoftCap ? 'success' : 'warning'}">
                        <strong>${isAboveSoftCap ? '✓ Exceeding Soft Cap' : '✓ At Soft Cap'}</strong>
                        <p>Offering proceeds. Funds will be released to you after close.</p>
                    </div>
                    
                    <div class="result-row">
                        <span class="result-label">Amount Raised</span>
                        <span class="result-value">${formatCurrency(actualAmount)}</span>
                    </div>
                    <div class="result-row">
                        <span class="result-label" style="font-style: italic;">Written</span>
                        <span class="result-value" style="font-style: italic; font-size: 0.85rem;">${numberToWords(actualAmount)}</span>
                    </div>
                    
                    <div class="breakdown-section">
                        <h4>Upfront Fees: Who Gets Paid</h4>
                        
                        <div style="background: rgba(201,162,39,0.08); padding: 12px; margin-bottom: 12px;">
                            <div class="result-row" style="border: none;">
                                <span class="result-label" style="font-weight: 600; color: var(--ink);">→ Sails.to Platform</span>
                                <span class="result-value">${formatCurrency(totalToSails)}</span>
                            </div>
                            <div style="font-size: 0.8rem; color: var(--slate); padding-left: 16px;">
                                Brokerage share: ${formatCurrency(brokerageToSails)}<br>
                                Distribution (1% own): ${formatCurrency(ownDistToSails)}<br>
                                Distribution share (6%): ${formatCurrency(brokerDistToSails + generalDistToSails)}
                            </div>
                        </div>
                        
                        <div style="background: rgba(13,27,42,0.08); padding: 12px; margin-bottom: 12px;">
                            <div class="result-row" style="border: none;">
                                <span class="result-label" style="font-weight: 600; color: var(--ink);">→ Brokers</span>
                                <span class="result-value">${formatCurrency(totalToBrokers)}</span>
                            </div>
                            <div style="font-size: 0.8rem; color: var(--slate); padding-left: 16px;">
                                Brokerage (⅓ buy + ⅓ sell): ${formatCurrency(brokerageToBrokers)}<br>
                                Distribution share (6%): ${formatCurrency(brokerDistToBroker + generalDistToBroker)}
                                ${hasBrokerReward ? `<br>Placement reward: ${formatCurrency(brokerRewardCost)}` : ''}
                            </div>
                        </div>
                        
                        <div style="background: rgba(0,0,0,0.04); padding: 12px; margin-bottom: 12px;">
                            <div class="result-row" style="border: none;">
                                <span class="result-label" style="font-weight: 600; color: var(--ink);">→ Security Deposit (held in trust)</span>
                                <span class="result-value">${formatCurrency(securityDeposit)}</span>
                            </div>
                            <div style="font-size: 0.8rem; color: var(--slate); padding-left: 16px;">
                                Returned to you at end of term
                            </div>
                        </div>
                        
                        ${hasDiscount ? `
                        <div style="background: rgba(184,25,43,0.08); padding: 12px; margin-bottom: 12px;">
                            <div class="result-row" style="border: none;">
                                <span class="result-label" style="font-weight: 600; color: var(--ink);">→ Early Bird Discount</span>
                                <span class="result-value">${formatCurrency(discountCost)}</span>
                            </div>
                            <div style="font-size: 0.8rem; color: var(--slate); padding-left: 16px;">
                                ${discountRate}% discount on soft cap investors<br>
                                <strong>Note:</strong> These investors paid ${formatCurrency(Math.min(actualAmount, softCap) - discountCost)} but get ${formatCurrency(Math.min(actualAmount, softCap))} at maturity
                            </div>
                        </div>
                        ` : ''}
                        
                        <div class="result-row" style="border-top: 2px solid var(--ink); padding-top: 12px; margin-top: 8px;">
                            <span class="result-label" style="font-weight: 700;">Total Upfront Deductions</span>
                            <span class="result-value" style="font-weight: 700;">-${formatCurrency(totalUpfrontFees)}</span>
                        </div>
                    </div>

                    <div class="highlight-row">
                        <div class="result-row" style="border: none; padding: 0;">
                            <span class="result-label" style="font-weight: 700; color: var(--ink);">💰 Net Proceeds Received</span>
                            <span class="result-value" style="font-size: 1.3rem; color: var(--gold);">${formatCurrency(netProceeds)}</span>
                        </div>
                    </div>

                    <div class="breakdown-section">
                        <h4>Ongoing Payments (${termYears} years)</h4>
                        
                        <div style="background: rgba(0,0,0,0.04); padding: 12px; margin-bottom: 12px;">
                            <div class="result-row" style="border: none;">
                                <span class="result-label" style="font-weight: 600;">→ Investors (Coupon)</span>
                                <span class="result-value">${formatCurrency(totalCouponPayments)}</span>
                            </div>
                            <div style="font-size: 0.8rem; color: var(--slate); padding-left: 16px;">
                                ${freqText} payments of ${formatCurrency(periodicPayment)} × ${totalPeriods} periods
                            </div>
                        </div>
                        
                        <div style="background: rgba(201,162,39,0.08); padding: 12px; margin-bottom: 12px;">
                            <div class="result-row" style="border: none;">
                                <span class="result-label" style="font-weight: 600;">→ Trust & Administration (1% annual)</span>
                                <span class="result-value">${formatCurrency(totalTrustAdminFees)}</span>
                            </div>
                            <div style="font-size: 0.8rem; color: var(--slate); padding-left: 16px;">
                                Trust: ${formatCurrency(trustAdminToTrust)}<br>
                                Sails.to admin: ${formatCurrency(trustAdminToSails)}
                            </div>
                        </div>
                    </div>
                    
                    <div class="breakdown-section">
                        <h4>At Maturity</h4>
                        <div class="result-row">
                            <span class="result-label">→ Investors (Principal)</span>
                            <span class="result-value">${formatCurrency(capitalReimbursement)}</span>
                        </div>
                        ${hasDiscount ? `
                        <div class="result-row">
                            <span class="result-label">→ Early Bird Investors (Discount Reimbursed)</span>
                            <span class="result-value">${formatCurrency(discountedPrincipalAtMaturity)}</span>
                        </div>
                        ` : ''}
                        <div class="result-row">
                            <span class="result-label">← Deposit Returned to You</span>
                            <span class="result-value" style="color: var(--gold);">+${formatCurrency(depositReimbursed)}</span>
                        </div>
                    </div>

                    <div class="summary-box">
                        <h4>Total Cost Analysis</h4>
                        <div class="result-row">
                            <span class="result-label">Net Proceeds Received</span>
                            <span class="result-value">${formatCurrency(totalReceived)}</span>
                        </div>
                        <div class="result-row">
                            <span class="result-label">Total Repaid Over Term</span>
                            <span class="result-value">${formatCurrency(totalRepaid)}</span>
                        </div>
                        <div class="result-row">
                            <span class="result-label" style="font-weight: 600;">Total Cost of Credit</span>
                            <span class="result-value" style="color: var(--crimson);">${formatCurrency(totalCostOfCredit)}</span>
                        </div>
                        <div class="result-row" style="border: none; padding-top: 12px; margin-top: 8px; border-top: 2px solid var(--ink);">
                            <span class="result-label" style="font-size: 1rem; font-weight: 700;">Effective Annual Rate</span>
                            <span class="result-value" style="font-size: 1.5rem; color: var(--gold); font-weight: 700;">${formatPercent(effectiveAnnualRate)}</span>
                        </div>
                    </div>
                `;
            }

            resultsDiv.innerHTML = html;
        }

        // Show/hide discount input
        earlyBirdCheckbox.addEventListener('change', function() {
            discountGroup.style.display = this.checked ? 'flex' : 'none';
            calculateCosts();
        });

        // Show/hide broker reward input
        brokerRewardCheckbox.addEventListener('change', function() {
            brokerRewardGroup.style.display = this.checked ? 'flex' : 'none';
            calculateCosts();
        });

        // Event listeners
        actualRaiseSlider.addEventListener('input', () => {
            updateSliderPosition();
            calculateCosts();
        });
        
        ownPlacementSlider.addEventListener('input', () => {
            const hardCap = parseFormattedNumber(hardCapInput.value);
            const percent = parseFloat(actualRaiseSlider.value) || 0;
            const actualAmount = roundToIncrement(Math.round((hardCap * percent) / 100));
            updateSourcingVisual(actualAmount);
            calculateCosts();
        });
        
        brokerPlacementSlider.addEventListener('input', () => {
            const hardCap = parseFormattedNumber(hardCapInput.value);
            const percent = parseFloat(actualRaiseSlider.value) || 0;
            const actualAmount = roundToIncrement(Math.round((hardCap * percent) / 100));
            updateSourcingVisual(actualAmount);
            calculateCosts();
        });
        
        discountRateInput.addEventListener('input', calculateCosts);
        brokerRewardRateInput.addEventListener('input', calculateCosts);
        couponRateInput.addEventListener('input', calculateCosts);
        termYearsInput.addEventListener('input', calculateCosts);
        paymentFreqSelect.addEventListener('change', calculateCosts);

        // Initial calculation
        updateSliderPosition();
        calculateCosts();

        // Navigation scroll effect
        const nav = document.querySelector('nav');
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });