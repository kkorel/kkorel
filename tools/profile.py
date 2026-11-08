"""Everything the profile graphics say. Edit this, then run `python tools/build.py`."""

NAME = 'Kuzey Korel'
KICKER = 'MENG MATHS & CS  ·  FIRST-CLASS  ·  IMPERIAL COLLEGE LONDON'
TAGLINE = ''  # optional line under the name; leave empty for none
# Contact row along the bottom of the hero: (glyph, text)
CONTACTS = [('linkedin', 'kuzeykorel'), ('mail', 'kuzey.korel24@imperial.ac.uk')]
LINKEDIN = 'https://www.linkedin.com/in/kuzeykorel/'
EMAIL = 'kuzey.korel24@imperial.ac.uk'

NOW = (2026, 11)  # the "now" line on the timeline

HIGHLIGHTS = [
    ('briefcase', 'Amazon', 'SDE intern, return offer'),
    ('trophy', 'Amadeus Award', 'Best of 55 2nd-year groups'),
    ('medal', 'IC Hack 2026', '2nd place, Europe\'s largest'),
    ('chart', 'QRT Quant Challenge', '2nd of 86 university teams'),
]

NOW_ITEMS = [
    ('bolt', 'Research Engineer · Oorja',
     "Peer-to-peer solar trading on India's Digital Energy Grid pilot, and research on a governance layer for "
     'multi-agent systems: permissions, escalation and audit trails.', None),
    ('people', 'Treasurer & Head of Lectures, Imperial AI Society',
     'Weekly ML and AI lectures to 150 students, live-coding every model, from an MLP in PyTorch to a transformer '
     'built from scratch in NumPy.', None),
    ('cap', 'Year 3 · MEng Mathematics and Computer Science', 'First Class Honours in Year 2.', None),
]

# (logo file or glyph, organisation, role, start (y, m), end (y, m) or None for ongoing, kind)
EXPERIENCE = [
    ('glyph:box', 'Amazon · Prime Video', 'Software Development Engineer Intern', (2026, 7), (2026, 9), 'work'),
    ('glyph:bolt', 'Oorja', 'Research Engineer, peer-to-peer energy trading', (2026, 1), None, 'work'),
    ('imperial', 'Imperial College London', 'MEng Mathematics and Computer Science', (2024, 10), None, 'study'),
    ('glyph:tyre', 'Tyres Life UK', 'Software Engineering Intern', (2024, 6), (2024, 7), 'work'),
    ('glyph:sigma', "KCL Mathematics School",'A-levels: Maths A*, Further Maths A*, Physics A',
     (2022, 9), (2024, 7), 'study'),
]

IMPACT = {
    'logo': 'glyph:box',
    'title': 'AMAZON  ·  PRIME VIDEO',
    'subtitle': 'SDE INTERN  ·  JUL–SEP 2026  ·  RETURN OFFER',
    'stats': [
        ('1,991', 'latency alarms audited', "across Prime Video's Apple fleet"),
        ('700+', 'alarms', 'that could never fire'),
        ('74%', 'false alarms', 'of alerts that fired (approx.)'),
        ('Daily', 'fleet-wide run', 'feeding a live dashboard'),
    ],
    'bullets': [
        "Built an end-to-end TypeScript tool that audits every latency alarm, recommends a threshold from each metric's "
        'own history and backtests it over weeks of real data.',
        'Shipped an on-call ticket bot: when a latency alarm pages, it re-audits the alarms that fired and comments the '
        'result and recommended thresholds on the ticket before the on-call engineer opens it.',
        'Kept the daily run inside AWS Lambda limits with a per-segment rolling metric cache in S3, refreshed '
        'incrementally and seeded by a one-time sharded backfill as a Step Functions fan-out.',
    ],
}

