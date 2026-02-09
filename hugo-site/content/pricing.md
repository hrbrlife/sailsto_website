---
title: "Pricing"
description: "Transparent pricing calculator for Sails CrossSecurities. Understand your costs based on investor sourcing and offering size."
keywords:
  - CrossSecurities pricing
  - tokenization costs
  - capital raising fees
  - success-based pricing
  - no upfront fees
  - CrossSecurities offering
ogImage: "/og-pricing.png"
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/pricing.css"
scripts:
  - "/js/pricing.js"
---


<section class="page-hero">
    <span class="section-label">Pricing</span>
    <h1 class="section-title">Cost Calculator</h1>
    <p class="section-desc">Model your offering costs based on size, caps, and investor sourcing. All amounts in multiples of $150,000.</p>
    <div class="trust-badges light">
        <span class="trust-badge">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" /></svg>
            SEC Reg D/Reg S
        </span>
        <span class="trust-badge">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21" /></svg>
            Wyoming DAO LLC
        </span>
        <span class="trust-badge">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            Zero Upfront Fees
        </span>
        <span class="trust-badge">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" /></svg>
            Success-Based Only
        </span>
    </div>
</section>
<div class="pricing-container">
    <div class="calculator-section">
        <h2>Calculate Your Costs</h2>
        <p class="intro">Adjust the parameters below to see exactly what you'll receive and pay over the life of your offering</p>
        <div class="calc-grid">
            <div class="calc-inputs">
                <div class="input-group">
                    <label for="softCap"><span class="glossary-term" data-term="soft-cap">Soft Cap</span> (Minimum Goal)</label>
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
                    <label for="hardCap"><span class="glossary-term" data-term="hard-cap">Hard Cap</span> (Maximum Goal)</label>
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
                    <label for="couponRate">Annual <span class="glossary-term" data-term="coupon">Coupon</span> Rate (%)</label>
                    <input type="number" id="couponRate" value="8" min="0" max="30" step="0.1">
                    <span class="input-hint">Annual interest rate paid to investors</span>
                </div>
                <div class="input-group">
                    <label for="termYears">Term (Years)</label>
                    <input type="number" id="termYears" value="3" min="1" max="30" step="1">
                    <span class="input-hint">Bond <span class="glossary-term" data-term="maturity">maturity</span> period</span>
                </div>
                <div class="input-group">
                    <label for="paymentFreq">Payment Frequency</label>
                    <select id="paymentFreq">
                        <option value="1">Annual</option>
                        <option value="2" selected>Semi-Annual</option>
                        <option value="4">Quarterly</option>
                        <option value="12">Monthly</option>
                    </select>
                    <span class="input-hint">How often <span class="glossary-term" data-term="coupon">coupon</span> payments are made</span>
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
                    <td><strong><span class="glossary-term" data-term="brokerage-fee">Brokerage Fee</span></strong></td>
                    <td><span class="fee-highlight">0.5%</span></td>
                    <td><span class="glossary-term" data-term="secondary-trading">Secondary trades</span> + post-<span class="glossary-term" data-term="soft-cap">soft cap</span> primary<br><em style="color:#38a169; font-size:0.85em;">⚡ Waived during <span class="glossary-term" data-term="soft-cap">soft cap</span> phase</em></td>
                    <td>Buyer</td>
                    <td>⅓ Platform + ⅓ Buy-side + ⅓ Sell-side</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="distribution-fee">Distribution Fee</span></strong></td>
                    <td><span class="fee-highlight">6% OR 1%</span></td>
                    <td>Deducted from <span class="glossary-term" data-term="soft-cap">soft cap</span> when reached<br><em style="color:#38a169; font-size:0.85em;">⚡ Not charged until <span class="glossary-term" data-term="soft-cap">soft cap</span> reached</em></td>
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
                    <td><strong><span class="glossary-term" data-term="security-deposit">Security Deposit</span></strong></td>
                    <td><span class="fee-highlight">3% of issuance</span></td>
                    <td>At issuance, reserved under <span class="glossary-term" data-term="trustee">trust</span></td>
                    <td>Issuer (from proceeds)</td>
                    <td>Reserved, returned at end</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="clearstream">Clearstream</span> Fees</strong></td>
                    <td>Variable</td>
                    <td>Channel 3 transactions</td>
                    <td>Investor</td>
                    <td>Clearstream</td>
                </tr>
                <tr>
                    <td><strong><span class="glossary-term" data-term="crossconversion">CrossConversion</span> Fee</strong></td>
                    <td><span class="fee-highlight">0.75%</span></td>
                    <td>When <span class="glossary-term" data-term="crossconversion">CrossConverting</span> between On-Chain ↔ Bankable form</td>
                    <td>Requester</td>
                    <td>Sails.to + Trust</td>
                </tr>
            </tbody>
        </table>
        <div class="note-box">
            <strong>📌 Key Points</strong>
            <ul>
                <li><strong><span class="glossary-term" data-term="soft-cap">Soft cap</span> phase is fee-free:</strong> <span class="glossary-term" data-term="brokerage-fee">Brokerage</span> (0.5%) waived, <span class="glossary-term" data-term="distribution-fee">distribution fees</span> deferred until <span class="glossary-term" data-term="soft-cap">soft cap</span> reached</li>
                <li><strong>If <span class="glossary-term" data-term="soft-cap">soft cap</span> fails:</strong> Full refund to investors (only <span class="glossary-term" data-term="clearstream">Clearstream</span> fees at cost, if used)</li>
                <li><strong>No upfront costs:</strong> All fees deducted from proceeds when offering succeeds</li>
                <li><strong><span class="glossary-term" data-term="security-deposit">Security deposit</span>:</strong> Returned at end of bond term if no issues</li>
            </ul>
        </div>
    </div>
</div>
