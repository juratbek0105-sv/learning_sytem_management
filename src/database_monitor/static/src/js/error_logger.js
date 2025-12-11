/** @odoo-module **/

import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";

const errorHandlerService = {
    dependencies: [],
    start() {
        // Catch unhandled promise rejections
        browser.addEventListener("unhandledrejection", (event) => {
            const error = event.reason;
            sendErrorToBackend({
                type: "UncaughtPromiseError",
                message: error?.message || String(error),
                stack: error?.stack || "",
                url: window.location.href,
                userAgent: navigator.userAgent,
                timestamp: new Date().toISOString(),
            });
        });

        // Catch general JavaScript errors
        browser.addEventListener("error", (event) => {
            sendErrorToBackend({
                type: "JavaScript Error",
                message: event.message || "Unknown error",
                stack: event.error?.stack || "",
                url: window.location.href,
                line: event.lineno,
                column: event.colno,
                filename: event.filename,
                userAgent: navigator.userAgent,
                timestamp: new Date().toISOString(),
            });
        });

        console.log("Telegram Error Logger initialized");
    },
};

/**
 * Send error data to backend
 */
function sendErrorToBackend(errorData) {
    // Use fetch to avoid dependency issues
    fetch("/telegram/log_js_error", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            jsonrpc: "2.0",
            method: "call",
            params: {
                error_data: errorData,
            },
        }),
    }).catch((err) => {
        console.error("Failed to send error to Telegram:", err);
    });
}

registry.category("services").add("telegram_error_handler", errorHandlerService);