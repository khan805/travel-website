from __future__ import annotations

import hashlib
import json
import os
import secrets
import threading
import time
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
USERS_FILE = DATA_DIR / "users.json"
SUBSCRIBERS_FILE = DATA_DIR / "subscribers.json"
CONTACT_MESSAGES_FILE = DATA_DIR / "contact_messages.json"

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jadoo Travel</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Volkhov:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <header class="site-header">
        <div class="container navbar">
            <a class="logo" href="/">Jadoo</a>
            <button class="menu-toggle" id="menuToggle" type="button" aria-expanded="false" aria-controls="siteMenu" aria-label="Open menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
            <div class="site-menu" id="siteMenu">
            <nav class="nav-links">
                <a href="#destinations">Destinations</a>
                <a href="#services">Services</a>
                <a href="#bookings">Bookings</a>
                <a href="#testimonials">Testimonials</a>
                <a href="#contact">Contact</a>
            </nav>
            <div class="nav-actions" id="navActions">
                <a class="text-link" href="/login.html">Login</a>
                <a class="outline-btn" href="/signup.html">Sign up</a>
            </div>
            </div>
        </div>
    </header>

    <main>
        <section class="hero-section">
            <div class="container hero">
                <div class="hero-copy">
                    <p class="eyebrow">Best Destinations Around The World</p>
                    <h1>Travel, enjoy and live a new and full life</h1>
                    <p class="hero-description">
                        Discover handpicked trips, stress-free bookings, and memorable experiences crafted for every kind of traveler.
                    </p>
                    <div class="hero-actions">
                        <a class="primary-btn" href="#destinations">Find out more</a>
                        <a class="play-link" href="#bookings">Plan my trip</a>
                    </div>
                </div>
                <div class="hero-visual">
                    <span class="hero-plane hero-plane-left" aria-hidden="true">✈</span>
                    <span class="hero-plane hero-plane-right" aria-hidden="true">✈</span>
                    <div class="hero-card floating-card top-card">
                        <span>Fast Booking</span>
                        <strong>24/7 support</strong>
                    </div>
                    <img
                        class="hero-traveler"
                        src="/traveler.png"
                        alt="Female traveler walking in an airport with a suitcase"
                    >
                    <div class="hero-card floating-card bottom-card">
                        <span>Top Rated Tours</span>
                        <strong>1,200+ happy travelers</strong>
                    </div>
                </div>
            </div>
        </section>

        <section class="section" id="services">
            <div class="container">
                <p class="section-label">Category</p>
                <h2 class="section-title">We Offer Best Services</h2>
                <div class="card-grid services-grid">
                    <article class="info-card">
                        <div class="icon-badge">01</div>
                        <h3>Calculated Weather</h3>
                        <p>Daily planning support with climate-aware schedules for smoother sightseeing.</p>
                    </article>
                    <article class="info-card featured-card">
                        <div class="icon-badge">02</div>
                        <h3>Best Flights</h3>
                        <p>Smart routing suggestions and flexible options to keep each journey efficient.</p>
                    </article>
                    <article class="info-card">
                        <div class="icon-badge">03</div>
                        <h3>Local Events</h3>
                        <p>Discover festivals, food tours, and hidden experiences curated by destination.</p>
                    </article>
                    <article class="info-card">
                        <div class="icon-badge">04</div>
                        <h3>Customization</h3>
                        <p>Personalized trip plans built around your pace, budget, and travel style.</p>
                    </article>
                </div>
            </div>
        </section>

        <section class="section section-soft" id="destinations">
            <div class="container">
                <p class="section-label">Top Selling</p>
                <h2 class="section-title">Top Destinations</h2>
                <div class="card-grid destination-grid">
                    <article class="destination-card">
                        <img
                            src="https://images.pexels.com/photos/36399043/pexels-photo-36399043.jpeg?auto=compress&cs=tinysrgb&w=1400"
                            alt="Rome, Italy historic architecture"
                        >
                        <div class="card-body">
                            <div class="card-headline">
                                <h3>Rome, Italy</h3>
                                <span>$5.42k</span>
                            </div>
                            <p>10 days trip with history walks, guided food stops, and boutique stays.</p>
                        </div>
                    </article>
                    <article class="destination-card">
                        <img
                            src="https://images.pexels.com/photos/34045028/pexels-photo-34045028.jpeg?auto=compress&cs=tinysrgb&w=1400"
                            alt="London skyline at sunset"
                        >
                        <div class="card-body">
                            <div class="card-headline">
                                <h3>London, UK</h3>
                                <span>$4.2k</span>
                            </div>
                            <p>12 days across landmarks, theater nights, and city neighborhoods.</p>
                        </div>
                    </article>
                    <article class="destination-card">
                        <img
                            src="https://images.pexels.com/photos/16238471/pexels-photo-16238471.jpeg?auto=compress&cs=tinysrgb&w=1400"
                            alt="Scenic alpine lake in Europe"
                        >
                        <div class="card-body">
                            <div class="card-headline">
                                <h3>Full Europe</h3>
                                <span>$15k</span>
                            </div>
                            <p>28 days connecting iconic capitals and scenic routes in one grand plan.</p>
                        </div>
                    </article>
                </div>
            </div>
        </section>

        <section class="section" id="bookings">
            <div class="container booking-layout">
                <div>
                    <p class="section-label">Easy And Fast</p>
                    <h2 class="section-title align-left">Book Your Next Trip In 3 Easy Steps</h2>
                    <div class="steps-list">
                        <article class="step-card">
                            <div class="step-number">1</div>
                            <div>
                                <h3>Choose Destination</h3>
                                <p>Select a route that fits your season, budget, and travel goals.</p>
                            </div>
                        </article>
                        <article class="step-card">
                            <div class="step-number">2</div>
                            <div>
                                <h3>Make Payment</h3>
                                <p>Confirm your booking securely with a simple and clear checkout flow.</p>
                            </div>
                        </article>
                        <article class="step-card">
                            <div class="step-number">3</div>
                            <div>
                                <h3>Reach Airport</h3>
                                <p>Get reminders, checklists, and updates before your departure.</p>
                            </div>
                        </article>
                    </div>
                </div>
                <aside class="trip-preview">
                    <img
                        src="https://images.pexels.com/photos/33343536/pexels-photo-33343536.jpeg?auto=compress&cs=tinysrgb&w=1400"
                        alt="Sunny beachfront view in Greece"
                    >
                    <h3>Trip To Greece</h3>
                    <p>14-29 June | by Robbin Joseph</p>
                    <div class="trip-meta">
                        <span>24 people going</span>
                        <span>Ongoing tracking</span>
                    </div>
                </aside>
            </div>
        </section>

        <section class="section section-soft" id="testimonials">
            <div class="container">
                <p class="section-label">Testimonials</p>
                <h2 class="section-title">What People Say About Us</h2>
                <div class="testimonial-card">
                    <p>
                        “The whole booking process felt calm and organized. We had a beautiful itinerary, clear travel support,
                        and every card on the site finally matches the quality of the service.”
                    </p>
                    <strong>Mike Taylor</strong>
                    <span>Islamabad, Pakistan</span>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="container newsletter-panel">
                <div>
                    <p class="section-label">Stay Connected</p>
                    <h2 class="section-title align-left">Subscribe to get information, latest news and other interesting offers</h2>
                </div>
                <form class="newsletter-form" id="newsletterForm">
                    <input type="email" id="newsletterEmail" placeholder="Your email address" required>
                    <button class="primary-btn" type="submit">Subscribe</button>
                </form>
                <p class="form-message" id="newsletterMessage" aria-live="polite"></p>
            </div>
        </section>
    </main>

    <footer class="site-footer" id="contact">
        <div class="container footer-layout">
            <div class="footer-brand">
                <a class="logo" href="/">Jadoo</a>
                <p>Smart travel planning with a polished booking experience.</p>
            </div>
            <div class="footer-links">
                <a href="/login.html">Login</a>
                <a href="/signup.html">Sign up</a>
                <a href="#destinations">Destinations</a>
            </div>
            <div class="footer-contact">
                <strong>Contact Us</strong>
                <a href="mailto:islamabad@jadootravel.local">islamabad@jadootravel.local</a>
                <a href="tel:+92512345678">+92 51 2345678</a>
                <span>Mon - Sat, 9:00 AM to 7:00 PM</span>
                <span>Blue Area, Islamabad, Pakistan</span>
            </div>
        </div>
    </footer>

    <script src="/site.js"></script>