# Project cards. icon: logo file or 'glyph:<name>'. url may be None.
PROJECTS = {
    'p2p': {
        'icon': 'glyph:bolt',
        'title': 'P2P energy trading',
        'badge': 'OORJA  ·  INDIA AI IMPACT SUMMIT',
        'text': "Households trade rooftop solar directly on India's Digital Energy Grid pilot. I built the trading core: "
                'no overselling under concurrent buyers, partial-delivery settlement, trust tiers and the order matcher.',
        'tags': ['TypeScript', 'Beckn', 'Redis'],
        'url': 'https://github.com/kkorel/p2p-trading',
    },
    'clam': {
        'icon': 'glyph:prompt',
        'title': 'CLAM',
        'badge': '2ND PLACE  ·  IC HACK 2026',
        'text': 'A Bash assistant that turns a half-typed command or plain-English request into runnable shell commands. '
                'It wraps rm, dd and 7 other risky commands so an LLM vets each call before it runs.',
        'tags': ['Bash', 'LLMs', 'Local models'],
        'url': 'https://github.com/kkorel/CLAM-IC-HACK-2026',
    },
    'fair': {
        'icon': 'glyph:offline',
        'title': 'Fair Companion',
        'badge': '~1,200 STUDENTS  ·  WELCOME FAIR',
        'text': "Helped about 1,200 students find societies at Imperial's Welcome Fair, even with no signal. Offline-first, "
                'with an AI assistant limited to the society list and capped per device, per network and globally.',
        'tags': ['Next.js', 'TypeScript', 'Cloudflare'],
        'url': None,
    },
    'alongside': {
        'icon': 'glyph:alongside',
        'title': 'Alongside',
        'badge': 'AMADEUS AWARD  ·  BEST OF 55',
        'text': 'Facilitated peer-support groups for bereaved young adults: a group room, a private line to the '
                "facilitator, a quiet space and a facilitator dashboard. Imperial's best second-year group project.",
        'tags': ['Next.js', 'Scala Play', 'PostgreSQL'],
        'url': 'https://github.com/aryan-the-jain/DRP_07',
    },
}

SYSTEMS_NOTE = 'IMPERIAL COURSEWORK  ·  TEACHING'
SYSTEMS = [
    ('glyph:braces', 'WACC compiler', 'Scala 3 to x86-64: parser combinators, typed AST, two-stage IR backend. 180+ tests pass.'),
    ('glyph:terminal', 'PintOS kernel', 'Priority donation across lock chains, a fixed-point MLFQS and 13 syscalls. 116/116 tests.'),
    ('glyph:chip', 'ARMv8 toolchain', 'Two-pass assembler and fetch-decode-execute emulator for AArch64, in C.'),
    ('glyph:layers', 'Transformer by hand', 'Built from scratch in NumPy, live-coded for an AI Society lecture.'),
]

# (glyph, title, detail, chip)
ACHIEVEMENTS = [
    ('chart', 'QRT Quant Challenge 2025', '2nd of 86 university teams', 'QUANT'),
    ('medal', 'Cayley Olympiad: Gold', 'Top 20 of 100,000+ entrants', 'UKMT'),
    ('star', 'British Mathematical Olympiad: Round 1 Distinction', 'UKMT Challenge Gold and Best in School, six years running', 'UKMT'),
    ('sigma', 'STEP II Grade 1  ·  MAT 84/100  ·  TMUA 8.4/9.0', 'TMUA in the top 2%', 'ADMISSIONS'),
]

LEADERSHIP = [
    ('people', 'Imperial AI Society', 'Treasurer and Head of Lectures, teaching ML to 150 students every week.'),
    ('cap', 'Maths tutoring', 'Five years of tutoring mathematics.'),
    ('tyre', 'Tyres Life UK', 'Automated daily price tracking of 5 suppliers, saving the team 5 hours a day.'),
    ('note', 'Piano', 'ABRSM Grade 8.'),
    ('dance', 'Salsa', 'Imperial Salsa Team.'),
    ('mountain', 'Off the keyboard', 'Chess, poker, climbing and skydiving.'),
]

