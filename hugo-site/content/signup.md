---
title: "Get Started"
description: "Join the Sails.to platform. Whether you're an issuer, investor, broker, or institution, start your journey with compliant tokenized securities."
stylesheets:
  - "/assets/fonts/fonts.css"
  - "/styles.css"
  - "/assets/css/glossary.css"
---


    <section class="signup-section">
        <div class="signup-container">
            <div class="signup-content">
                <h1>Start Your Journey with Hybrid Securities</h1>
                <p>Join the platform that bridges blockchain innovation with traditional finance infrastructure. Whether you're raising capital or seeking investment opportunities, we're here to help.</p>
                <ul class="signup-benefits">
                    <li>
                        <span class="icon">💰</span>
                        <div class="text">
                            <h4>Zero Upfront Cost</h4>
                            <p>Soft cap phase is fee-free. After soft cap: 1% direct, 6% via broker</p>
                        </div>
                    </li>
                    <li>
                        <span class="icon">⚡</span>
                        <div class="text">
                            <h4>1-2 Weeks to Launch</h4>
                            <p>Turnkey Wyoming DAO LLC structure included</p>
                        </div>
                    </li>
                    <li>
                        <span class="icon">🔄</span>
                        <div class="text">
                            <h4>Hybrid Custody</h4>
                            <p>Hold on Solana or convert to ISIN for bank custody</p>
                        </div>
                    </li>
                    <li>
                        <span class="icon">✅</span>
                        <div class="text">
                            <h4>Built-in Compliance</h4>
                            <p>KYC/AML, Reg S/Reg D, investor eligibility on-chain</p>
                        </div>
                    </li>
                </ul>
            </div>
            <div class="signup-form-card">
                <div id="signup-form-wrapper">
                    <div class="form-header">
                        <h2>Join the Waitlist</h2>
                        <p>Tell us about yourself and we'll be in touch within 24 hours</p>
                    </div>
                    <form id="signup-form" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
                        <div class="user-type-grid">
                            <button type="button" class="user-type-btn" data-type="issuer">
                                <span class="icon">🏢</span>
                                <span class="label">Issuer</span>
                            </button>
                            <button type="button" class="user-type-btn" data-type="investor">
                                <span class="icon">💼</span>
                                <span class="label">Investor</span>
                            </button>
                            <button type="button" class="user-type-btn" data-type="broker">
                                <span class="icon">🤝</span>
                                <span class="label">Broker</span>
                            </button>
                            <button type="button" class="user-type-btn" data-type="institution">
                                <span class="icon">🏛️</span>
                                <span class="label">Institution</span>
                            </button>
                        </div>
                        <input type="hidden" name="user_type" id="user-type-input" value="">
                        <div class="form-row">
                            <div class="form-group">
                                <label for="first-name">First Name *</label>
                                <input type="text" id="first-name" name="first_name" required>
                            </div>
                            <div class="form-group">
                                <label for="last-name">Last Name *</label>
                                <input type="text" id="last-name" name="last_name" required>
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="email">Email Address *</label>
                            <input type="email" id="email" name="email" required>
                        </div>
                        <div class="form-group">
                            <label for="company">Company / Organization</label>
                            <input type="text" id="company" name="company">
                        </div>
                        <div class="form-group">
                            <label for="country">Country *</label>
                            <select id="country" name="country" required>
                                <option value="">Select your country</option>
                                <option value="US">United States</option>
                                <option value="GB">United Kingdom</option>
                                <option value="DE">Germany</option>
                                <option value="FR">France</option>
                                <option value="CH">Switzerland</option>
                                <option value="SG">Singapore</option>
                                <option value="HK">Hong Kong</option>
                                <option value="AE">United Arab Emirates</option>
                                <option value="LU">Luxembourg</option>
                                <option value="OTHER">Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="interest">Tell us about your interest</label>
                            <textarea id="interest" name="interest" placeholder="What brings you to Sails.to? What are you looking to achieve?"></textarea>
                        </div>
                        <div class="form-checkbox">
                            <input type="checkbox" id="professional" name="professional_investor" required>
                            <label for="professional">I confirm that I am a <span class="glossary-term" data-term="professional-investor">professional</span> or <span class="glossary-term" data-term="accredited-investor">accredited investor</span>, or I am inquiring on behalf of a professional entity. *</label>
                        </div>
                        <div class="form-checkbox">
                            <input type="checkbox" id="terms" name="agree_terms" required>
                            <label for="terms">I agree to the <a href="/company/legal/">Terms of Service</a> and <a href="/company/legal/#privacy">Privacy Policy</a>. *</label>
                        </div>
                        <button type="submit" class="form-submit">Submit Application</button>
                    </form>
                </div>
                <div class="form-success" id="form-success">
                    <span class="icon">✅</span>
                    <h3>Thank You!</h3>
                    <p>Your application has been received. A member of our team will be in touch within 24 hours.</p>
                    <div class="social-links">
                        <a href="https://t.me/sailsto" class="social-link" target="_blank">Join Telegram</a>
                        <a href="https://linkedin.com/company/sailsto" class="social-link" target="_blank">Follow LinkedIn</a>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
