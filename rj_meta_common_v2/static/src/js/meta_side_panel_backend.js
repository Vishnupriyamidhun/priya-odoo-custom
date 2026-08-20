/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { MetaSidePanel } from "@rj_meta_common_v2/js/meta_side_panel_core";

export class MetaSidePanelBackend extends Component {
    static template = "rj_meta_common_v2.MetaSidePanelBackend";
    static components = { MetaSidePanel };

    setup() {
        this.orm = useService("orm");
        this.config = { enabled: false };

        onWillStart(async () => {
            try {
                this.config = await this.orm.call("website", "get_backend_meta_panel_config", []);
            } catch (e) {
                console.warn("[Meta Common] Could not fetch backend panel config", e);
            }
        });
    }
}

registry.category("main_components").add("rj_meta_common_v2.meta_side_panel_backend", {
    Component: MetaSidePanelBackend,
});

