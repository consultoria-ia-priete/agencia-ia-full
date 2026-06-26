"""
_styles.py — CSS base + paletas de cor para os 3 variants (DARK/LIGHT/GREEN).
Centralizado pra evitar duplicação entre os tipos de slide.
"""

# Caminho relativo das fontes (resolve a partir do HTML em design/CXX-*/)
FONTS_PATH = "../_shared/fonts"

# Caminho relativo do avatar
AVATAR_PATH = "../_shared/alex-profile.jpg"

# Paleta por variante
PALETTE = {
    "DARK": {
        "bg": "#000000",
        "text": "#FFFFFF",
        "accent": "#8FDF65",
        "muted": "#A3A3A3",
        "dim": "#555",
        "handle": "#71767B",
        "avatar_border": "#8FDF65",
        "avatar_bg": "#1a1a1a",
        "verified_border": "#000",
    },
    "LIGHT": {
        "bg": "#FFFFFF",
        "text": "#000000",
        "accent": "#8FDF65",
        "muted": "#555",
        "dim": "#888",
        "handle": "#71767B",
        "avatar_border": "transparent",
        "avatar_bg": "#EEE",
        "verified_border": "#FFF",
    },
    "GREEN": {
        "bg": "#8FDF65",
        "text": "#000000",
        "accent": "#000000",
        "muted": "#1a1a1a",
        "dim": "#2a5f1a",
        "handle": "#2a5f1a",
        "avatar_border": "#000",
        "avatar_bg": "#7BC851",
        "verified_border": "#000",
    },
}


def base_css(variant: str) -> str:
    """CSS base compartilhado: fontes, layout, profile-badge, footer.
    Cada tipo de slide adiciona overrides específicos."""
    p = PALETTE[variant]
    avatar_border_decl = (
        f"border:2px solid {p['avatar_border']};" if variant == "DARK"
        else (f"border:3px solid {p['avatar_border']};" if variant == "GREEN"
              else "")
    )
    return f"""
@font-face{{font-family:'Poppins';font-weight:700;src:url('{FONTS_PATH}/poppins-700.woff2') format('woff2');font-display:block}}
@font-face{{font-family:'Poppins';font-weight:600;src:url('{FONTS_PATH}/poppins-600.woff2') format('woff2');font-display:block}}
@font-face{{font-family:'Inter';font-weight:400;src:url('{FONTS_PATH}/inter-400.woff2') format('woff2');font-display:block}}
@font-face{{font-family:'JetBrains Mono';font-weight:400;src:url('{FONTS_PATH}/jetbrains-400.woff2') format('woff2');font-display:block}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1440px;background:{p['bg']};overflow:hidden;font-family:'Inter',system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
.slide{{width:1080px;height:1440px;padding:0 80px;position:relative;display:flex;flex-direction:column;background:{p['bg']}}}
.badge-area{{padding-top:184px}}
.profile-badge{{display:flex;align-items:center;gap:24px}}
.profile-avatar-wrap{{position:relative;width:104px;height:104px;flex-shrink:0}}
.profile-avatar{{width:104px;height:104px;border-radius:50%;object-fit:cover;object-position:top center;display:block;background:{p['avatar_bg']};{avatar_border_decl}}}
.profile-text{{display:flex;flex-direction:column;gap:2px}}
.profile-name-row{{display:flex;align-items:center;gap:12px;font-family:'Poppins',sans-serif;font-weight:700;font-size:40px;color:{p['text']};letter-spacing:-0.5px;line-height:1.1}}
.verified-badge{{width:32px;height:32px;background:#1DA1F2;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;border:2px solid {p['verified_border']}}}
.profile-handle{{font-family:'Inter',sans-serif;font-weight:400;font-size:28px;color:{p['handle']};line-height:1.2}}
.hero{{flex:1;display:flex;flex-direction:column;justify-content:center;padding-right:20px}}
.eyebrow{{font-family:'Inter',sans-serif;font-weight:600;font-size:20px;color:{p['accent']};letter-spacing:4px;text-transform:uppercase;margin-bottom:36px;display:flex;align-items:center;gap:14px}}
.eyebrow::before{{content:'';width:36px;height:2px;background:{p['accent']}}}
.footer-area{{padding-bottom:184px;display:flex;justify-content:flex-end;align-items:flex-end}}
.slide-num{{font-family:'JetBrains Mono',monospace;font-size:18px;color:{p['dim']};letter-spacing:2px}}
"""


