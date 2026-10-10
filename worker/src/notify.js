// Admin heads-up over Telegram, the channel every other project here uses.
// Optional: set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID as Worker secrets.

export async function notifyAdmin(env, text, fetchImpl = fetch) {
  if (!env.TELEGRAM_BOT_TOKEN || !env.TELEGRAM_CHAT_ID) return { ok: false, skipped: true };
  try {
    const res = await fetchImpl(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ chat_id: env.TELEGRAM_CHAT_ID, text, disable_web_page_preview: true }),
    });
    if (!res.ok) console.error(JSON.stringify({ event: "telegram_failed", status: res.status }));
    return { ok: res.ok };
  } catch (error) {
    console.error(JSON.stringify({ event: "telegram_failed", error: String(error) }));
    return { ok: false };
  }
}
