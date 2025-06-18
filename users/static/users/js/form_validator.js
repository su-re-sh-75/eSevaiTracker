document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const passwordInput = document.querySelector("#userPassword");
    const confirmInput = document.querySelector("#userConfrimPassword");
    const errorText = document.querySelector("#passwordError");

    confirmInput.addEventListener("input", () => {
        if (confirmInput.value === "") {
            errorText.classList.add("hidden");
            return;
        }

        if (passwordInput.value === confirmInput.value) {
            errorText.classList.remove("hidden", "text-error");
            errorText.classList.add("text-success");
            errorText.textContent = "Passwords match ✅";
        } else {
            errorText.classList.remove("hidden", "text-success");
            errorText.classList.add("text-error");
            errorText.textContent = "Passwords do not match ❌";
        }

        clearTimeout(window.passwordMsgTimer);
        window.passwordMsgTimer = setTimeout(() => {
            errorText.classList.add("hidden");
        }, 5000);
    });

    form.addEventListener("submit", (e) => {
        if (passwordInput.value !== confirmInput.value) {
            e.preventDefault();
            errorText.classList.remove("hidden", "text-success");
            errorText.classList.add("text-error");
            errorText.textContent = "Passwords do not match ❌";

            clearTimeout(window.passwordMsgTimer);
            window.passwordMsgTimer = setTimeout(() => {
                errorText.classList.add("hidden");
            }, 5000);
        }
    });
});
