import csv
from requests_html import HTML
import unicodedata
import re
import sys


def remove_emojis(data):
    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
                      u"\U00002702-\U000027B0"
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)


filename = sys.argv[1]
reviews = open(filename, "r", encoding="utf8")

text = reviews.read()

html_r = HTML(html=text)
# print(html_r.find('div'))

count = 0
data = []

nombre = ""
review = ""
calificacion = ""
for element in html_r.find('div'):
    # print(element.attrs)
    # print(element)

    if 'class' in element.attrs:
        if 'ODSEW-ShBeI-title' in element.attrs['class']:
            nombre = element.text
            # print(element.text)

        if 'ODSEW-ShBeI-jfdpUb' in element.attrs['class']:
            # encabezado resena
            encabezado = HTML(html=element.html)

            for sub_element in encabezado.find('span'):
                if 'aria-label' in sub_element.attrs:
                    # estrellas =
                    # calificacion = unicodedata.normalize(
                    #     "NFKD", sub_element.attrs['aria-label'])
                    calificacion = int(sub_element.attrs['aria-label'].split(u'\xa0')[
                        0].replace(" ", "")) - 1
                    # print(sub_element.attrs['aria-label'])
                    # print(element.html)

        if 'ODSEW-ShBeI-ShBeI-content' in element.attrs['class']:
            review = remove_emojis(element.text)
            count += 1

            res = {
                "username": nombre,
                "review": review,
                "calificacion": calificacion
            }
            data.append(res)
            nombre = ""
            review = ""
            calificacion = ""
            # print(element.attrs['class'])
            # print(element.text)
            # if element.attrs['class'] == 'ODSEW-ShBeI-ShBeI-content':
            #     print(element)
            # reviews_text = [x for x in list(
            #     html_r) if x.startswith('/es/telas/')]


print(count)
# print(data)


csv_columns = ['username', 'review', 'calificacion']

csv_file = "reviews_final.csv"
try:
    with open("{}-{}.csv".format(filename.split(".")[0], count), 'w', encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerows(data)
        # for info in data:
        #     # print(info)
        #     writer.writerow(info)
except IOError:
    print("I/O error")
