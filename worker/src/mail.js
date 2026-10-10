// Bidder email through Resend, the same provider the newsletter uses. Nothing
// sends until RESEND_API_KEY and MAIL_FROM are set; without them the auction
// runs in review mode and Jessyka approves bids by hand.

import { money } from "./auction.js";

export function mailConfigured(env) {
  return Boolean(env.RESEND_API_KEY && env.MAIL_FROM);
}

export async function sendMail(env, message, fetchImpl = fetch) {
  if (!mailConfigured(env)) return { ok: false, skipped: true };
  const res = await fetchImpl("https://api.resend.com/emails", {
    method: "POST",
    headers: { authorization: `Bearer ${env.RESEND_API_KEY}`, "content-type": "application/json" },
    body: JSON.stringify({ from: env.MAIL_FROM, reply_to: env.MAIL_REPLY_TO || env.MAIL_FROM, ...message }),
  });
  if (!res.ok) console.error(JSON.stringify({ event: "mail_failed", status: res.status, subject: message.subject }));
  return { ok: res.ok, status: res.status };
}

function when(iso) {
  return new Date(iso).toUTCString().replace(":00 GMT", " UTC");
}

function amountLine(cfg, amount) {
  return money(amount) + (cfg.perMonth ? " per month" : "");
}

export function verifyEmail({ siteUrl, link, cfg, amount, name, to }) {
  return {
    to: [to],
    subject: `Confirm your bid on the ${cfg.label.toLowerCase()} slot`,
    text: [
      `Thanks for bidding on the ${cfg.label.toLowerCase()} slot at omarchyapps.com.`,
      "",
      `Your bid: ${amountLine(cfg, amount)}`,
      `Product: ${name}`,
      "",
      "Confirm it here so it counts:",
      link,
      "",
      "The link works once and belongs to this bid only. If you did not place it, ignore this email and nothing happens.",
      "",
      "Jessyka",
      `${siteUrl}/advertise.html`,
    ].join("\n"),
  };
}

export function outbidEmail({ siteUrl, cfg, bid, minimum, closesAt }) {
  return {
    to: [bid.email],
    subject: `You have been outbid on the ${cfg.label.toLowerCase()} slot`,
    text: [
      `Someone bid above you on the ${cfg.label.toLowerCase()} slot at omarchyapps.com.`,
      "",
      `Your bid: ${amountLine(cfg, bid.amount)}`,
      `The bid to beat is now: ${amountLine(cfg, minimum)}`,
      closesAt ? `Bidding closes ${when(closesAt)} unless a late bid extends it.` : "",
      "",
      `Bid again here: ${siteUrl}/advertise.html#${cfg.id}`,
      "",
      "You owe nothing for a bid that does not win.",
      "",
      "Jessyka",
    ].join("\n"),
  };
}

export function wonEmail({ siteUrl, cfg, bid, charge }) {
  const term = cfg.perMonth ? `the first ${cfg.termDays} day term` : "one payment, and the slot never expires";
  return {
    to: [bid.email],
    subject: `You won the ${cfg.label.toLowerCase()} slot on Omarchy Apps`,
    text: [
      `Your bid of ${amountLine(cfg, bid.amount)} won the ${cfg.label.toLowerCase()} slot at omarchyapps.com.`,
      "",
      "What happens next:",
      `1. You get an invoice by email for ${money(charge)}, ${term}.`,
      `2. Once it is paid, your ad goes live in that slot: "${bid.name}", linking to ${bid.url}.`,
      "3. Change the link, text, or image any time by replying to this email.",
      "",
      "Reply to this email with any question.",
      "",
      "Jessyka",
      `${siteUrl}/advertise.html`,
    ].join("\n"),
  };
}
