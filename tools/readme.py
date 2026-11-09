"""Writes README.md from tools/profile.py, using the graphics in assets/."""

import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import profile as P  # noqa: E402

BASE = 'https://raw.githubusercontent.com/kkorel/kkorel/main/assets'


def pic(name, alt, width=None):
    w = f' width="{width}"' if width else ''
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{BASE}/{name}-dark.svg">'
            f'<img src="{BASE}/{name}-light.svg" alt="{html.escape(alt, quote=True)}"{w}></picture>')


def link(href, inner):
    return f'<a href="{html.escape(href, quote=True)}">{inner}</a>' if href else inner


def build():
    def card(k):
        d = P.PROJECTS[k]
        return link(d.get('url'), pic(f'card-{k}', f'{d["title"]}: {d["text"]}', '49%'))

    keys = list(P.PROJECTS)
    tagline = ' '.join(P.TAGLINE.split())
    contacts = (f'{P.NAME}. ' + (f'{tagline} ' if tagline else '') + ' · '.join(P.KICKER.split('  ·  '))
                + f'. LinkedIn: {P.CONTACTS[0][1]}. Email: {P.EMAIL}.')
    parts = [
        pic('hero', contacts),
        f'<p><a href="{P.LINKEDIN}">LinkedIn</a> &nbsp;·&nbsp; <a href="mailto:{P.EMAIL}">{P.EMAIL}</a></p>',
        pic('highlights', 'Highlights: ' + '; '.join(f'{x[1]}, {x[2]}' for x in P.HIGHLIGHTS)),
        pic('now', 'Now: ' + '; '.join(x[1] for x in P.NOW_ITEMS)),
        pic('timeline', 'Experience: ' + '; '.join(f'{r[2]} at {r[1]}' for r in P.EXPERIENCE)),
        pic('impact', P.IMPACT['title'].title() + ': ' + '; '.join(' '.join(x) for x in P.IMPACT['stats'])),
    ]
    if getattr(P, 'YEAR_PERIODS', None):
        import datetime as dt
        first = dt.date(*P.YEAR_START)
        parts.append(pic('year', f'Work since {first:%B %Y}, real commits plus estimated private work. ' + '. '.join(
            f'{lane}: ' + ', '.join(item[2] for item in items) for lane, items in P.YEAR_TRACKS)))
    parts.append(pic('label-work', 'Selected work'))
    for a, b in zip(keys[0::2], keys[1::2]):
        parts.append('<p>' + card(a) + '&nbsp;' + card(b) + '</p>')
    parts += [
        pic('systems', 'Built from scratch: ' + '; '.join(f'{x[1]}: {x[2]}' for x in P.SYSTEMS)),
        pic('achievements', 'Achievements: ' + '; '.join(f'{x[1]}, {x[2]}' for x in P.ACHIEVEMENTS)),
        pic('leadership', P.LEADERSHIP_TITLE.capitalize() + ': ' + '; '.join(f'{x[1]}: {x[2]}' for x in P.LEADERSHIP)),
        pic('stack', 'Stack: ' + ', '.join(ids for _, ids in P.STACK)),
    ]
    for i, (_, kicker, title, text, url) in enumerate(P.SIDE):
        parts.append(link(url, pic(f'side-{i}', f'{title}: {text}')))
    text = ('\n\n'.join(parts) + '\n\n<!-- Generated: edit tools/profile.py, then run `python tools/build.py`. '
            'Template by Aryan Jain (github.com/aryan-the-jain), used with permission. -->\n')
    with open(os.path.join(os.path.dirname(HERE), 'README.md'), 'w') as f:
        f.write(text)


if __name__ == '__main__':
    build()
