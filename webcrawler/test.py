import re
ArticleExtract = '\u201eHeimsfaraldur dreps\u00f3ttar var \u00fea\u00f0 s\u00ed\u00f0asta sem b\u00f6rn \u00ed \u00feessum heimshlutum \u00feurftu, \u201c segir UNICEF, < a href =\"https://unicef.is/covid-19-eykur-enn-a-neyd-barna\">\u00ed fr\u00e9tt</>,  um \u00e1standi\u00f0 \u00ed Mi\u00f0austurl\u00f6ndum og Nor\u00f0ur-Afr\u00edku \u00fear sem hvergi \u00ed heiminum eru fleiri b\u00f6rn \u00ed ney\u00f0 vegna str\u00ed\u00f0s\u00e1taka. K\u00f3r\u00f3naveirufaraldurinn barst tilt\u00f6lulega seint \u00ed \u00feessa heimshluta en sta\u00f0fest smit er n\u00fa r\u00famlega 105 \u00fe\u00fasund og dau\u00f0sf\u00f6llin 5.700, flest \u00ed \u00cdran.'

print(ArticleExtract)

AfterTreatment = re.sub(r'<.+?>', '', ArticleExtract)
print(AfterTreatment)

'„Heimsfaraldur drepsóttar var það síðasta sem börn í þessum heimshlutum þurftu,“ segir UNICEF , í frétt,  um ástandið í Miðausturlöndum og Norður-Afríku þar sem hvergi í heiminum eru fleiri börn í neyð vegna stríðsátaka. Kórónaveirufaraldurinn barst tiltölulega seint í þessa heimshluta en staðfest smit er nú rúmlega 105 þúsund og dauðsföllin 5.700, flest í Íran.", "ImageLink": "'