</body>
</html>
"""

LOGIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login | Jadoo Travel</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Volkhov:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/style.css">
</head>
<body class="auth-page">
    <div class="auth-shell">
        <section class="auth-visual">
            <a class="logo" href="/">Jadoo</a>
            <p class="section-label">Welcome Back</p>
            <h1>Login to manage your next journey.</h1>
            <p class="auth-subtitle">Access your booking details, saved destinations, and upcoming travel plans from one place.</p>
            <ul>
                <li>Secure password-based login</li>
                <li>Local backend ready for your forms</li>
                <li>Fast access to your travel dashboard</li>
            </ul>
        </section>

        <section class="auth-card">
            <h2>Login</h2>
            <p class="auth-subtitle">Enter your email and password to continue.</p>
            <form class="auth-form" id="loginForm">
                <input type="email" id="loginEmail" name="email" placeholder="Email address" required>
                <input type="password" id="loginPassword" name="password" placeholder="Password" minlength="6" required>
                <button class="primary-btn" type="submit">Login</button>
            </form>
            <p class="form-message" id="authMessage" aria-live="polite"></p>
            <p class="auth-footer">New here? <a href="/signup.html">Create an account</a></p>
        </section>
    </div>

    <script src="/site.js"></script>
</body>
</html>
"""

