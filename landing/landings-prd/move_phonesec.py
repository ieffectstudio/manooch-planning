# -*- coding: utf-8 -*-
h = open('menuch-landing.html', encoding='utf-8').read()

# ============================================================
# 1) Move phonesec section up — right after the hero section
# ============================================================
ps_start = h.find('<section class="mn-phonesec mn-section" id="app">')
ps_end = h.find('</section>', ps_start) + len('</section>')
assert ps_start != -1 and ps_end > ps_start
sec_html = h[ps_start:ps_end]

# remove from current position
h = h[:ps_start] + h[ps_end:]

# insert right after hero
hero_start = h.find('<section class="mn-hero">')
hero_end = h.find('</section>', hero_start) + len('</section>')
assert hero_start != -1 and hero_end > hero_start
h = h[:hero_end] + '\n\n' + sec_html + h[hero_end:]
print("moved phonesec after hero")

# ============================================================
# 2) Compact the title/sub/cta
# ============================================================
h = h.replace(
    ".mn-phonesec__tag {\n  display: inline-block; background: var(--lav); color: var(--brand);\n  font-size: 14px; font-weight: 500; padding: 8px 16px; border-radius: 999px;\n}",
    ".mn-phonesec__tag {\n  display: inline-block; background: var(--lav); color: var(--brand);\n  font-size: 13px; font-weight: 400; padding: 6px 14px; border-radius: 999px;\n}")
h = h.replace(
    ".mn-phonesec__title { font-size: clamp(26px, 3vw, 40px); font-weight: 600; color: var(--ink); margin-top: 16px; line-height: 1.35; }",
    ".mn-phonesec__title { font-size: clamp(22px, 2.4vw, 32px); font-weight: 600; color: var(--ink); margin-top: 12px; line-height: 1.35; }")
h = h.replace(
    ".mn-phonesec__sub { font-size: clamp(14px, 1.15vw, 17px); line-height: 1.95; color: var(--body); margin-top: 14px; max-width: 54ch; }",
    ".mn-phonesec__sub { font-size: clamp(13px, 1vw, 15px); line-height: 1.8; color: var(--body); margin-top: 10px; max-width: 52ch; }")
h = h.replace(
    ".mn-phonesec__cta { margin-top: 28px; height: 56px; width: max-content; }",
    ".mn-phonesec__cta { margin-top: 18px; height: 52px; width: max-content; }")

# ============================================================
# 3) Steps -> compact feature tiles (2-col grid, smaller)
# ============================================================
old_steps_css = """.mn-phonesec__grid { align-items: stretch; }
.mn-phonesec__stage { align-self: stretch; }
/* در دسکتاپ خود گوشی sticky است */
.mn-phone { position: -webkit-sticky; position: sticky; top: 110px; margin-inline: auto; }
.mn-phonesec__steps { list-style: none; margin-top: 28px; display: flex; flex-direction: column; gap: 22px; }
.mn-phonestep {
  display: flex; gap: 16px; align-items: flex-start;
  background: #fff; border: 1px solid var(--line); border-radius: 18px;
  padding: 26px 24px; min-height: 158px; align-items: center;
  transition: border-color .2s ease, box-shadow .2s ease, transform .2s ease;
}
.mn-phonestep:hover { border-color: rgba(75,69,230,.5); box-shadow: 0 14px 32px rgba(75,69,230,.1); transform: translateX(-4px); }
.mn-phonestep__num {
  width: 46px; height: 46px; flex: none; border-radius: 14px;
  color: #fff; display: grid; place-items: center;
  font-size: 18px; font-weight: 600; line-height: 1;
  box-shadow: 0 8px 18px rgba(32,42,55,.2);
}
.mn-phonestep h3 { font-size: 18px; font-weight: 500; color: var(--ink); }
.mn-phonestep p { font-size: 14.5px; line-height: 1.85; color: var(--body); margin-top: 6px; max-width: 46ch; }
.mn-phonesec__steps { gap: 26px; }"""
new_steps_css = """.mn-phonesec__grid { align-items: center; }
.mn-phonesec__stage { align-self: center; }
/* در دسکتاپ خود گوشی sticky است */
.mn-phone { position: -webkit-sticky; position: sticky; top: 110px; margin-inline: auto; }
.mn-phonesec__steps {
  list-style: none; margin-top: 20px;
  display: grid; grid-template-columns: 1fr 1fr; gap: 12px;
}
.mn-phonestep {
  display: flex; gap: 10px; align-items: flex-start;
  background: #fff; border: 1px solid var(--line); border-radius: 14px;
  padding: 14px; min-height: 0;
  transition: border-color .2s ease, box-shadow .2s ease, transform .2s ease;
}
.mn-phonestep:hover { border-color: rgba(75,69,230,.5); box-shadow: 0 10px 24px rgba(75,69,230,.1); transform: translateY(-2px); }
.mn-phonestep__num {
  width: 30px; height: 30px; flex: none; border-radius: 9px;
  color: #fff; display: grid; place-items: center;
  font-size: 13px; font-weight: 600; line-height: 1;
  box-shadow: 0 4px 10px rgba(32,42,55,.18);
}
.mn-phonestep h3 { font-size: 14.5px; font-weight: 500; color: var(--ink); line-height: 1.45; }
.mn-phonestep p { font-size: 12.5px; line-height: 1.7; color: var(--body); margin-top: 4px; }
.mn-phonestep:last-child { grid-column: 1 / -1; }
@media (max-width: 560px) {
  .mn-phonesec__steps { grid-template-columns: 1fr; }
  .mn-phonestep:last-child { grid-column: auto; }
}"""
assert h.count(old_steps_css) == 1, f"steps css found {h.count(old_steps_css)}"
h = h.replace(old_steps_css, new_steps_css)

# ============================================================
# 4) Shorten sub text (more compact)
# ============================================================
old_sub = "از لحظه‌ی سفارش تا تحویل — همه‌چیز تو گوشت اتفاق میفته. اسکرول بده تا مراحل واقعی فروش با منوچ را ببینی؛ موکاپ جلویت ثابت می‌ماند."
new_sub = "از لحظه‌ی سفارش تا تحویل — همه‌چیز تو گوشت اتفاق میفته."
assert h.count(old_sub) == 1
h = h.replace(old_sub, new_sub)

open('menuch-landing.html', 'w', encoding='utf-8').write(h)
print("done. new length:", len(h))

# sanity: order of sections
import re
order = re.findall(r'<section class="(mn-[a-z]+)', h)
print("section order:", order)
