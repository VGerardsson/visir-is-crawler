#import textstat as stats
from .mittextstat import textstatistics
import warnings
from functools import lru_cache


class istextstats(textstatistics):

    def _isCountSyllables(self, word):
        sylcounter = 0
        for c in range(len(word)):
            if ((c < (len(word)-1)) and (
                        (word[c] == 'a' and word[c + 1] == 'u')
                        or (word[c] == 'e' and (word[c + 1] == 'i' or word[c + 1] == 'y')))
                    ):
                sylcounter += 1
            elif (word[c] == 'a' or word[c] == 'á' or word[c] == 'e' or word[c] == 'é' or
                  word[c] == 'i' or word[c] == 'í' or word[c] == 'o' or word[c] == 'ó' or
                  word[c] == 'u' or word[c] == 'ú' or word[c] == 'y' or word[c] == 'ý' or
                  word[c] == 'æ' or word[c] == 'ö'):
                sylcounter += 1
        return sylcounter

    def _big_word_count(self, textcontent):
        BigWordText = self.remove_punctuation(textcontent)
        BigWordCounter = 0
        for word in BigWordText.split():
            if self.syllable_count(word) > 6:
                BigWordCounter += 1
        return BigWordCounter

    @lru_cache(maxsize=128)
    def syllable_count(self, text, lang=None):
        """
        Function to calculate syllable words in a text.
        I/P - a text
        O/P - number of syllable words
        """
        if lang:
            warnings.warn(
                "The 'lang' argument has been moved to "
                "'textstat.set_lang(<lang>)'. This argument will be removed "
                "in the future.",
                DeprecationWarning
            )
        if isinstance(text, bytes):
            text = text.decode(self.text_encoding)

        text = text.lower()
        text = self.remove_punctuation(text)

        if not text:
            return 0

        count = 0
        count = self.isCountSyllables(text)
        return count

    def automated_readability_index(self, textcontent):
        Charactercount = None
        WordCount = None
        SentenceCount = None
        ARIndex = None

        WordCount = self.lexicon_count(textcontent)
        SentenceCount = self.sentence_count(textcontent)
        Charactercount = self.char_count(textcontent)

        try:
            if Charactercount != None and WordCount != None and SentenceCount:
                ARIndex = 4.71*(Charactercount/WordCount) + \
                    0.5 * (WordCount / SentenceCount) - 21.43
                ARIndex = round(ARIndex)
        except ZeroDivisionError:
            ARIndex = 0.0
        return ARIndex


""" word = 'Öllum þeim sem koma til landsins verður skylt að fara í sóttkví í fjórtán daga frá komu. Samhliða því verður tekið upp tímabundið landamæraeftirlit á innri landamærum. Reglurnar koma til framkvæmda föstudaginn 24. apríl og falla að óbreyttu úr gildi 15. maí. Þetta kemur fram að í tilkynningu sem birtist á vef stjórnarráðsins. Segir að Svandís Svavarsdóttir heilbrigðisráðherra hafi breytt reglum um sóttkví í samræmi við tillögu sóttvarnalæknis.Á við um fólk sem kemur frá há-áhættusvæðum Krafan um sóttkví er sögð eiga við um komu fólks frá löndum sem sóttvarnalæknir skilgreinir sem há-áhættusvæði en sem stendur eigi það við um öll lönd. Reglulega verði endurmetið hvort einhver lönd falli ekki lengur undir þessa skilgreiningu.Eins og fram kemur í minnisblaði sóttvarnalæknis hefur að mestu tekist að ráða niðurlögum COVID-19 faraldursins hér á landi þannig að einungis nokkur tilfelli greinast daglega. Eitt mikilvægasta atriðið til að viðhalda stöðunni og koma í veg fyrir víðtækan faraldur hér á landi er að tryggja að smit berist ekki hingað frá öðrum löndum. Verkefnahópur undir stjórn ríkislögreglustjóra sem stofnaður var að beiðni sóttvarnalæknis hefur skilað tillögum sínum. Niðurstaða hópsins er sú að skynsamlegast sé að útvíkka reglur um sóttkví þannig að þær taki til allra sem koma til landsins en hingað til hefur það ekki gilt um ferðamenn,“ segir í tilkynningunni.Ennfremur segir að til að framfylgja breyttum reglum um sóttkví þurfi að taka upp tímabundið landamæraeftirlit á innri landamærum Schengen-svæðisins í samræmi við útlendingalög og reglugerð um för yfir landamæri.Gerð verður krafa til þeirra sem flytja farþega til landsins að þeir útfylli svokallað e. Public Health Passenger Locator eða sambærilegt form og munu farþegar þurfa að framvísa því við landamæraeftirlit. Með því er gert að skilyrði við komu fólks til landsins að fyrir liggi allar nauðsynlegar upplýsingar um hvar viðkomandi muni dvelja í sóttkví og hvernig henni verður háttað.Á fundi ríkisstjórnar í gær var samþykkt að starfshópur nokkurra ráðuneyta sem leiddur verður af forsætisráðuneytinu muni fjalla um möguleg næstu skref varðandi ferðalög milli landa. Ákvarðanir um hvert framhaldið verður munu ráðast af þróun faraldursins hérlendis og erlendis og taka mið af stefnu annarra ríkja í þessum efnum,“ segir í tilkynningunni.'


TextStatHandler = istextstats()
TextStats = TextStatHandler.automated_readability_index(word) """
