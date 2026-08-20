/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Interaction } from "@web/public/interaction";
import { MetaSidePanel } from "@rj_meta_common_v2/js/meta_side_panel_core";

/**
 * Public interaction: boot the OWL panel from layout-injected JSON config.
 */
export class MetaSidePanelInteraction extends Interaction {
    static selector = "#rj_meta_common_v2_root";

    dynamicContent = {};

    start() {
        let config = { enabled: false };
        const cfgEl = this.el.querySelector("#rj_meta_common_v2_config");
        if (cfgEl?.textContent) {
            try {
                config = JSON.parse(cfgEl.textContent);
            } catch (e) {
                console.warn("[Meta Common] invalid panel config", e);
                return;
            }
        }
        if (!config?.enabled) {
            return;
        }

        const mountEl = document.createElement("div");
        mountEl.className = "o_rj_meta_panel_mount";
        this.el.appendChild(mountEl);

        // Odoo 19 public Interaction API
        if (typeof this.mountComponent === "function") {
            try {
                this.mountComponent(mountEl, MetaSidePanel, { config });
                // Hide server-side FAB so only OWL panel is shown
                this.el.classList.add("o_rj_meta_owl_mounted");
                return;
            } catch (err) {
                console.warn("[Meta Common] mountComponent failed, keeping SSR button", err);
            }
        }
        // Keep SSR button (already in DOM); no need for second DOM fallback
    }

    /**
     * DOM fallback if OWL mount is unavailable.
     */
    _mountDomFallback(mountEl, config) {
        const posStyle = config.position === "left" ? "left:20px" : "right:20px";
        const screens = config.screens || [];
        const defaultUrl = config.defaultUrl || "https://business.facebook.com/";
        const hideMobile = config.showOnMobile === false ? "d-none d-md-block" : "";
        mountEl.innerHTML = `
            <div class="o_rj_meta_panel_fallback ${hideMobile}"
                 style="position:fixed;bottom:24px;${posStyle};z-index:1060;">
                <button type="button" class="btn btn-primary rounded-pill shadow o_rj_meta_fallback_btn"
                        style="background:#1877f2;border:0;font-weight:700;">
                    ${config.label || "Meta"}
                </button>
                <div class="o_rj_meta_fallback_menu d-none mt-2 p-2 rounded-3 shadow"
                     style="background:#0f1522;min-width:240px;max-width:90vw;">
                    ${
                        screens
                            .map(
                                (s) => `
                        <a class="d-block text-white text-decoration-none py-2 px-2 rounded"
                           style="font-size:13px;"
                           href="${s.url}" target="_blank" rel="noopener noreferrer">${s.title}</a>`
                            )
                            .join("") ||
                        `<a class="d-block text-white text-decoration-none py-2 px-2"
                           href="${defaultUrl}" target="_blank" rel="noopener">Business Suite</a>`
                    }
                </div>
            </div>`;
        const btn = mountEl.querySelector(".o_rj_meta_fallback_btn");
        const menu = mountEl.querySelector(".o_rj_meta_fallback_menu");
        btn?.addEventListener("click", () => {
            menu?.classList.toggle("d-none");
        });
    }
}

registry
    .category("public.interactions")
    .add("rj_meta_common_v2.meta_side_panel", MetaSidePanelInteraction);