SIGNUP_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up | Jadoo Travel</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Volkhov:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/style.css">
</head>
<body class="auth-page">
    <div class="auth-shell">
        <section class="auth-visual">
            <a class="logo" href="/">Jadoo</a>
            <p class="section-label">Join Jadoo</p>
            <h1>Create an account and start booking smarter.</h1>
            <p class="auth-subtitle">Build your travel profile and keep your favorite destinations, plans, and bookings together.</p>
            <ul>
                <li>Simple account creation</li>
                <li>Passwords stored as secure hashes</li>
                <li>Ready to connect with more backend features later</li>
            </ul>
        </section>

        <section class="auth-card">
            <h2>Sign Up</h2>
            <p class="auth-subtitle">Fill in your details to create an account.</p>
            <form class="auth-form" id="signupForm">
                <input type="text" id="signupName" name="name" placeholder="Full name" required>
                <input type="email" id="signupEmail" name="email" placeholder="Email address" required>
                <input type="password" id="signupPassword" name="password" placeholder="Password" minlength="6" required>
                <button class="primary-btn" type="submit">Create account</button>
            </form>
            <p class="form-message" id="authMessage" aria-live="polite"></p>
            <p class="auth-footer">Already have an account? <a href="/login.html">Login</a></p>
        </section>
    </div>

    <script src="/site.js"></script>
</body>
</html>
"""

CONTACT_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Us | Jadoo Travel</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Volkhov:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/style.css">
</head>
<body class="auth-page contact-page">
    <div class="auth-shell contact-shell">
        <section class="auth-visual contact-visual">
            <a class="logo" href="/">Jadoo</a>
            <p class="section-label">Contact Us</p>
            <h1>Let us help plan your next trip.</h1>
            <p class="auth-subtitle">Share your travel goals, preferred destinations, or booking questions and our team will get back to you.</p>
            <div class="contact-details">
                <div class="contact-detail-card">
                    <strong>Email</strong>
                    <span>islamabad@jadootravel.local</span>
                </div>
                <div class="contact-detail-card">
                    <strong>Phone</strong>
                    <span>+92 51 2345678</span>
                </div>
                <div class="contact-detail-card">
                    <strong>Hours</strong>
                    <span>Mon - Sat, 9:00 AM to 7:00 PM</span>
                </div>
            </div>
        </section>

        <section class="auth-card contact-card">
            <h2>Send a Message</h2>
            <p class="auth-subtitle">Tell us what you need and we will reply with the right travel support.</p>
            <form class="auth-form contact-form" id="contactForm">
                <input type="text" id="contactName" name="name" placeholder="Your name" required>
                <input type="email" id="contactEmail" name="email" placeholder="Your email address" required>
                <input type="text" id="contactSubject" name="subject" placeholder="Subject" required>
                <textarea id="contactMessageInput" name="message" placeholder="Write your message" rows="6" required></textarea>
                <button class="primary-btn" type="submit">Send message</button>
            </form>
            <p class="form-message" id="contactMessage" aria-live="polite"></p>
            <p class="auth-footer">Want to create an account too? <a href="/signup.html">Sign up</a></p>
        </section>
    </div>

    <script src="/site.js"></script>
</body>
</html>
"""

