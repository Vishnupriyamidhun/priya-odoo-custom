/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { standardActionServiceProps } from "@web/webclient/actions/action_service";

/**
 * Customer-facing Meta suite / module dashboard with action cards.
 * Suite mode: one card per installed app with all actions visible.
 * Module mode: detail cards (all actions, config, logs, records, tools) + recent logs.
 */
export class MetaDashboard extends Component {
    static template = "rj_meta_common_v2.MetaDashboard";
    static props = { ...standardActionServiceProps };

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");

        const params = this.props.action?.params || {};
        const ctx = this.props.action?.context || {};
        this.mode = params.mode || ctx.meta_dash_mode || "suite";
        this.moduleTech = params.module_tech || ctx.module_tech || false;

        this.state = useState({
            loading: true,
            title: "Meta Dashboard",
            subtitle: "",
            kpis: [],
            cards: [],
            recent_logs: [],
            mode: this.mode,
        });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        this.state.loading = true;
        try {
            const data = await this.orm.call("meta.common.dashboard", "get_dashboard_data", [], {
                mode: this.mode,
                module_tech: this.moduleTech || null,
            });
            this.state.title = data.title || "Meta Dashboard";
            this.state.subtitle = data.subtitle || "";
            this.state.kpis = data.kpis || [];
            this.state.cards = data.cards || [];
            this.state.recent_logs = data.recent_logs || [];
            this.state.mode = data.mode || this.mode;
        } catch (e) {
            console.error(e);
            this.notification.add("Could not load Meta dashboard.", { type: "danger" });
        } finally {
            this.state.loading = false;
        }
    }

    async onAction(act) {
        if (!act) {
            return;
        }
        try {
            if (act.type === "object" && act.method) {
                const result = await this.orm.call(
                    "meta.common.dashboard",
                    act.method,
                    [],
                    act.params || {}
                );
                if (result) {
                    await this.action.doAction(result);
                }
                return;
            }
            if (act.type === "action" && act.tag) {
                await this.action.doAction({
                    type: "ir.actions.client",
                    tag: act.tag,
                    params: act.params || {},
                });
            }
        } catch (e) {
            console.error(e);
            this.notification.add(e.message || "Action failed", { type: "danger" });
        }
    }

    async openLog(log) {
        if (!log || !log.model || !log.id) {
            return;
        }
        try {
            const result = await this.orm.call(
                "meta.common.dashboard",
                "action_open_log_record",
                [],
                { model: log.model, res_id: log.id }
            );
            if (result) {
                await this.action.doAction(result);
            }
        } catch (e) {
            console.error(e);
            this.notification.add(e.message || "Could not open log", { type: "danger" });
        }
    }

    async openSuite() {
        await this.action.doAction({
            type: "ir.actions.client",
            tag: "rj_meta_common_v2_dashboard",
            name: "Meta Marketing Suite",
            params: { mode: "suite" },
        });
    }

    logStateClass(state) {
        if (state === "success") {
            return "o_rj_meta_log_ok";
        }
        if (state === "error") {
            return "o_rj_meta_log_err";
        }
        return "o_rj_meta_log_pending";
    }
}

registry.category("actions").add("rj_meta_common_v2_dashboard", MetaDashboard);
