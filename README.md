# merriamscraper
beginnings of code to scrape merriam-webster for all words in the english language, extracting the phonetics of every word from the web pages to get the syllables
<h1>Why?</h1>
For my haiku generator (haikugenerate.com) I need the syllables for every word, to keep the 5 7 5 syllable structure. 

To do this at the moment, I have a basic algorithm which looks at the incidence of vowels and consonants, it's ~80% correct.

As phonetics in English is basically a guessing game, I wrote a program to scrape merriamwebster.com as it seems like they have the syllable count for most words there.

It's fairly arbitrary, parsing the HTML to get to the syllable part of the website, and it will take about 3 days to run to get every word on their site, but once I run it it should make my haiku generator more accurate.