STYLE_CSS = r""":root {
    --bg: #fff7ef;
    --surface: #ffffff;
    --surface-soft: #f8fbff;
    --text: #1f1f39;
    --muted: #5f6285;
    --accent: #f1a501;
    --accent-dark: #df6951;
    --border: rgba(31, 31, 57, 0.08);
    --shadow: 0 18px 45px rgba(36, 42, 78, 0.12);
    --radius-lg: 28px;
    --radius-md: 20px;
    --container: 1180px;
}

* {
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    margin: 0;
    font-family: "Poppins", sans-serif;
    color: var(--text);
    background:
        radial-gradient(circle at top left, rgba(241, 165, 1, 0.12), transparent 28%),
        linear-gradient(180deg, #fffdf9 0%, #fff7ef 100%);
}

img {
    display: block;
    max-width: 100%;
}

a {
    color: inherit;
    text-decoration: none;
}

button,
input {
    font: inherit;
}

.container {
    width: min(calc(100% - 32px), var(--container));
    margin: 0 auto;
}

.site-header {
    position: sticky;
    top: 0;
    z-index: 20;
    backdrop-filter: blur(12px);
    background: rgba(255, 253, 249, 0.88);
    border-bottom: 1px solid rgba(31, 31, 57, 0.04);
}

.navbar {
    min-height: 88px;
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: center;
    gap: 20px;
    position: relative;
}

.logo {
    font-family: "Volkhov", serif;
    font-size: 2rem;
    font-weight: 700;
}

.site-menu {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    width: 100%;
    gap: 28px;
}

.nav-links,
.nav-actions,
.footer-links,
.footer-contact {
    display: flex;
    align-items: center;
    gap: 24px;
}

.nav-links {
    grid-column: 2;
    justify-content: center;
}

.nav-actions {
    grid-column: 3;
    justify-self: end;
}

.nav-links a,
.text-link,
.footer-links a,
.footer-contact a {
    color: var(--muted);
    transition: color 0.2s ease;
}

.nav-links a:hover,
.text-link:hover,
.footer-links a:hover,
.footer-contact a:hover {
    color: var(--text);
}

.outline-btn,
.primary-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    padding: 14px 24px;
    font-weight: 600;
    transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
}

.outline-btn {
    border: 1px solid var(--text);
}

.primary-btn {
    border: 0;
    background: var(--accent);
    color: #fff;
    box-shadow: 0 14px 25px rgba(241, 165, 1, 0.28);
}

.outline-btn:hover,
.primary-btn:hover,
.play-link:hover {
    transform: translateY(-1px);
}

.menu-toggle {
    display: none;
    width: 48px;
    height: 48px;
    border: 1px solid rgba(31, 31, 57, 0.12);
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.92);
    align-items: center;
    justify-content: center;
    gap: 5px;
    flex-direction: column;
    margin-left: auto;
}

.menu-toggle span {
    width: 18px;
    height: 2px;
    background: var(--text);
    border-radius: 999px;
    transition: transform 0.2s ease, opacity 0.2s ease;
}

.hero-section {
    padding: 56px 0 24px;
}

.hero {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    align-items: center;
    gap: 48px;
}

.hero-copy {
    position: relative;
    z-index: 3;
}

.eyebrow,
.section-label {
    margin: 0 0 16px;
    color: var(--accent-dark);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.82rem;
    font-weight: 700;
}

.hero-copy h1,
.section-title {
    margin: 0;
    font-family: "Volkhov", serif;
    line-height: 1.08;
}

.hero-copy h1 {
    font-size: clamp(3rem, 5vw, 5.2rem);
    max-width: 10ch;
}

.hero-description,
.info-card p,
.destination-card p,
.step-card p,
.trip-preview p,
.testimonial-card p,
.newsletter-panel p,
.site-footer p,
.form-message,
.auth-subtitle {
    color: var(--muted);
    line-height: 1.75;
}

.hero-actions {
    display: flex;
    align-items: center;
    gap: 18px;
    margin-top: 32px;
    flex-wrap: wrap;
}

.play-link {
    font-weight: 600;
    color: var(--text);
}

.hero-visual {
    position: relative;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    min-height: 560px;
    padding: 26px 20px 12px;
    overflow: hidden;
    z-index: 1;
}

.hero-visual::before {
    content: "";
    position: absolute;
    inset: 30px 40px 35px;
    border-radius: 42% 58% 50% 50% / 28% 28% 72% 72%;
    background:
        radial-gradient(circle at 55% 38%, rgba(255, 220, 160, 0.88) 0%, rgba(255, 220, 160, 0.42) 28%, rgba(255, 220, 160, 0) 62%),
        linear-gradient(180deg, #fff4dc 0%, #fff7e9 100%);
    z-index: -1;
}

.hero-visual img {
    width: min(100%, 500px);
}

.hero-traveler {
    filter: saturate(1.06) contrast(1.03) brightness(1.02);
    position: relative;
    z-index: 2;
}

.hero-plane {
    position: absolute;
    font-size: 2rem;
    color: #1d9bd1;
    text-shadow: 0 10px 18px rgba(29, 155, 209, 0.18);
    line-height: 1;
}

.hero-plane-left {
    left: 12px;
    top: 145px;
    transform: rotate(-18deg);
}

.hero-plane-right {
    right: 20px;
    top: 170px;
    transform: scaleX(-1) rotate(-8deg);
}

.hero-card {
    background: var(--surface);
    border-radius: 18px;
    box-shadow: var(--shadow);
    padding: 18px 20px;
    min-width: 180px;
}

.hero-card span {
    display: block;
    color: var(--muted);
    font-size: 0.85rem;
}

.floating-card {
    position: absolute;
}

.top-card {
    top: 70px;
    right: 20px;
    z-index: 3;
}

.bottom-card {
    left: 10px;
    bottom: 100px;
    z-index: 3;
}

.section {
    padding: 56px 0;
}

.section-soft {
    background: linear-gradient(180deg, rgba(248, 251, 255, 0.3) 0%, rgba(255, 255, 255, 0.75) 100%);
}

.section-title {
    font-size: clamp(2rem, 4vw, 3.25rem);
    text-align: center;
    margin-bottom: 36px;
}

.align-left {
    text-align: left;
}

.card-grid {
    display: grid;
    gap: 24px;
    align-items: stretch;
}

.services-grid {
    grid-template-columns: repeat(4, minmax(0, 1fr));
}

.destination-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
}

.info-card,
.destination-card,
.step-card,
.testimonial-card,
.trip-preview,
.newsletter-panel,
.auth-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow);
}

.info-card,
.destination-card {
    height: 100%;
}

.info-card {
    padding: 28px;
    text-align: left;
}

.featured-card {
    transform: translateY(-6px);
}

.icon-badge,
.step-number {
    width: 52px;
    height: 52px;
    border-radius: 16px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: rgba(241, 165, 1, 0.14);
    color: var(--accent-dark);
    font-weight: 700;
}

.info-card h3,
.destination-card h3,
.step-card h3,
.trip-preview h3 {
    margin: 18px 0 12px;
    font-size: 1.2rem;
}

.destination-card {
    overflow: hidden;
}

.destination-card img {
    width: 100%;
    height: 280px;
    object-fit: cover;
}

.card-body {
    padding: 24px;
}

.card-headline {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
}

.card-headline h3 {
    margin: 0;
}

.card-headline span,
.trip-meta span {
    color: var(--muted);
    font-size: 0.95rem;
    font-weight: 600;
}

.booking-layout {
    display: grid;
    grid-template-columns: 1.1fr 0.9fr;
    gap: 40px;
    align-items: center;
}

.steps-list {
    display: grid;
    gap: 18px;
}

.step-card {
    padding: 22px 24px;
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 18px;
    align-items: start;
}

.step-card h3 {
    margin-top: 4px;
}

.trip-preview {
    padding: 24px;
}

.trip-preview img {
    width: 100%;
    height: 320px;
    object-fit: cover;
    border-radius: 22px;
}

.trip-meta {
    display: flex;
    gap: 18px;
    flex-wrap: wrap;
    margin-top: 18px;
}

.testimonial-card {
    max-width: 760px;
    margin: 0 auto;
    padding: 34px;
    text-align: center;
}

.testimonial-card strong,
.testimonial-card span {
    display: block;
}

.newsletter-panel {
    padding: 32px;
    display: grid;
    gap: 18px;
}

.newsletter-form,
.auth-form {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 14px;
}

.newsletter-form input,
.auth-form input {
    width: 100%;
    border: 1px solid rgba(31, 31, 57, 0.14);
    border-radius: 16px;
    padding: 16px 18px;
    background: #fffdfb;
}

.form-message {
    min-height: 28px;
    margin: 0;
}

.site-footer {
    padding: 24px 0 40px;
}

.footer-layout {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    align-items: center;
    border-top: 1px solid rgba(31, 31, 57, 0.08);
    padding-top: 28px;
}

.footer-brand {
    max-width: 280px;
}

.footer-contact {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
}

.footer-contact strong {
    font-size: 1rem;
}

.footer-contact span {
    color: var(--muted);
    line-height: 1.6;
}

.auth-page {
    min-height: 100vh;
    display: grid;
    place-items: center;
    padding: 40px 16px;
}

.auth-shell {
    width: min(100%, 1080px);
    display: grid;
    grid-template-columns: 0.95fr 1.05fr;
    background: rgba(255, 255, 255, 0.76);
    border: 1px solid rgba(31, 31, 57, 0.08);
    border-radius: 36px;
    overflow: hidden;
    box-shadow: var(--shadow);
}

.auth-visual {
    padding: 48px;
    background:
        linear-gradient(180deg, rgba(241, 165, 1, 0.18) 0%, rgba(223, 105, 81, 0.08) 100%),
        #fff5e8;
    display: grid;
    align-content: center;
    gap: 18px;
}

.auth-visual h1 {
    margin: 0;
    font-family: "Volkhov", serif;
    font-size: clamp(2.4rem, 4vw, 3.8rem);
}

.auth-visual ul {
    margin: 0;
    padding-left: 18px;
    color: var(--muted);
    line-height: 1.8;
}

.auth-card {
    padding: 40px;
    border: 0;
    box-shadow: none;
    border-radius: 0;
}

.auth-card h2 {
    margin: 0 0 8px;
    font-size: 2rem;
}

.auth-form {
    grid-template-columns: 1fr;
    margin-top: 28px;
}

.auth-form button {
    width: 100%;
}

.auth-footer {
    margin-top: 18px;
    color: var(--muted);
}

.auth-footer a {
    color: var(--accent-dark);
    font-weight: 600;
}

.contact-shell {
    grid-template-columns: 0.9fr 1.1fr;
}

.contact-visual {
    gap: 22px;
}

.contact-details {
    display: grid;
    gap: 14px;
}

.contact-detail-card {
    padding: 16px 18px;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.72);
    border: 1px solid rgba(31, 31, 57, 0.08);
}

.contact-detail-card strong,
.contact-detail-card span {
    display: block;
}

.contact-detail-card span {
    color: var(--muted);
    margin-top: 6px;
}

.contact-form {
    grid-template-columns: 1fr;
}

.contact-form textarea {
    width: 100%;
    border: 1px solid rgba(31, 31, 57, 0.14);
    border-radius: 16px;
    padding: 16px 18px;
    background: #fffdfb;
    font: inherit;
    resize: vertical;
    min-height: 140px;
}

@media (max-width: 1024px) {
    .hero,
    .booking-layout,
    .auth-shell,
    .contact-shell {
        grid-template-columns: 1fr;
    }

    .hero-visual {
        min-height: auto;
    }

    .floating-card {
        position: static;
        margin: 12px 0;
    }

    .hero-visual {
        gap: 12px;
        flex-direction: column;
    }

    .services-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 760px) {
    .site-header {
        position: static;
    }

    .navbar {
        min-height: auto;
        padding: 18px 0;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
    }

    .menu-toggle {
        display: inline-flex;
    }

    .site-menu {
        display: none;
        width: 100%;
        grid-template-columns: 1fr;
        align-items: stretch;
        gap: 18px;
        padding: 18px;
        border: 1px solid rgba(31, 31, 57, 0.08);
        border-radius: 22px;
        background: rgba(255, 255, 255, 0.98);
        box-shadow: 0 20px 35px rgba(31, 31, 57, 0.08);
    }

    .site-menu.open {
        display: flex;
    }

    .nav-links,
    .nav-actions,
    .footer-layout,
    .footer-contact {
        flex-direction: column;
        align-items: flex-start;
    }

    .nav-links,
    .nav-actions {
        grid-column: auto;
        width: 100%;
        gap: 12px;
    }

    .nav-actions {
        justify-self: stretch;
    }

    .nav-links a,
    .nav-actions a,
    .nav-actions span {
        width: 100%;
    }

    .nav-actions .outline-btn,
    .nav-actions .text-link {
        justify-content: center;
    }

    .hero-section {
        padding: 30px 0 8px;
    }

    .section {
        padding: 38px 0;
    }

    .hero-copy h1 {
        max-width: none;
        font-size: clamp(2.2rem, 11vw, 3.2rem);
    }

    .hero-description {
        font-size: 0.98rem;
    }

    .hero-actions {
        gap: 12px;
    }

    .hero-actions .primary-btn,
    .hero-actions .play-link {
        width: 100%;
        justify-content: center;
    }

    .hero-visual {
        min-height: auto;
    }

    .hero-card {
        width: 100%;
        min-width: 0;
    }

    .services-grid,
    .destination-grid {
        grid-template-columns: 1fr;
    }

    .newsletter-form {
        grid-template-columns: 1fr;
    }

    .newsletter-form .primary-btn,
    .auth-form .primary-btn {
        width: 100%;
    }

    .auth-visual,
    .auth-card,
    .newsletter-panel,
    .testimonial-card {
        padding: 28px 22px;
    }

    .step-card {
        grid-template-columns: 1fr;
    }

    .card-body,
    .trip-preview,
    .info-card {
        padding: 22px 18px;
    }

    .destination-card img,
    .trip-preview img {
        height: 220px;
    }

    .card-headline {
        flex-direction: column;
        align-items: flex-start;
    }

    .newsletter-panel {
        gap: 14px;
    }

    .footer-layout {
        align-items: flex-start;
    }
}

@media (max-width: 480px) {
    body {
        font-size: 15px;
    }

    .container {
        width: min(calc(100% - 24px), var(--container));
    }

    .logo {
        font-size: 1.7rem;
    }

    .section-title,
    .auth-card h2 {
        font-size: 1.8rem;
    }

    .eyebrow,
    .section-label {
        font-size: 0.72rem;
        letter-spacing: 0.1em;
    }

    .primary-btn,
    .outline-btn,
    .newsletter-form input,
    .auth-form input {
        padding: 14px 16px;
    }

    .auth-page {
        padding: 16px 10px;
    }

    .auth-shell {
        border-radius: 28px;
    }

    .auth-visual h1 {
        font-size: 2rem;
    }

    .trip-meta {
        flex-direction: column;
        gap: 8px;
    }

    .testimonial-card p {
        font-size: 0.95rem;
    }

    .contact-detail-card {
        padding: 14px 16px;
    }
}
"""

