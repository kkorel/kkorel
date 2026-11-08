"""Builds the stack icon strips in tools/cache/ from a local copy of skill-icons.

    git clone --depth 1 https://github.com/tandpfun/skill-icons /path/to/skill-icons
    python tools/make_icons.py /path/to/skill-icons

Produces the same strip skillicons.dev would serve (dark theme), for when that
site can't be reached. Icons are by tandpfun/skill-icons, MIT licensed.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import profile as P  # noqa: E402

# skillicons id -> icon file stem
FILES = {
    'py': 'Python', 'c': 'C', 'cpp': 'CPP', 'ts': 'TypeScript', 'scala': 'Scala', 'kotlin': 'Kotlin',
    'java': 'Java', 'haskell': 'Haskell', 'bash': 'Bash', 'pytorch': 'PyTorch', 'sklearn': 'ScikitLearn',
    'tensorflow': 'TensorFlow', 'react': 'React', 'nextjs': 'NextJS', 'nodejs': 'NodeJS',
    'postgres': 'PostgreSQL', 'redis': 'Redis', 'aws': 'AWS', 'docker': 'Docker', 'linux': 'Linux',
    'git': 'Git', 'githubactions': 'GithubActions', 'cloudflare': 'Cloudflare',
}


def icon(root, key, n):
    stem = FILES[key]
    for name in (f'{stem}-Dark.svg', f'{stem}.svg'):
        path = os.path.join(root, 'icons', name)
        if os.path.exists(path):
            svg = open(path).read()
            break
    else:
        raise SystemExit(f'No icon for {key}')
    # Give each icon's gradient/clip ids a unique prefix so they can't collide in one strip.
    ids = set(re.findall(r'id="([^"]+)"', svg))
    for i in sorted(ids, key=len, reverse=True):
        svg = svg.replace(f'id="{i}"', f'id="i{n}_{i}"').replace(f'url(#{i})', f'url(#i{n}_{i})') \
                 .replace(f'href="#{i}"', f'href="#i{n}_{i}"')
    return svg


def main():
    root = sys.argv[1]
    os.makedirs(os.path.join(HERE, 'cache'), exist_ok=True)
    for _, ids in P.STACK:
        keys = ids.split(',')
        w = len(keys) * 300 - 44
        body = ''.join(f'<g transform="translate({i * 300}, 0)">{icon(root, k, i)}</g>' for i, k in enumerate(keys))
        out = (f'<svg width="{w * 48 // 256}" height="48" viewBox="0 0 {w} 256" fill="none" '
               f'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">{body}</svg>')
        path = os.path.join(HERE, 'cache', ids.replace(',', '-') + '.svg')
        with open(path, 'w') as f:
            f.write(out)
        print(f'{len(keys)} icons -> {os.path.relpath(path, HERE)}')


if __name__ == '__main__':
    main()
