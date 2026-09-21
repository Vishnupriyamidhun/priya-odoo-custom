/** @odoo-module **/

const MARKDOWN_LINK_RE = /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g;
const PLAIN_URL_RE = /(https?:\/\/[^\s<]+)/g;

// Selector(s) used to identify the LOCATION row inside the popover.
// Odoo's calendar popover renders the location next to a "fa-map-marker" icon.
// If your Odoo version uses a different markup, inspect the popover in
// devtools and adjust this selector accordingly.
const LOCATION_ICON_SELECTOR = ".fa-map-marker, .fa-map-marker-alt";

// Words that should NEVER be treated as a real location, even though they
// are plain text typed into the Location field (test input, greetings, etc).
// Add more words here as needed - matching is case-insensitive and only
// applies when the ENTIRE location text equals one of these words.
const NON_LOCATION_WORDS = new Set([
    "yes", "no", "hi", "hii", "hello", "hey", "ok", "okay",
    "test", "testing", "name", "sample", "demo", "none", "na", "n/a",
    "asdf", "abc", "xyz", "lorem", "ipsum", "dummy", "x", "xx", "xxx",
]);

// Minimum length for plain text to be considered a possible location.
const MIN_LOCATION_LENGTH = 2;

function looksLikeLocation(text) {
    const trimmed = text.trim();
    if (trimmed.length < MIN_LOCATION_LENGTH) {
        return false;
    }
    if (NON_LOCATION_WORDS.has(trimmed.toLowerCase())) {
        return false;
    }
    return true;
}

function buildFragmentFromText(text, isLocationField) {
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

    // 3. Plain text -> Google Maps link.
    // IMPORTANT: only do this when we are inside the location field, AND
    // the text passes a basic sanity check (not a greeting/test word like
    // "yes", "hi", "name" etc).
    if (isLocationField && looksLikeLocation(text)) {
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

// Returns true if `el` is a field icon (Odoo marks every popover field -
// date, time, location, attendees, organizer - with a FontAwesome icon,
// e.g. class="fa fa-calendar", "fa fa-clock-o", "fa fa-map-marker", etc).
function isFieldIcon(el) {
    return !!(el && el.tagName === "I" && /(^|\s)fa-/.test(el.className || ""));
}

// Collects only the text nodes that sit between the location icon and the
// NEXT field icon in document order. This does not depend on the popover's
// row/wrapper markup at all - it works whether each field is wrapped in its
// own <div> or all fields share one parent container.
function collectLocationTextNodes(icon, root) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_ALL);
    walker.currentNode = icon;
    const nodes = [];
    let node;
    while ((node = walker.nextNode())) {
        if (node.nodeType === 1 && isFieldIcon(node)) {
            break; // reached the next field's icon - stop collecting
        }
        if (node.nodeType === 3 && node.nodeValue && node.nodeValue.trim()) {
            if (!(node.parentElement && node.parentElement.closest("a, script, style"))) {
                nodes.push(node);
            }
        }
    }
    return nodes;
}

function linkifyContainer(root) {
    if (!root || root.dataset?.locationLinkified === "1") {
        return;
    }

    // Only process text that sits between the location icon and the next
    // field icon - never the whole row/container - so date, time,
    // attendees, and organizer are never touched.
    const icons = root.querySelectorAll(LOCATION_ICON_SELECTOR);
    icons.forEach((icon) => {
        const textNodes = collectLocationTextNodes(icon, root);
        for (const textNode of textNodes) {
            const frag = buildFragmentFromText(textNode.nodeValue, /* isLocationField */ true);
            if (frag && textNode.parentNode) {
                textNode.parentNode.replaceChild(frag, textNode);
            }
        }
    });

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
