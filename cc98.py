#!/usr/bin/python
# encoding: utf-8

import sys
import re
from workflow import Workflow, web

def fix_authors(authors, boards):
    j = 0
    updated_authors = []
    for i in xrange(len(boards)):
        if boards[i] == u'心灵之约':
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
    board_p = re.compile(
        '<a href="list\.asp\?boardid=\d+" target="_blank">.+?<\/a>')
    author_p = re.compile(
        '<a href="dispuser\.asp\?name=.+?" target="_blank">.+?<\/a>')
    time_p = re.compile(
        '<span title=".+?">.+?</span>')

    urls = map(lambda x: 'http://www.cc98.org/'+x, url_p.findall(html))
    titles = title_p.findall(html)
    boards = map(lambda x: x[x.index('>')+1:-4], board_p.findall(html))
    authors = map(lambda x: x[x.index('>')+1:-4], author_p.findall(html))
    time = map(lambda x: x[x.index('>')+1:-7], time_p.findall(html))

    authors = fix_authors(authors, boards)
   
    subtitles = map(lambda x:
            u'板块: {board:<20} 作者: {author:<20} 时间: {time:<20}'.format(
                board=x[0],
                author=x[1],
                time=x[2]),
            zip(boards, authors, time))

    return zip(titles, subtitles, urls)

def main(wf):
    data = wf.cached_data('cc98', get_hottopics)
    for title, subtitle, url in data:
        wf.add_item(title, subtitle, arg=url, valid=True)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
