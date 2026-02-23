---
title: "Contact Us"
description: "Get in touch with the Sails.to team. For issuers, investors, brokers, or general inquiries about our CrossSecurities platform."
keywords:
  - contact sails.to
  - get in touch
  - support
  - inquiries
  - tokenization questions
ogImage: "/og-contact.png"
stylesheets:
  - "/styles.css"
  - "/assets/css/glossary.css"
  - "/assets/css/company-contact.css"
scripts:
  - "/js/company-contact.js"
---


<section class="page-hero">
    <span class="section-label">Get In Touch</span>
    <h1 class="section-title">Let's Talk</h1>
    <p class="section-desc">Whether you're ready to launch, exploring options, or have questions, we're here to help.</p>
</section>
<section class="contact-section">
    <div class="contact-container">
        <div class="contact-grid">
            <div class="contact-info">
                <div class="contact-card">
                    <span class="icon-wrapper"><svg><use href="#icon-mail"></use></svg></span>
                    <h3>Email Us</h3>
                    <p>For general inquiries and support</p>
                    <a href="mailto:hello@sails.to">hello@sails.to</a>
                </div>
                <div class="contact-card">
                    <span class="icon-wrapper"><svg><use href="#icon-message"></use></svg></span>
                    <h3>Telegram</h3>
                    <p>Join our community or DM us directly</p>
                    <a href="https://t.me/sailsto" target="_blank">@sailsto</a>
                </div>
                <div class="contact-card">
                    <span class="icon-wrapper"><svg><use href="#icon-briefcase"></use></svg></span>
                    <h3>LinkedIn</h3>
                    <p>Follow us for updates and announcements</p>
                    <a href="https://linkedin.com/company/sailsto" target="_blank">/company/sailsto</a>
                </div>
                <div class="contact-card">
                    <span class="icon-wrapper"><svg><use href="#icon-send"></use></svg></span>
                    <h3>Twitter/X</h3>
                    <p>Quick updates and industry commentary</p>
                    <a href="https://x.com/sailsto" target="_blank">@sailsto</a>
                </div>
                <div class="contact-divider"></div>
                <div class="contact-address">
                    <h4>Registered Address</h4>
                    <address>
                        Sails.to<br>
                        1712 Pioneer Ave, Suite 500<br>
                        Cheyenne, WY 82001<br>
                        United States
                    </address>
                </div>
                <div class="contact-hours">
                    <h4>Response Time</h4>
                    <p>We typically respond within 24 hours during business days (Monday–Friday, 9:00–18:00 CET).</p>
                </div>
            </div>
            <div class="contact-form-card">
                <div id="contact-form-wrapper">
                    <div class="form-header">
                        <h2>Send Us a Message</h2>
                        <p>Fill out the form and we'll get back to you shortly</p>
                    </div>
                    <form id="contact-form" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
                        <div class="form-group">
                            <label for="topic">How can we help?</label>
                            <select id="topic" name="topic" required>
                                <option value="">Select a topic</option>
                                <option value="issuer">I want to issue securities</option>
                                <option value="investor">I'm interested in investing</option>
                                <option value="broker">Broker partnership inquiry</option>
                                <option value="institution">Institutional services</option>
                                <option value="media">Press / Media inquiry</option>
                                <option value="technical">Technical question</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="name">Your Name *</label>
                                <input type="text" id="name" name="name" required>
                            </div>
                            <div class="form-group">
                                <label for="email">Email Address *</label>
                                <input type="email" id="email" name="email" required>
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="company">Company / Organization</label>
                            <input type="text" id="company" name="company">
                        </div>
                        <div class="form-group">
                            <label for="message">Your Message *</label>
                            <textarea id="message" name="message" required placeholder="Tell us about your project, question, or how we can help..."></textarea>
                        </div>
                        <div class="form-checkbox">
                            <input type="checkbox" id="consent" name="consent" required>
                            <label for="consent">I consent to Sails.to processing my data as described in the <a href="/company/legal/#privacy">Privacy Policy</a>. *</label>
                        </div>
                        <button type="submit" class="form-submit">Send Message</button>
                    </form>
                </div>
                <div class="form-success" id="form-success">
                    <span class="icon-wrapper"><svg><use href="#icon-check"></use></svg></span>
                    <h3>Message Sent!</h3>
                    <p>Thank you for reaching out. We'll get back to you within 24 hours.</p>
                    <a href="/" class="btn btn-primary">Back to Home</a>
                </div>
            </div>
        </div>
    </div>
</section>
<section class="quick-connect">
    <div class="quick-connect-container">
        <h2>Looking for Something Specific?</h2>
        <div class="quick-connect-grid">
            <a href="/signup/?type=issuer" class="quick-link">
                <span class="icon-wrapper"><svg><use href="#icon-building"></use></svg></span>
                <span class="text">
                    <strong>Launch a Token</strong>
                    <small>Start your issuance journey</small>
                </span>
            </a>
            <a href="/signup/?type=investor" class="quick-link">
                <span class="icon-wrapper"><svg><use href="#icon-briefcase"></use></svg></span>
                <span class="text">
                    <strong>Invest in Opportunities</strong>
                    <small>Access tokenized securities</small>
                </span>
            </a>
            <a href="/signup/?type=broker" class="quick-link">
                <span class="icon-wrapper"><svg><use href="#icon-handshake"></use></svg></span>
                <span class="text">
                    <strong>Become a Partner</strong>
                    <small>Broker referral program</small>
                </span>
            </a>
            <a href="/knowledge/faq/" class="quick-link">
                <span class="icon-wrapper"><svg><use href="#icon-info"></use></svg></span>
                <span class="text">
                    <strong>Read the FAQ</strong>
                    <small>Answers to common questions</small>
                </span>
            </a>
        </div>
    </div>
</section>

