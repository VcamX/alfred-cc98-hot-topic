#!/usr/bin/python
# encoding: utf-8

import sys
import re
from workflow import Workflow, web

def fix_authors(authors, sections):
    j = 0
    updated_authors = []
    for i in xrange(len(sections)):
        if sections[i] == u'心灵之约':
            updated_authors.append(u'匿名')
        else:
            updated_authors.append(authors[j])
            j += 1
    return updated_authors

def get_hottopics():
    resp = web.get('http://www.cc98.org/hottopic.asp')
    html = resp.content.decode('utf-8')

    url_p = re.compile('dispbbs\.asp\?boardid=\d+&id=\d+')
    title_p = re.compile('(?<=<font color=#000066>).+?(?=<\/font>)')
    section_p = re.compile(
        '<a href="list\.asp\?boardid=\d+" target="_blank">.+?<\/a>')
    author_p = re.compile(
        '<a href="dispuser\.asp\?name=.+?" target="_blank">.+?<\/a>')
    time_p = re.compile(
        '<span title=".+?">.+?</span>')

    urls = map(lambda x: 'http://www.cc98.org/'+x, url_p.findall(html))
    titles = title_p.findall(html)
    sections = section_p.findall(html)
    authors = author_p.findall(html)
    time = time_p.findall(html)

    sections = map(lambda x: x[x.index('>')+1:-4], sections)
    authors = map(lambda x: x[x.index('>')+1:-4], authors)
    time = map(lambda x: x[x.index('>')+1:-7], time)

    authors = fix_authors(authors, sections)
   
    subtitles = map(lambda x: u'板块: {0}    用户: {1}    时间: {2}'.format(*x),

        zip(sections, authors, time))

    return zip(titles, subtitles, urls)

def main(wf):
    try:
        max_age = int(sys.argv[1])
    except Exception:
        max_age = 30

    data = wf.cached_data('cc98', get_hottopics, max_age=max_age)

    for item in data:
        wf.add_item(item[0], item[1], arg=item[2], valid=True)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