SITE_JS = r"""const authStorageKey = "jadooUser";

function setMessage(element, message, isError = false) {
    if (!element) {
        return;
    }

    element.textContent = message;
    element.style.color = isError ? "#c2410c" : "#2f6b3f";
}

function updateNavigation() {
    const navActions = document.getElementById("navActions");
    if (!navActions) {
        return;
    }

    const storedUser = localStorage.getItem(authStorageKey);
    if (!storedUser) {
        return;
    }

    try {
        const user = JSON.parse(storedUser);
        navActions.innerHTML = `
            <span class="text-link">Hi, ${user.name}</span>
            <a class="outline-btn" href="#" id="logoutBtn">Logout</a>
        `;

        const logoutBtn = document.getElementById("logoutBtn");
        logoutBtn?.addEventListener("click", (event) => {
            event.preventDefault();
            localStorage.removeItem(authStorageKey);
            window.location.reload();
        });
    } catch (error) {
        localStorage.removeItem(authStorageKey);
    }
}

async function postJson(url, payload) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.message || "Something went wrong.");
    }

    return data;
}

function setupNewsletterForm() {
    const form = document.getElementById("newsletterForm");
    const message = document.getElementById("newsletterMessage");
    if (!form || !message) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const email = document.getElementById("newsletterEmail").value.trim();

        try {
            const data = await postJson("/api/subscribe", { email });
            form.reset();
            setMessage(message, data.message);
        } catch (error) {
            setMessage(message, error.message, true);
        }
    });
}

function setupLoginForm() {
    const form = document.getElementById("loginForm");
    const message = document.getElementById("authMessage");
    if (!form || !message) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const email = document.getElementById("loginEmail").value.trim();
        const password = document.getElementById("loginPassword").value;

        try {
            const data = await postJson("/api/login", { email, password });
            localStorage.setItem(authStorageKey, JSON.stringify(data.user));
            setMessage(message, data.message);
            window.setTimeout(() => {
                window.location.href = "/";
            }, 800);
        } catch (error) {
            setMessage(message, error.message, true);
        }
    });
}

function setupSignupForm() {
    const form = document.getElementById("signupForm");
    const message = document.getElementById("authMessage");
    if (!form || !message) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const name = document.getElementById("signupName").value.trim();
        const email = document.getElementById("signupEmail").value.trim();
        const password = document.getElementById("signupPassword").value;

        try {
            const data = await postJson("/api/signup", { name, email, password });
            localStorage.setItem(authStorageKey, JSON.stringify(data.user));
            setMessage(message, data.message);
            window.setTimeout(() => {
                window.location.href = "/";
            }, 800);
        } catch (error) {
            setMessage(message, error.message, true);
        }
    });
}

function setupContactForm() {
    const form = document.getElementById("contactForm");
    const message = document.getElementById("contactMessage");
    if (!form || !message) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const name = document.getElementById("contactName").value.trim();
        const email = document.getElementById("contactEmail").value.trim();
        const subject = document.getElementById("contactSubject").value.trim();
        const contactMessage = document.getElementById("contactMessageInput").value.trim();

        try {
            const data = await postJson("/api/contact", { name, email, subject, message: contactMessage });
            form.reset();
            setMessage(message, data.message);
        } catch (error) {
            setMessage(message, error.message, true);
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const menuToggle = document.getElementById("menuToggle");
    const siteMenu = document.getElementById("siteMenu");
    if (menuToggle && siteMenu) {
        menuToggle.addEventListener("click", () => {
            const isOpen = siteMenu.classList.toggle("open");
            menuToggle.setAttribute("aria-expanded", String(isOpen));
        });

        siteMenu.querySelectorAll("a").forEach((link) => {
            link.addEventListener("click", () => {
                siteMenu.classList.remove("open");
                menuToggle.setAttribute("aria-expanded", "false");
            });
        });
    }

    updateNavigation();
    setupNewsletterForm();
    setupLoginForm();
    setupSignupForm();
    setupContactForm();
});
"""

