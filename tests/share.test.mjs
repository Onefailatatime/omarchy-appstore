import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import vm from "node:vm";

let clickHandler;
let shared;
let copied;

globalThis.window = {
  isSecureContext: true,
  location: { href: "https://omarchyapps.com/" },
  setTimeout() {},
  prompt() { throw new Error("prompt fallback should not be needed"); },
};
globalThis.document = {
  baseURI: "https://omarchyapps.com/",
  addEventListener(type, handler, capture) {
    assert.equal(type, "click");
    assert.equal(capture, true);
    clickHandler = handler;
  },
};
Object.defineProperty(globalThis, "navigator", {
  configurable: true,
  value: {
    share: async (payload) => { shared = payload; },
    clipboard: { writeText: async (value) => { copied = value; } },
  },
});

vm.runInThisContext(await readFile(new URL("../assets/share.js", import.meta.url), "utf8"));

const trigger = {
  dataset: {
    shareApp: "slap-notes-bin",
    shareTitle: "slap-notes-bin for Omarchy",
    shareUrl: "https://omarchyapps.com/apps/slap-notes-bin.html",
  },
  textContent: "Share",
};
const event = {
  target: { closest: () => trigger },
  preventDefault() {},
  stopPropagation() {},
};

clickHandler(event);
await new Promise((resolve) => setImmediate(resolve));
assert.equal(shared.url, "https://omarchyapps.com/apps/slap-notes-bin.html");
assert.equal(shared.title, "slap-notes-bin for Omarchy");

delete navigator.share;
clickHandler(event);
await new Promise((resolve) => setImmediate(resolve));
await new Promise((resolve) => setImmediate(resolve));
assert.equal(copied, "https://omarchyapps.com/apps/slap-notes-bin.html");
assert.equal(trigger.textContent, "Copied!");

console.log("share-tests-ok");
