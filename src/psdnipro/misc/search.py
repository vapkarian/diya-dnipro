"""
Code originally by Julien Phalip:
http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap
"""
import re
from django.db.models import Q


__all__ = [
    'get_query',
]

STOP_WORDS_EN = r"""\b(a|about|above|across|after|afterwards|again|against|all|almost|alone|along|already|also|although|
always|am|among|amongst|amoungst|amount|an|and|another|any|anyhow|anyone|anything|anyway|anywhere|are|around|as|at|back|
be|became|because|become|becomes|becoming|been|before|beforehand|behind|being|below|beside|besides|between|beyond|bill|
both|bottom|but|by|call|can|cannot|cant|co|computer|con|could|couldnt|cry|de|describe|detail|do|done|down|due|during|
each|eg|eight|either|eleven|else|elsewhere|empty|enough|etc|even|ever|every|everyone|everything|everywhere|except|few|
fifteen|fify|fill|find|fire|first|five|for|former|formerly|forty|found|four|from|front|full|further|get|give|go|had|
has|hasnt|have|he|hence|her|here|hereafter|hereby|herein|hereupon|hers|herself|him|himself|his|how|however|hundred|i|ie|
if|in|inc|indeed|interest|into|is|it|its|itself|keep|last|latter|latterly|least|less|ltd|made|many|may|me|meanwhile|
might|mill|mine|more|moreover|most|mostly|move|much|must|my|myself|name|namely|neither|never|nevertheless|next|nine|no|
nobody|none|noone|nor|not|nothing|now|nowhere|of|off|often|on|once|one|only|onto|or|other|others|otherwise|our|ours|
ourselves|out|over|own|part|per|perhaps|please|put|rather|re|same|see|seem|seemed|seeming|seems|serious|several|she|
should|show|side|since|sincere|six|sixty|so|some|somehow|someone|something|sometime|sometimes|somewhere|still|such|
system|take|ten|than|that|the|their|them|themselves|then|thence|there|thereafter|thereby|therefore|therein|thereupon|
these|they|thick|thin|third|this|those|though|three|through|throughout|thru|thus|to|together|too|top|toward|towards|
twelve|twenty|two|un|under|until|up|upon|us|very|via|was|we|well|were|what|whatever|when|whence|whenever|where|
whereafter|whereas|whereby|wherein|whereupon|wherever|whether|which|while|whither|who|whoever|whole|whom|whose|why|
will|with|within|without|would|yet|you|your|yours|yourself|yourselves)\b"""

STOP_WORDS_UA = r"""\b(аби|абикуди|абияк|або|але|без|би|біля|більш|буде|будемо|буду|будуть|будь|коли|були|було|бути|вас|
ваш|вдалині|верх|весь|вже|ви|вигляд|видно|вищі|від|відноситься|відразу|він|вниз|внизу|вона|вони|врівень|все|всередину|
все|таки|всупереч|всього|далі|де|декілька|деколи|де|небудь|десь|дехто|дечий|дещо|деякий|для|до|доки|є|ж|жоден|з|за|
замість|зате|звідки|звідки-небудь|звідкись|звідси|згідно|знов|знову|зовні|зовсім|і|із|за|інакше|інколи|інших|інші|її|їх|
його|йому|когось|коли|коли|колись|коротко|котрий|котрийсь|крізь|куди|куди|кудись|ледве|ледь|лише|майже|мало|ми|мимо|між|
містить|містить|може|можна|на|набагато|навздогін|навіщо|навіщось|навряд|чи|над|надалі|назад|нарізно|наскільки|настільки|
наш|не|небагато|немало|ним|ні|якому|разі|раз|ніби|ніде|ніколи|нікуди|ніскільки|ніхто|нічий|нічого|ніщо|обоє|окрім|
оскільки|особливо|остільки|ось|перед|під|пізніше|після|по|поблизу|повно|подекуди|полягає|помалу|поряд|своєму|посередині|
потім|представляє|представляють|при|про|просто|проте|проти|прямо|ради|разом|раніше|раптом|своїми очима|серед|скільки|
скількись|складно|собі|собою|спереду|спершу|спочатку|стільки|суцільно|та|так|так що|такий|також|там|те|теж|то|хіба|того|
тоді|той|той|що містить|том|тому|треба|тут|у|відношенні|убік|увись|увісьмох|удалину|удвічі|удвічі|удвох|удев'ятьох|
удосталь|укупі|уподовж|усередині|услід|усюди|хоч|хоча|хто|хтось|це|цим|цих|ці|цьому|часом|через|чи|чиє|чиєсь|чий|чий|
небудь|чийсь|чим|чого|чого-небудь|чогось|чому|чомусь|шляхом|ще|що|що зовсім|що має|що мають|що скільки-небудь|щоб|
що-небудь|щосили|щось|я|і|раніше|якийсь|як-небудь|якось|якщо|й|ті|від|ці|ця|цю|цієї|усіх|які|якої|якою|якому|грн|якщо|
цього|свої|своїх|зі|з|або|ні|інщої|як|яка|якої|деяких|деяка|деякий|якщо|які|яке|яку|яким|яких|який|якій|якими|якого|або|
такому|таких|таким|такого|адже|має|маю|їхнім|вул|тел|якщо|якому|їм|щодо|об|оба|обидва|обидві|був|була|було|під|ці|ця|
цією|цими|цим|цій|ній|свій|іншому|інших|іншим|іншого|іншої|іншими|тільки|деякі|повному|насамперед|крім|того|напередодні|
безпосередньо|однак|ніж|таким|чином|менш|ніж|більш|перш|будь-коли|де-небудь|із-за|куди-небудь|ледь-ледь|чиє-небудь|
чий-небудь|чого-небудь|скільки-небудь|що-небудь|як-небудь)\b"""
STOP_WORDS_RE = re.compile(STOP_WORDS_UA, re.IGNORECASE)


def normalize_query(query_string):
    """
    Split the query string into individual keywords, getting rid of unnecessary spaces and grouping quoted words
    together.

    :param str query_string: search query submitted by user
    :rtype: list[str]
    """
    find_terms = re.compile(r'"([^"]+)"|(\S+)').findall
    normalize_space = re.compile(r'\s{2,}').sub

    # Split the string into terms.
    terms = find_terms(query_string)

    # Only send unquoted terms through the stop words filter.
    for index, term in enumerate(terms):
        if term[1] is not '':
            # If the term is a stop word, delete it from the list.
            if STOP_WORDS_RE.sub('', term[1]) is '':
                del terms[index]

    return [normalize_space(' ', (t[0] or t[1]).strip()) for t in terms]


def get_query(query_string, search_fields):
    """
    Return a query which is a combination of Q objects.

    :param str query_string: search query submitted by user
    :param list[str] search_fields: list of model's fields
    """
    query = None
    terms = normalize_query(query_string)

    for term in terms:
        or_query = None

        for field_name in search_fields:
            q = Q(**{field_name + '__icontains': term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q

        if query is None:
            query = or_query
        else:
            query = query & or_query

    return query

# entry_query = get_query('search query', ['title', 'body'])
# results = Post.objects.filter(is_active=True).filter(entry_query).distinct()