INLINE_TEXT_FILES = {
    "/": ("text/html; charset=utf-8", INDEX_HTML),
    "/index.html": ("text/html; charset=utf-8", INDEX_HTML),
    "/login.html": ("text/html; charset=utf-8", LOGIN_HTML),
    "/signup.html": ("text/html; charset=utf-8", SIGNUP_HTML),
    "/contact.html": ("text/html; charset=utf-8", CONTACT_HTML),
    "/style.css": ("text/css; charset=utf-8", STYLE_CSS),
    "/site.js": ("application/javascript; charset=utf-8", SITE_JS),
}

IMAGE_FILES = {
    "/hero-female.jpg": BASE_DIR / "hero-female.jpg",
    "/hero-female-enhanced.jpg": BASE_DIR / "hero-female-enhanced.jpg",
    "/traveler.png": BASE_DIR / "traveler.png",
}

MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".svg": "image/svg+xml",
}

def ensure_data_files() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    for file_path in (USERS_FILE, SUBSCRIBERS_FILE, CONTACT_MESSAGES_FILE):
        if not file_path.exists():
            file_path.write_text("[]", encoding="utf-8")


def read_json(file_path: Path) -> list[dict]:
    ensure_data_files()
    return json.loads(file_path.read_text(encoding="utf-8"))


