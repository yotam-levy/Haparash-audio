#!/usr/bin/env python3
"""Builds feed.xml for the HaParash podcast from episodes.json.

Each episode in episodes.json needs: n, title, guid, date (ISO, UTC), description,
and an mp3 at episodes/haparash-epNN.mp3. Only episodes listed in episodes.json
appear in the feed, so adding an entry there is what publishes an episode.
"""
import json, os, subprocess, sys
from datetime import datetime, timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO_BASE = "https://yotam-levy.github.io/Haparash-audio"
FEED_URL = "https://podcast.yotamlevy.com/haparash/feed.xml"
SITE_URL = "https://podcast.yotamlevy.com/haparash"

SHOW = {
    "title": "הפרש",
    "author": "יותם לוי",
    "email": "yl0504144536@gmail.com",
    "description": "יונתן רז רואה דרך אנשים. בגיל 30 הקליניקה שלו קורסת, החובות נערמים, והמשפחה מתרחקת – ואז מגיע פוליטיקאי שמזהה בו את מה שהוא צריך: הפרש שלו. דרמת אודיו ישראלית על כוח, חובות, והמחיר של לראות יותר מכולם.",
    "image": f"{AUDIO_BASE}/cover.jpg",
    "language": "he",
}


def duration(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                   "-of", "csv=p=0", path], text=True)
    return int(round(float(out.strip())))


def hms(s):
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def main():
    eps = json.load(open(os.path.join(ROOT, "episodes.json"), encoding="utf-8"))
    eps.sort(key=lambda e: e["date"], reverse=True)
    items = []
    for e in eps:
        rel = f"episodes/haparash-ep{e['n']:02d}.mp3"
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            sys.exit(f"missing {rel}")
        date = datetime.fromisoformat(e["date"].replace("Z", "+00:00")).astimezone(timezone.utc)
        items.append(f"""    <item>
      <title>{escape(e['title'])}</title>
      <description><![CDATA[{e['description']}]]></description>
      <itunes:summary><![CDATA[{e['description']}]]></itunes:summary>
      <guid isPermaLink="false">{e['guid']}</guid>
      <pubDate>{format_datetime(date)}</pubDate>
      <enclosure url="{AUDIO_BASE}/{rel}" length="{os.path.getsize(path)}" type="audio/mpeg"/>
      <itunes:duration>{hms(duration(path))}</itunes:duration>
      <itunes:episode>{e['n']}</itunes:episode>
      <itunes:episodeType>full</itunes:episodeType>
      <itunes:explicit>false</itunes:explicit>
    </item>""")

    s = SHOW
    owner = f"""
    <itunes:owner>
      <itunes:name>{escape(s['author'])}</itunes:name>
      <itunes:email>{escape(s['email'])}</itunes:email>
    </itunes:owner>""" if s["email"] else ""
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{escape(s['title'])}</title>
    <link>{SITE_URL}</link>
    <atom:link href="{FEED_URL}" rel="self" type="application/rss+xml"/>
    <language>{s['language']}</language>
    <description><![CDATA[{s['description']}]]></description>
    <itunes:summary><![CDATA[{s['description']}]]></itunes:summary>
    <itunes:author>{escape(s['author'])}</itunes:author>{owner}
    <itunes:image href="{s['image']}"/>
    <image><url>{s['image']}</url><title>{escape(s['title'])}</title><link>{SITE_URL}</link></image>
    <itunes:category text="Fiction"><itunes:category text="Drama"/></itunes:category>
    <itunes:explicit>false</itunes:explicit>
    <itunes:type>serial</itunes:type>
{chr(10).join(items)}
  </channel>
</rss>
"""
    open(os.path.join(ROOT, "feed.xml"), "w", encoding="utf-8").write(xml)
    print(f"feed.xml: {len(items)} episodes")


if __name__ == "__main__":
    main()