def profile_badge_html() -> str:
    """HTML do profile-badge (igual em todos os slides)."""
    return f"""<div class="badge-area"><div class="profile-badge"><div class="profile-avatar-wrap"><img class="profile-avatar" src="{AVATAR_PATH}"></div><div class="profile-text"><div class="profile-name-row">Alex Priete<span class="verified-badge"><svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg></span></div><div class="profile-handle">@alexpriete</div></div></div></div>"""


def footer_html(slide_num: int) -> str:
    return f'<div class="footer-area"><div class="slide-num">{slide_num:02d} / 08</div></div>'


def render_inline_tags(text: str, variant: str) -> str:
    """Substitui as tags <verde>, <highlight>, <black>, <black-block>, <black-highlight>, <strike>
    pelo HTML correto dependendo da variante."""
    if not text:
        return text

    if variant == "DARK":
        text = text.replace("<verde>", '<span style="color:#8FDF65">').replace("</verde>", "</span>")
        text = text.replace("<highlight>", '<span style="color:#8FDF65">').replace("</highlight>", "</span>")
        text = text.replace("<black>", '<span style="color:#FFF">').replace("</black>", "</span>")
        text = text.replace("<black-block>", '<span style="color:#8FDF65">').replace("</black-block>", "</span>")
        text = text.replace("<black-highlight>", '<span style="color:#8FDF65">').replace("</black-highlight>", "</span>")
        text = text.replace("<strike>", '<span style="text-decoration:line-through;text-decoration-thickness:4px;color:#555">').replace("</strike>", "</span>")
    elif variant == "LIGHT":
        text = text.replace("<verde>", '<span style="background:#8FDF65;padding:0 14px;display:inline-block">').replace("</verde>", "</span>")
        text = text.replace("<highlight>", '<span style="background:#8FDF65;padding:0 14px;display:inline-block">').replace("</highlight>", "</span>")
        text = text.replace("<black>", '<span style="background:#000;color:#FFF;padding:0 14px;display:inline-block">').replace("</black>", "</span>")
        text = text.replace("<black-block>", '<span style="background:#000;color:#8FDF65;padding:0 14px;display:inline-block">').replace("</black-block>", "</span>")
        text = text.replace("<black-highlight>", '<span style="background:#000;color:#8FDF65;padding:0 14px;display:inline-block">').replace("</black-highlight>", "</span>")
        text = text.replace("<strike>", '<span style="text-decoration:line-through;text-decoration-thickness:4px;color:#CCC">').replace("</strike>", "</span>")
    elif variant == "GREEN":
        text = text.replace("<verde>", '<span style="background:#000;color:#8FDF65;padding:0 14px;display:inline-block">').replace("</verde>", "</span>")
        text = text.replace("<highlight>", '<span style="background:#000;color:#8FDF65;padding:0 14px;display:inline-block">').replace("</highlight>", "</span>")
        text = text.replace("<black>", '<span style="background:#000;color:#FFF;padding:0 14px;display:inline-block">').replace("</black>", "</span>")
        text = text.replace("<black-block>", '<span style="background:#000;color:#8FDF65;padding:0 14px;display:inline-block">').replace("</black-block>", "</span>")
        text = text.replace("<black-highlight>", '<span style="background:#000;color:#8FDF65;padding:0 14px;display:inline-block">').replace("</black-highlight>", "</span>")
        text = text.replace("<strike>", '<span style="text-decoration:line-through;text-decoration-thickness:4px;color:#4a4a4a">').replace("</strike>", "</span>")

    return text
