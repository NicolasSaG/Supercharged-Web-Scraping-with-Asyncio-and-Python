from requests_html import HTML

reviews = open("data2.txt", "r", encoding="utf8")

text = reviews.read()

html_r = HTML(html=text)
# print(html_r.find('div'))

count = 0
data = []
for element in html_r.find('div'):
    # print(element.attrs)
    # print(element)
    if 'class' in element.attrs:
        if 'ODSEW-ShBeI-title' in element.attrs['class']:

            print(element.text)

        if 'ODSEW-ShBeI-ShBeI-content' in element.attrs['class']:
            count += 1
            # print(element.attrs['class'])
            print(element.text)
            # if element.attrs['class'] == 'ODSEW-ShBeI-ShBeI-content':
            #     print(element)
            # reviews_text = [x for x in list(
            #     html_r) if x.startswith('/es/telas/')]


print(count)
