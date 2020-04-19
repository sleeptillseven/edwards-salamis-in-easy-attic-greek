#!/usr/bin/env python3

from roman_numerals import convert_to_numeral

WORK_LIST = [
    "preface",
    "introduction",
    "main",
]

TITLES = {
    "preface": "Preface",
    "introduction": "Introduction",
    "main": "Main Text",
}

for WORK in WORK_LIST:
    print("processing: " + WORK)
    SRC = f"../text/edwards-salamis-{WORK}.txt"
    DEST = f"../docs/edwards-salamis-{WORK}.html"

    TITLE = TITLES[WORK]

    HEADER = f"""\
    <!DOCTYPE html>
    <html lang="grc">
    <head>
    <title>{TITLE}</title>
    <meta charset="utf-8">
    <link href="https://fonts.googleapis.com/css?family=Noto+Serif:400,700&amp;subset=greek,greek-ext" rel="stylesheet">
    <link href="style.css" rel="stylesheet">
    </head>
    <body>
      <div class="container">
      <nav>&#x2191; <a href="./">Edwards' Salamis in Easy Attic Greek</a></nav>
    """
      #<h1 lang="en">{TITLE}</h1>

    FOOTER = """\
        <br/><br/>
        <nav>&#x2191; <a href="./">Edward's Salamis in Easy Attic Greek</a></nav>
        <br/>
        <p>This work is licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.</p>
        <p>The source is available at <a href="https://github.com/sleeptillseven/edwards-salamis-in-easy-attic-greek">https://github.com/sleeptillseven/edwards-salamis-in-easy-attic-greek</a>.</p>
      </div>
    </body>
    </html>
    """

    with open(SRC) as f:
        with open(DEST, "w") as g:
            prev_section = None
            prev_chapter = None
            print(HEADER, file=g)
            for line in f:
                parts = line.strip().split(maxsplit=1)
                ref = parts[0].split(".")
                if len(ref) == 2:
                    section = None
                    chapter, verse = ref
                else:
                    section, chapter, verse = ref
                if prev_section != section:
                    if prev_section is not None:
                        print("   </div>""", file=g)
                        print("   </div>""", file=g)
                    print("""   <div class="section">""", file=g)
                    prev_section = section
                    prev_chapter = None
                if prev_chapter != chapter:
                    if prev_chapter is not None:
                        if prev_chapter == "0":
                            if section is None:
                                print("""    </div>""", file=g)
                        else:
                            print("""    </div>""", file=g)
                    if chapter == "0":
                        if section is None:
                            print("""    <div class="preamble">""", file=g)
                    else:
                        if chapter == "title":
                            print("""    <div class="subscription">""", file=g)
                        elif chapter == "subtitle":
                            print("""    <div class="epilogue">""", file=g)
                        else:
                            if not chapter == "text":
                                print("""    <div class="chapter">""", file=g)
                                print(f"""      <h3 class="chapter_ref">{chapter} {parts[1]}</h3>""", file=g)
                            else:
                               print("""    <div class="chapter">""", file=g) 
                    prev_chapter = chapter
                    next
                if chapter == "0" and verse == "0":
                    print(f"""    <h2 class="section_title">{parts[1]}</h2>""", file=g)
                else:
                    if chapter != "0" and verse == "0":
                        print(f"""<h3 class="epilogue_title">{parts[1]}</h3>""", file=g)
                    else:
                        # HANDLE VERSE
                        if not (verse == "title" or chapter == "0" or chapter == "text"):
                            print(f"""      <span class="verse_ref">{verse}</span>""", end="&nbsp;", file=g)
                            print(parts[1], file=g)
                            print(f"""      <br/>""", file=g)
                        else:
                            if chapter == "text":
                                print(f"""   <p>{parts[1]}</p>""", file=g)

            print("""    </div>""", file=g)

            if section is not None:
                print("""    </div>""", file=g)
            print(FOOTER, file=g)

