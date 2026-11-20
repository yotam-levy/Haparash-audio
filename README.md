# הפרש: קבצי הפודקאסט

הריפו הזה מאחסן את הפרקים של "הפרש" ואת פיד ה־RSS שספוטיפיי קורא.

- הפיד: https://podcast.yotamlevy.com/haparash/feed.xml (מפנה ל־feed.xml כאן, דרך GitHub Pages)
- הפרקים: `episodes/haparash-epNN.mp3`
- הנתונים של כל פרק (שם, תיאור, מזהה, תאריך): `episodes.json`

## איך מפרסמים פרק חדש
1. שמים את הקובץ ב־`episodes/haparash-epNN.mp3`.
2. מוסיפים רשומה ל־`episodes.json` עם מזהה (guid) חדש שלא ישתנה לעולם.
3. מריצים `python3 build_feed.py` ודוחפים ל־main.

לא משנים guid של פרק קיים, אחרת ספוטיפיי יראה אותו כפרק חדש.
