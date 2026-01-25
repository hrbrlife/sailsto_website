---
title: "Pricing"
description: "Transparent pricing calculator. Understand your costs based on investor sourcing and offering size."
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/pricing.css"
scripts:
  - "/js/pricing.js"
---


<section class="page-hero">
    <span class="section-label">Pricing</span>
    <h1 class="section-title">Cost Calculator</h1>
    <p class="section-desc">Model your offering costs based on size, caps, and investor sourcing. All amounts in multiples of $150,000.</p>
</section>
<div class="pricing-container">
    <div class="calculator-section">
        <h2>Calculate Your Costs</h2>
        <p class="intro">Adjust the parameters below to see exactly what you'll receive and pay over the life of your offering</p>
        <div class="calc-grid">
            <div class="calc-inputs">
                <div class="input-group">
                    <label for="softCap">Soft Cap (Minimum Goal)</label>
                    <div class="amount-input-wrapper">
                        <input type="text" id="softCap" value="600,000" inputmode="numeric">
                        <div class="increment-buttons">
                            <button type="button" class="increment-btn" data-target="softCap" data-dir="up">▲</button>
                            <button type="button" class="increment-btn" data-target="softCap" data-dir="down">▼</button>
                        </div>
                    </div>
                    <span class="amount-written" id="softCapWritten">Six Hundred Thousand Dollars</span>
                    <span class="input-hint">Minimum funding required to proceed</span>
                </div>
                <div class="input-group">
                    <label for="hardCap">Hard Cap (Maximum Goal)</label>
                    <div class="amount-input-wrapper">
                        <input type="text" id="hardCap" value="1,500,000" inputmode="numeric">
                        <div class="increment-buttons">
                            <button type="button" class="increment-btn" data-target="hardCap" data-dir="up">▲</button>
                            <button type="button" class="increment-btn" data-target="hardCap" data-dir="down">▼</button>
                        </div>
                    </div>
                    <span class="amount-written" id="hardCapWritten">One Million Five Hundred Thousand Dollars</span>
                    <span class="input-hint">Maximum you can raise</span>
                </div>
                <div class="slider-group">
                    <label>Actual Amount Raised</label>
                    <div class="slider-container">
                        <div class="slider-value" id="sliderValue">$900,000</div>
                        <div class="slider-track">
                            <div class="slider-softcap-marker" id="softCapMarker">
                                <span class="slider-softcap-label">Soft Cap</span>
                            </div>
                        </div>
                        <input type="range" id="actualRaise" class="slider" min="0" max="100" value="60">
                    </div>
                    <div class="slider-labels">
                        <span id="minLabel">$0</span>
                        <span id="maxLabel">$1,500,000</span>
                    </div>
                    <span class="input-hint">Drag to simulate different outcomes (from $0 to hard cap)</span>
                </div>
                <div class="sourcing-section">
                    <h3 style="font-family: var(--font-ui); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--ink); margin-bottom: 20px; padding-top: 20px; border-top: 1px solid rgba(0,0,0,0.1);">Investor Sourcing</h3>
                    <div class="sourcing-visual" id="sourcingVisual">
                        <div class="sourcing-bar">
                            <div class="sourcing-segment own-segment" id="ownSegment"></div>
                            <div class="sourcing-segment broker-segment" id="brokerSegment"></div>
                            <div class="sourcing-segment general-segment" id="generalSegment"></div>
                        </div>
                        <div class="sourcing-legend">
                            <span class="legend-item"><span class="legend-color own"></span>Your Network (1%)</span>
                            <span class="legend-item"><span class="legend-color broker"></span>Broker Placed (6%)</span>
                            <span class="legend-item"><span class="legend-color general"></span>General (6%)</span>
                        </div>
                    </div>
                    <div class="slider-group">
                        <label>Your Own Network Placement</label>
                        <div class="sourcing-slider-row">
                            <input type="range" id="ownPlacement" class="slider sourcing-slider" min="0" max="100" value="30">
                            <span class="slider-percent" id="ownPercent">30%</span>
                        </div>
                        <div class="sourcing-amounts">
                            <span id="ownAmount">$270,000</span>
                            <span class="input-hint">Investors you bring directly → 1% distribution fee</span>
                        </div>
                    </div>
                    <div class="slider-group">
                        <label>Broker Assisted (of remaining <span id="remainingPercent">70%</span>)</label>
                        <div class="sourcing-slider-row">
                            <input type="range" id="brokerPlacement" class="slider sourcing-slider" min="0" max="100" value="50">
                            <span class="slider-percent" id="brokerPercent">50%</span>
                        </div>
                        <div class="sourcing-amounts">
                            <span id="brokerAmount">$315,000</span>
                            <span class="input-hint">Broker helps place → 6% distribution fee</span>
                        </div>
                    </div>
                    <div class="sourcing-summary" id="sourcingSummary">
                        <div class="summary-row">
                            <span>General Distribution (unassisted)</span>
                            <span id="generalAmount">$315,000</span>
                        </div>
                    </div>
                </div>
                <div class="checkbox-group">
                    <input type="checkbox" id="earlyBirdDiscount">
                    <label for="earlyBirdDiscount">Enable Early Bird Discount (during soft cap phase)</label>
                </div>
                <div class="input-group" id="discountGroup" style="display: none;">
                    <label for="discountRate">Early Bird Discount (%)</label>
                    <input type="number" id="discountRate" value="10" min="0" max="50" step="1">
                    <span class="input-hint">Discount for investors during soft cap phase</span>
                </div>
                <div class="checkbox-group">
                    <input type="checkbox" id="brokerReward">
                    <label for="brokerReward">Enable Broker Placement Reward (soft cap phase)</label>
                </div>
                <div class="input-group" id="brokerRewardGroup" style="display: none;">
                    <label for="brokerRewardRate">Broker Reward (%)</label>
                    <input type="number" id="brokerRewardRate" value="2" min="0" max="10" step="0.5">
                    <span class="input-hint">Additional incentive for brokers on their placed amount</span>
                </div>
                <div class="input-group">
                    <label for="couponRate">Annual Coupon Rate (%)</label>
                    <input type="number" id="couponRate" value="8" min="0" max="30" step="0.1">
                    <span class="input-hint">Annual interest rate paid to investors</span>
                </div>
                <div class="input-group">
                    <label for="termYears">Term (Years)</label>
                    <input type="number" id="termYears" value="3" min="1" max="30" step="1">
                    <span class="input-hint">Bond maturity period</span>
                </div>
                <div class="input-group">
                    <label for="paymentFreq">Payment Frequency</label>
                    <select id="paymentFreq">
                        <option value="1">Annual</option>
                        <option value="2" selected>Semi-Annual</option>
                        <option value="4">Quarterly</option>
                        <option value="12">Monthly</option>
                    </select>
                    <span class="input-hint">How often coupon payments are made</span>
                </div>
            </div>
            <div class="calc-results" id="results">
            </div>
        </div>
    </div>
    <div class="fee-section">
        <h2>Complete Fee Structure</h2>
        <p class="intro">All fees depend on how investors are sourced</p>
        <table class="fee-table">
            <thead>
                <tr>
                    <th>Fee Type</th>
                    <th>Amount</th>
                    <th>When Charged</th>
                    <th>Who Pays</th>
                    <th>Split</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Brokerage Fee</strong></td>
                    <td><span class="fee-highlight">0.5%</span></td>
                    <td>Secondary trades + post-soft-cap primary<br><em style="color:#38a169; font-size:0.85em;">⚡ Waived during soft cap phase</em></td>
                    <td>Buyer</td>
                    <td>⅓ Platform + ⅓ Buy-side + ⅓ Sell-side</td>
                </tr>
                <tr>
                    <td><strong>Distribution Fee</strong></td>
                    <td><span class="fee-highlight">6% OR 1%</span></td>
                    <td>Deducted from soft cap when reached<br><em style="color:#38a169; font-size:0.85em;">⚡ Not charged until soft cap reached</em></td>
                    <td>Issuer (from proceeds)</td>
                    <td>See below</td>
                </tr>
                <tr>
                    <td style="padding-left: 30px;">→ General Distribution</td>
                    <td><span class="fee-highlight">6%</span></td>
                    <td>Investors not from issuer's network</td>
                    <td>Issuer</td>
                    <td>Brokers + Sails.to</td>
                </tr>
                <tr>
                    <td style="padding-left: 30px;">→ Referral Investors</td>
                    <td><span class="fee-highlight">1%</span></td>
                    <td>Investors using issuer's referral code</td>
                    <td>Issuer</td>
                    <td>Sails.to</td>
                </tr>
                <tr>
                    <td><strong>Trust & Administration</strong></td>
                    <td><span class="fee-highlight">1% annual</span></td>
                    <td>Ongoing (annually on nominal value)</td>
                    <td>Issuer</td>
                    <td>Trust + Sails.to</td>
                </tr>
                <tr>
                    <td><strong>Security Deposit</strong></td>
                    <td><span class="fee-highlight">3% of issuance</span></td>
                    <td>At issuance, reserved under trust</td>
                    <td>Issuer (from proceeds)</td>
                    <td>Reserved, returned at end</td>
                </tr>
                <tr>
                    <td><strong>Clearstream Fees</strong></td>
                    <td>Variable</td>
                    <td>Channel 3 transactions</td>
                    <td>Investor</td>
                    <td>Clearstream</td>
                </tr>
                <tr>
                    <td><strong>Conversion Fee</strong></td>
                    <td><span class="fee-highlight">0.10-0.25%</span></td>
                    <td>When wrapping/unwrapping Solana ↔ Clearstream</td>
                    <td>Requester</td>
                    <td>Sails.to + Trust</td>
                </tr>
            </tbody>
        </table>
        <div class="note-box">
            <strong>📌 Key Points</strong>
            <ul>
                <li><strong>Soft cap phase is fee-free:</strong> Brokerage (0.5%) waived, distribution fees deferred until soft cap reached</li>
                <li><strong>If soft cap fails:</strong> Full refund to investors (only Clearstream fees at cost, if used)</li>
                <li><strong>No upfront costs:</strong> All fees deducted from proceeds when offering succeeds</li>
                <li><strong>Security deposit:</strong> Returned at end of bond term if no issues</li>
            </ul>
        </div>
    </div>
</div>
