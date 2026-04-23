const authStorageKey = "jadooUser";

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
                window.location.href = "index.html";
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
                window.location.href = "index.html";
            }, 800);
        } catch (error) {
            setMessage(message, error.message, true);
        }
    });
}

// ✅ Mobile nav toggle
function setupMobileNav() {
    const navToggle = document.getElementById("navToggle");
    const navLinks = document.getElementById("navLinks");
    const navActions = document.getElementById("navActions");

    if (!navToggle || !navLinks || !navActions) {
        return;
    }

    navToggle.addEventListener("click", () => {
        navLinks.classList.toggle("active");
        navActions.classList.toggle("active");
    });
}