STACK = [
    ('LANGUAGES', 'py,c,cpp,ts,scala,kotlin,java,haskell,bash'),
    ('ML · SYSTEMS · WEB', 'pytorch,sklearn,tensorflow,react,nextjs,nodejs,postgres,redis,aws,docker,linux,git'),
]

# "Year in work" heatmap. Days with commits use real counts from
# tools/cache/contributions.json (your commits in public GitHub repos, or run
# tools/fetch_github.py). Work no public repo shows (Imperial GitLab, Amazon) is
# estimated from these periods: (start, end, weekday 0-1, weekend 0-1, source).
# 'gitlab' periods are dropped once tools/cache/gitlab.json exists (run tools/fetch_gitlab.py).
YEAR_START = (2025, 10, 1)
YEAR_END = (2026, 11, 8)
YEAR_PERIODS = [
    ((2025, 10, 6), (2025, 10, 12), 0.45, 0.2, 'gitlab'),     # term 1, week 1
    ((2025, 10, 13), (2025, 11, 28), 0.84, 0.22, 'gitlab'),   # PintOS
    ((2025, 11, 29), (2025, 12, 12), 0.4, 0.2, 'gitlab'),
    ((2025, 12, 13), (2026, 1, 9), 0.15, 0.1, 'gitlab'),
    ((2026, 1, 10), (2026, 3, 20), 0.9, 0.25, 'gitlab'),      # WACC
    ((2026, 3, 21), (2026, 4, 26), 0.28, 0.18, 'gitlab'),
    ((2026, 4, 27), (2026, 6, 20), 0.5, 0.25, 'gitlab'),      # term 3, Alongside
    ((2026, 7, 6), (2026, 9, 25), 0.92, 0.35, 'private'),     # Amazon (+ Fair Companion on weekends)
    ((2026, 10, 5), (2026, 11, 8), 0.5, 0.25, 'gitlab'),      # year 3, term 1
]
YEAR_TERMS = [((2025, 10, 6), (2025, 12, 12)), ((2026, 1, 10), (2026, 3, 20)), ((2026, 4, 27), (2026, 6, 20)),
              ((2026, 10, 5), (2026, 12, 11))]
YEAR_COURSEWORK = 0.25  # weekly GitLab coursework during term (estimate only)
YEAR_BACKGROUND = 0.06  # side projects outside the main blocks
YEAR_NOTE = 'Public GitHub commits are exact. Imperial GitLab coursework and Amazon work are estimated.'
YEAR_NOTE_GITLAB = 'GitHub and Imperial GitLab commits are exact. Amazon work is estimated.'

# Two lines under the grid: the main thing, and what ran alongside it.
YEAR_TRACKS = [
    ('MAIN', [((2025, 10, 13), (2025, 11, 28), 'PintOS · term 1'), ((2026, 1, 12), (2026, 3, 20), 'WACC compiler'),
              ((2026, 4, 27), (2026, 6, 19), 'Alongside · DRP'), ((2026, 7, 6), (2026, 9, 25), 'Amazon · Prime Video'),
              ((2026, 10, 5), (2026, 11, 8), 'Year 3')]),
    ('ALONGSIDE', [((2026, 1, 10), (2026, 3, 20), 'Oorja P2P trading + CLAM'),
                   ((2026, 4, 27), (2026, 6, 20), 'Coursework + exams'),
                   ((2026, 8, 1), (2026, 9, 25), 'Fair Companion'),
                   ((2026, 10, 5), (2026, 11, 8), 'Oorja + lectures')]),
]

# Small linked rows at the end: (glyph, label, title, text, url)
SIDE = [
    ('glyph:tree', 'IC HACK 2025', 'Pathfinder', 'Turns a decision into a branching tree of questions and likely futures, generated by Claude.',
     'https://github.com/kkorel/Pathfinder-IC-HACK-2025'),
    ('glyph:cap', 'SELF-STUDY', 'Harvard CS50 AI', '12 projects, from minimax and Bayesian networks to Q-learning and BERT attention.',
     'https://github.com/kkorel/Harvard-CS50-AI-Projects'),
]