def write_json(file_path: Path, payload: list[dict]) -> None:
    ensure_data_files()
    file_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    selected_salt = salt or secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        selected_salt.encode("utf-8"),
        100_000,
    ).hex()
    return selected_salt, password_hash


def open_browser_when_ready(port: int) -> None:
    if os.environ.get("JADOO_OPEN_BROWSER", "1") != "1":
        return

    def _open() -> None:
        time.sleep(1)
        webbrowser.open(f"http://127.0.0.1:{port}")

    threading.Thread(target=_open, daemon=True).start()


class TravelRequestHandler(BaseHTTPRequestHandler):
    server_version = "JadooTravel/1.1"

    def do_HEAD(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        if parsed.path in INLINE_TEXT_FILES:
            content_type, content = INLINE_TEXT_FILES[parsed.path]
            body = content.encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            return

        image_path = IMAGE_FILES.get(parsed.path)
        if image_path and image_path.exists():
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", MIME_TYPES.get(image_path.suffix, "application/octet-stream"))
            self.send_header("Content-Length", str(image_path.stat().st_size))
            self.end_headers()
            return

        self.send_response(HTTPStatus.NOT_FOUND)
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self.send_json(HTTPStatus.OK, {"status": "ok"})
            return

        if parsed.path in INLINE_TEXT_FILES:
            content_type, content = INLINE_TEXT_FILES[parsed.path]
            self.send_bytes(HTTPStatus.OK, content.encode("utf-8"), content_type)
            return

        image_path = IMAGE_FILES.get(parsed.path)
        if image_path and image_path.exists():
            self.send_bytes(
                HTTPStatus.OK,
                image_path.read_bytes(),
                MIME_TYPES.get(image_path.suffix, "application/octet-stream"),
            )
            return

        self.send_json(HTTPStatus.NOT_FOUND, {"message": "Page not found."})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/signup":
            self.handle_signup()
            return
        if parsed.path == "/api/login":
            self.handle_login()
            return
        if parsed.path == "/api/subscribe":
            self.handle_subscribe()
            return
        if parsed.path == "/api/contact":
            self.handle_contact()
            return

        self.send_json(HTTPStatus.NOT_FOUND, {"message": "Endpoint not found."})

    def handle_signup(self) -> None:
        payload = self.read_payload()
        name = payload.get("name", "").strip()
        email = payload.get("email", "").strip().lower()
        password = payload.get("password", "")

        if not name or not email or len(password) < 6:
            self.send_json(HTTPStatus.BAD_REQUEST, {"message": "Name, email, and a 6+ character password are required."})
            return

        users = read_json(USERS_FILE)
        if any(user["email"] == email for user in users):
            self.send_json(HTTPStatus.CONFLICT, {"message": "An account with this email already exists."})
            return

        salt, password_hash = hash_password(password)
        users.append({
            "name": name,
            "email": email,
            "salt": salt,
            "password_hash": password_hash,
        })
        write_json(USERS_FILE, users)
        self.send_json(HTTPStatus.CREATED, {
            "message": "Account created successfully.",
            "user": {"name": name, "email": email},
        })

    def handle_login(self) -> None:
        payload = self.read_payload()
        email = payload.get("email", "").strip().lower()
        password = payload.get("password", "")

        if not email or not password:
            self.send_json(HTTPStatus.BAD_REQUEST, {"message": "Email and password are required."})
            return

        users = read_json(USERS_FILE)
        matching_user = next((user for user in users if user["email"] == email), None)
        if not matching_user:
            self.send_json(HTTPStatus.UNAUTHORIZED, {"message": "Invalid email or password."})
            return

        _, password_hash = hash_password(password, matching_user["salt"])
        if password_hash != matching_user["password_hash"]:
            self.send_json(HTTPStatus.UNAUTHORIZED, {"message": "Invalid email or password."})
            return

        self.send_json(HTTPStatus.OK, {
            "message": "Login successful.",
            "user": {"name": matching_user["name"], "email": matching_user["email"]},
        })

    def handle_subscribe(self) -> None:
        payload = self.read_payload()
        email = payload.get("email", "").strip().lower()
        if "@" not in email:
            self.send_json(HTTPStatus.BAD_REQUEST, {"message": "Please enter a valid email address."})
            return

        subscribers = read_json(SUBSCRIBERS_FILE)
        if any(entry["email"] == email for entry in subscribers):
            self.send_json(HTTPStatus.OK, {"message": "You are already subscribed."})
            return

        subscribers.append({"email": email})
        write_json(SUBSCRIBERS_FILE, subscribers)
        self.send_json(HTTPStatus.OK, {"message": "Thanks for subscribing."})

    def handle_contact(self) -> None:
        payload = self.read_payload()
        name = payload.get("name", "").strip()
        email = payload.get("email", "").strip().lower()
        subject = payload.get("subject", "").strip()
        message = payload.get("message", "").strip()

        if not name or "@" not in email or not subject or len(message) < 10:
            self.send_json(
                HTTPStatus.BAD_REQUEST,
                {"message": "Please complete all fields and write a message of at least 10 characters."},
            )
            return

        contact_messages = read_json(CONTACT_MESSAGES_FILE)
        contact_messages.append({
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
        })
        write_json(CONTACT_MESSAGES_FILE, contact_messages)
        self.send_json(HTTPStatus.OK, {"message": "Your message has been sent successfully."})

    def read_payload(self) -> dict:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw_payload = self.rfile.read(content_length).decode("utf-8") if content_length else "{}"
        try:
            return json.loads(raw_payload)
        except json.JSONDecodeError:
            self.send_json(HTTPStatus.BAD_REQUEST, {"message": "Invalid JSON payload."})
            return {}

    def send_json(self, status: HTTPStatus, payload: dict) -> None:
        self.send_bytes(status, json.dumps(payload).encode("utf-8"), "application/json; charset=utf-8")

    def send_bytes(self, status: HTTPStatus, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        return


def run() -> None:
    ensure_data_files()
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), TravelRequestHandler)
    open_browser_when_ready(port)
    print(f"Serving Jadoo Travel on http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
