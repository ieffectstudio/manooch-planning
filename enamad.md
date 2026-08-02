The problem is likely not with your content, but with your **Server Configuration (HTTPS/SSL)** or your **Caddy configuration syntax**.

Based on your provided output, there are 3 specific reasons why the Enamad (اینماد) bot is failing to see your file:

### 1. The SSL/HTTPS Certificate Issue (Most Likely)
Enamad's verification bot is notorious for failing if your SSL certificate is not "Perfect."
*   If your site is using a **Self-Signed certificate**, Enamad will fail.
*   If your **SSL Chain is incomplete**, Enamad will fail.
*   **Test:** Go to [SSL Labs](https://www.ssllabs.com/ssltest/) and enter `manooch.site`. If you get anything less than an **A grade**, the Enamad bot might block the connection.

### 2. Caddy Configuration Syntax
You provided this snippet:
```caddy
header Content-Type "text/plain; charset=utf-8"
respond "۳۹۳۲۱۳۵۳" 200
```
**The Problem:** You are using Persian digits `۳۹۳۲۱۳۵۳`. Enamad usually expects standard English digits `39321353` unless specifically stated otherwise. Furthermore, ensure this block is inside the correct site block in your `Caddyfile`.

**Try this exact block in your Caddyfile:**
```caddy
manooch.site {
    # Ensure this is at the top of your site block
    handle /39321353.txt {
        header Content-Type "text/plain; charset=utf-8"
        respond "39321353" 200
    }

    # ... your other config (reverse_proxy, etc)
}
```

### 3. DNS and IPv6 (AAAA Record)
If your domain has an **IPv6 (AAAA record)** set in your DNS (like Cloudflare or ArvanCloud) but your server is not correctly configured to handle IPv6, the Enamad bot (which often uses IPv6) will hit a wall.
*   **Solution:** Check your DNS panel. If you see an `AAAA` record, try deleting it temporarily and leave only the `A` record (IPv4).

### 4. Cloudflare / Firewall Blocking
If you are using **Cloudflare**, **ArvanCloud**, or a **WAF**:
*   The Enamad bot is often flagged as a "Crawler" or "Bot."
*   Go to your Firewall logs. Look for blocked requests to `/39321353.txt`.
*   **Try this:** Temporarily "Pause" Cloudflare (Development Mode) and try the Enamad verification again.

### How to verify it yourself before clicking the button:
Open your phone (using mobile data, not Wi-Fi) and go to:
`https://manooch.site/39321353.txt`

1.  Does it load instantly?
2.  Does the browser show a "Not Secure" warning? (If yes, Enamad will fail).
3.  Does it download a file or show the text? (It should show the text).

**Recommendation:** Change the Persian numbers `۳۹۳۲۱۳۵۳` to English `39321353` in your `respond` command and restart Caddy (`caddy reload`). Enamad's system is very old and often doesn't recognize UTF-8 Persian digits in the verification string.