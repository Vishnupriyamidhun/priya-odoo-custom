/** @odoo-module **/

const MARKDOWN_LINK_RE = /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g;
const PLAIN_URL_RE = /(https?:\/\/[^\s<]+)/g;

function buildFragmentFromText(text) {
    const frag = document.createDocumentFragment();
    let lastIndex = 0;
    let match;
    let hasMarkdown = false;

    // 1. Check for Markdown links [Text](URL)
    MARKDOWN_LINK_RE.lastIndex = 0;
    while ((match = MARKDOWN_LINK_RE.exec(text))) {
        hasMarkdown = true;
        const [full, label, url] = match;
        if (match.index > lastIndex) {
            frag.appendChild(document.createTextNode(text.slice(lastIndex, match.index)));
        }
        const a = document.createElement("a");
        a.href = url;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        a.textContent = label;
        frag.appendChild(a);
        lastIndex = match.index + full.length;
    }
    if (hasMarkdown) {
        if (lastIndex < text.length) {
            frag.appendChild(document.createTextNode(text.slice(lastIndex)));
        }
        return frag;
    }

    // 2. Check for Plain URLs (https://...)
    lastIndex = 0;
    let hasUrl = false;
    PLAIN_URL_RE.lastIndex = 0;
    while ((match = PLAIN_URL_RE.exec(text))) {
        hasUrl = true;
        const url = match[0];
        if (match.index > lastIndex) {
            frag.appendChild(document.createTextNode(text.slice(lastIndex, match.index)));
        }
        const a = document.createElement("a");
        a.href = url;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        a.textContent = url;
        frag.appendChild(a);
        lastIndex = match.index + url.length;
    }

    if (hasUrl) {
        if (lastIndex < text.length) {
            frag.appendChild(document.createTextNode(text.slice(lastIndex)));
        }
        return frag;
    }

    // 3. Google Maps link generation for plain text locations (e.g. "Kochi")
    if (text.trim().length > 0) {
        const a = document.createElement("a");
        a.href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(text.trim())}`;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        a.textContent = text;
        frag.appendChild(a);
        return frag;
    }

    return null;
}

function linkifyContainer(root) {
    if (!root || root.dataset?.locationLinkified === "1") {
        return;
    }
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
        acceptNode(node) {
            if (!node.nodeValue || !node.nodeValue.trim()) {
                return NodeFilter.FILTER_REJECT;
            }
            if (node.parentElement && node.parentElement.closest("a, script, style")) {
                return NodeFilter.FILTER_REJECT;
            }
            return NodeFilter.FILTER_ACCEPT;
        },
    });

    const textNodes = [];
    let node;
    while ((node = walker.nextNode())) {
        textNodes.push(node);
    }

    for (const textNode of textNodes) {
        const frag = buildFragmentFromText(textNode.nodeValue);
        if (frag && textNode.parentNode) {
            textNode.parentNode.replaceChild(frag, textNode);
        }
    }

    if (root.dataset) {
        root.dataset.locationLinkified = "1";
    }
}

function scanNode(node) {
    if (node.nodeType !== 1) {
        return;
    }
    if (node.matches && node.matches(".o_cw_popover")) {
        linkifyContainer(node);
    }
    if (node.querySelectorAll) {
        node.querySelectorAll(".o_cw_popover").forEach(linkifyContainer);
    }
}

function startObserving() {
    const observer = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
            mutation.addedNodes.forEach(scanNode);
            if (mutation.target) {
                const popover = mutation.target.closest && mutation.target.closest(".o_cw_popover");
                if (popover) {
                    delete popover.dataset.locationLinkified;
                    linkifyContainer(popover);
                }
            }
        }
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true,
        characterData: true,
    });

    document.querySelectorAll(".o_cw_popover").forEach(linkifyContainer);
}

if (document.body) {
    startObserving();
} else {
    document.addEventListener("DOMContentLoaded", startObserving);
}