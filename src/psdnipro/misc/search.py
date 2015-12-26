import re

from django.db.models import Q


__all__ = [
    'get_query',
]

STOP_WORDS = [
    'а', 'аби', 'абикуди', 'абияк', 'або', 'адже', 'але', 'б', 'без', 'безпосередньо', 'би', 'более ,бы', 'був', 'буде',
    'будемо', 'буду', 'будуть', 'будь', 'будь-коли', 'була', 'були', 'було', 'бути', 'был', 'была', 'были', 'было',
    'быть', 'більш', 'біля', 'в', 'вам', 'вас', 'ваш', 'вдалині', 'верх', 'весь', 'вже', 'ви', 'вигляд', 'видно',
    'вищі', 'вниз', 'внизу', 'во', 'вона', 'вони', 'вот', 'врівень', 'все', 'всего', 'всередину', 'всех', 'всупереч',
    'всього', 'вул', 'вы', 'від', 'відноситься', 'відношенні', 'відразу', 'він', 'вісім', 'г', 'где', 'грн', 'ґ', 'д',
    'да', 'даже', 'далі', 'два', 'де', 'де-небудь', "дев'ять", 'деколи', 'декілька', 'десь', 'дехто', 'дечий', 'дещо',
    'деяка', 'деякий', 'деяких', 'деякі', 'для', 'до', 'доки', 'е', 'его', 'ее', 'ей', 'если', 'есть', 'еще', 'ею', 'є',
    'ж', 'же', 'жоден', 'з', 'за', 'замість', 'зате', 'звідки', 'звідки-небудь', 'звідкись', 'звідси', 'згідно',
    'здесь', 'знов', 'знову', 'зовні', 'зовсім', 'зі', 'и', 'из', 'или', 'им', 'их', 'і', 'із', 'із-за', 'інакше',
    'інколи', 'іншим', 'іншими', 'інших', 'іншого', 'іншому', 'іншої', 'інші', 'інщої', 'ї', 'їм', 'їх', 'їхнім', 'її',
    'й', 'його', 'йому', 'к', 'как', 'ко', 'когда', 'когось', 'коли', 'колись', 'коротко', 'котрий', 'котрийсь',
    'крізь', 'крім', 'кто', 'куди', 'куди-небудь', 'кудись', 'л', 'ледве', 'ледь', 'ледь-ледь', 'ли', 'либо', 'лише',
    'м', 'майже', 'мало', 'маю', 'має', 'менш', 'ми', 'мимо', 'мне', 'може', 'может', 'можна', 'мы', 'між', 'містить',
    'н', 'на', 'набагато', 'навздогін', 'навряд', 'навіщо', 'навіщось', 'над', 'надалі', 'надо', 'назад', 'напередодні',
    'нарізно', 'насамперед', 'наскільки', 'настільки', 'наш', 'не', 'небагато', 'небудь', 'него', 'нее', 'немало',
    'нет', 'ни', 'ним', 'них', 'но', 'ну', 'нуль', 'ні', 'ніби', 'ніде', 'ніж', 'ній', 'ніколи', 'нікуди', 'ніскільки',
    'ніхто', 'нічий', 'нічого', 'ніщо', 'о', 'об', 'оба', 'обидва', 'обидві', 'обоє', 'один', 'однак', 'однако',
    'окрім', 'он', 'она', 'они', 'оно', 'оскільки', 'особливо', 'остільки', 'ось', 'от', 'очень', 'п', "п'ять", 'перед',
    'перш', 'по', 'поблизу', 'повно', 'повному', 'под', 'подекуди', 'полягає', 'помалу', 'поряд', 'посередині', 'потім',
    'представляють', 'представляє', 'при', 'про', 'просто', 'проте', 'проти', 'прямо', 'під', 'пізніше', 'після', 'р',
    'ради', 'раз', 'разом', 'разі', 'раніше', 'раптом', 'с', 'своєму', 'свої', 'своїми очима', 'своїх', 'свій', 'серед',
    'складно', 'скільки', 'скільки-небудь', 'скількись', 'со', 'собою', 'собі', 'спереду', 'спершу', 'спочатку',
    'стільки', 'суцільно', 'сім', 'т', 'та', 'так', 'так що', 'также', 'таки', 'такий', 'таким', 'таких', 'такого',
    'також', 'такой', 'такому', 'там', 'те', 'теж', 'тел', 'тем', 'то', 'того', 'тоді', 'тоже', 'той', 'только', 'том',
    'тому', 'треба', 'три', 'тут', 'ты', 'ті', 'тільки', 'у', 'убік', 'увись', 'увісьмох', 'удалину', 'удвох', 'удвічі',
    "удев'ятьох", 'удосталь', 'уже', 'укупі', 'уподовж', 'усередині', 'услід', 'усюди', 'усіх', 'ф', 'х', 'хотя', 'хоч',
    'хоча', 'хто', 'хтось', 'хіба', 'ц', 'це', 'цим', 'цими', 'цих', 'цього', 'цьому', 'цю', 'ця', 'ці', 'цій', 'цією',
    'цієї', 'ч', 'часом', 'чего', 'чей', 'чем', 'через', 'чи', 'чий', 'чий-небудь', 'чийсь', 'чим', 'чином', 'чиє',
    'чиє-небудь', 'чиєсь', 'чого', 'чого-небудь', 'чогось', 'чому', 'чомусь', 'чотири', 'что', 'чтобы', 'чье', 'чья',
    'ш', 'шляхом', 'шість', 'щ', 'ще', 'що', 'що зовсім', 'що мають', 'що має', 'що містить', 'що скільки-небудь',
    'що-небудь', 'щоб', 'щодо', 'щосили', 'щось', 'ь', 'эта', 'эти', 'это', 'ю', 'я', 'як', 'як-небудь', 'яка', 'яке',
    'який', 'якийсь', 'яким', 'якими', 'яких', 'якого', 'якому', 'якось', 'якою', 'якої', 'яку', 'якщо', 'які', 'якій',
]


def get_query(query_string, search_fields):
    """
    Return a query which is a combination of Q objects for normalized query string.

    :param str query_string: search query submitted by user
    :param list[str] search_fields: list of model's fields
    :rtype: django.db.models.Q
    """
    query_string = re.sub('\s\s+', ' ', query_string.strip())
    terms = []
    for elem in query_string.split(' '):
        if any(x.isalpha() for x in elem) and elem not in STOP_WORDS:
            terms.append(elem)

    query = None
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
