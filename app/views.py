import itertools
import math
import re
from collections import OrderedDict

from django.db.models import F
from django.shortcuts import render

from .models import Word_in_texts

TOTAL_DOC_KEY = '__count_doc'


def get_updated_quantity(word):
    data, created = Word_in_texts.objects.get_or_create(
                                word=word, defaults={'quantity': 0}
    )
    data.quantity = F('quantity') + 1
    data.save(update_fields=['quantity'])
    data.refresh_from_db()
    return data.quantity


def upload(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload'].read().decode('utf-8')
        upload = re.sub(r'[^\w\s]', '', upload)
        text = upload.split()
        count = get_updated_quantity(TOTAL_DOC_KEY)
        words = {}
        for word in text:
            if word in words:
                words[word][0] += 1
            else:
                words[word] = [1]
        for k, v in words.items():
            word_in_texts = get_updated_quantity(k)
            idf = round(math.log10(count/word_in_texts), 2)
            words[k].append(idf)
        words = OrderedDict(sorted(words.items(),
                                  key=lambda kv: kv[1][1], reverse=True))
        words = dict(itertools.islice(words.items(), 50))
        return render(request, 'upload.html', {'words': words})
    return render(request, 'upload.html')
 