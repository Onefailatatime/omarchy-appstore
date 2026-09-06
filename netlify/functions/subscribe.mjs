import checklist from "./checklist.mjs";

// Newsletter signup: adds the address to the Resend audience and emails the
// packaging checklist as an attachment. Resend is called over plain fetch so
// the function carries no SDK.
const RESEND = "https://api.resend.com";
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const jsonHeaders = {
  "cache-control": "no-store",
  "content-type": "application/json; charset=utf-8",
  "referrer-policy": "same-origin",
  "x-content-type-options": "nosniff",
};

function response(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: jsonHeaders });
}

function welcome(siteUrl) {
  return [
    "Thanks for joining the Unofficial Omarchy App Store newsletter.",
    "",
    "Your copy of the Develop for Omarchy packaging checklist is attached as",
    "Markdown. Drop it into an LLM project, knowledge base, or skill, or just",
    "work through it before you open a pull request to omarchy-pkgs.",
    "",
    `Read it online any time: ${siteUrl}/develop.html`,
    "",
    "You'll hear from me when notable apps land in the Omarchy repo. Reply to",
    "this email with \"unsubscribe\" at any time and I'll remove you.",
    "",
    "Jessyka",
    siteUrl,
  ].join("\n");
}

async function resend(fetchImpl, key, method, path, body) {
  const res = await fetchImpl(RESEND + path, {
    method,
    headers: { authorization: `Bearer ${key}`, "content-type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  return { ok: res.ok, status: res.status, data: await res.json().catch(() => ({})) };
}

export async function handleSubscribeRequest(request, env, fetchImpl = fetch) {
  if (request.method !== "POST") return response({ error: "Method not allowed" }, 405);

  const url = new URL(request.url);
  const origin = request.headers.get("origin");
  if (origin && origin !== url.origin) return response({ error: "Cross-site signup is not allowed" }, 403);

  let body;
  try {
    body = await request.json();
  } catch {
    return response({ error: "Invalid JSON" }, 400);
  }
  // Honeypot: real visitors never fill "website".
  if (body.website) return response({ status: "subscribed" });

  const email = typeof body.email === "string" ? body.email.trim().toLowerCase() : "";
  if (!EMAIL.test(email) || email.length > 254) return response({ error: "Enter a valid email address" }, 400);

  const key = env.RESEND_API_KEY;
  const audience = env.RESEND_AUDIENCE_ID;
  const from = env.NEWSLETTER_FROM;
  if (!key || !audience || !from) return response({ error: "Newsletter signup is not configured yet" }, 500);

  const existing = await resend(fetchImpl, key, "GET", `/audiences/${audience}/contacts/${encodeURIComponent(email)}`);
  if (existing.ok && existing.data.unsubscribed === false) return response({ status: "existing" });

  const contact = await resend(fetchImpl, key, "POST", `/audiences/${audience}/contacts`, { email, unsubscribed: false });
  if (!contact.ok) {
    console.error("resend contact failed", contact.status, contact.data);
    return response({ error: "Could not save your signup. Please try again." }, 502);
  }

  const siteUrl = url.origin;
  const sent = await resend(fetchImpl, key, "POST", "/emails", {
    from,
    to: [email],
    reply_to: env.NEWSLETTER_REPLY_TO || from,
    subject: "Your Develop for Omarchy checklist",
    text: welcome(siteUrl),
    attachments: [{ filename: "develop-for-omarchy.md", content: Buffer.from(checklist, "utf8").toString("base64") }],
  });
  if (!sent.ok) {
    console.error("resend email failed", sent.status, sent.data);
    return response({ error: "You're subscribed, but the checklist email failed to send. Please try again later." }, 502);
  }
  return response({ status: "subscribed" });
}

export default async function subscribe(request) {
  try {
    return await handleSubscribeRequest(request, process.env);
  } catch (error) {
    console.error("subscribe function failed", error);
    return response({ error: "Signup is temporarily unavailable" }, 500);
  }
}

export const config = {
  path: "/api/subscribe",
  rateLimit: {
    windowLimit: 5,
    windowSize: 60,
    aggregateBy: ["ip", "domain"],
  },
};
