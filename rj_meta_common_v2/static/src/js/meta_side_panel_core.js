/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

/**
 * OWL Meta side panel — floating console launcher for Meta Business screens.
 * Core component shared between frontend (Interaction) and backend (MainComponent).
 */
export class MetaSidePanel extends Component {
    static template = "rj_meta_common_v2.MetaSidePanel";
    static props = {
        config: { type: Object },
    };

    setup() {
        this.config = this.props.config || { enabled: false, screens: [] };
        const screens = this.config.screens || [];
        const defaultKey = this.config.defaultScreen || screens[0]?.key || "business";
        const active =
            screens.find((s) => s.key === defaultKey) ||
            screens[0] || {
                key: "business",
                title: "Business Suite",
                url: this.config.defaultUrl || "https://business.facebook.com/",
            };
        this.state = useState({
            open: false,
            activeKey: active.key,
            activeUrl: active.url,
            activeTitle: active.title,
        });
    }

    get rootClass() {
        const pos = this.config.position === "left" ? "pos-left" : "pos-right";
        const mobile = this.config.showOnMobile === false ? "hide-mobile" : "";
        return `${pos} ${mobile}`.trim();
    }

    get drawerClass() {
        return "";
    }

    get showEmbed() {
        return this.config.openMode === "embed";
    }

    togglePanel() {
        if (this.config.openMode === "new_tab") {
            window.open(this.state.activeUrl, "_blank", "noopener,noreferrer");
            return;
        }
        this.state.open = !this.state.open;
    }

    closePanel() {
        this.state.open = false;
    }

    selectScreen(screen) {
        this.state.activeKey = screen.key;
        this.state.activeUrl = screen.url;
        this.state.activeTitle = screen.title;
        if (this.config.openMode === "new_tab") {
            window.open(screen.url, "_blank", "noopener,noreferrer");
        }
    }
}
