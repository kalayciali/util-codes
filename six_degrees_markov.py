import pymysql

conn = pymysql.connect(host='localhost', user='phymat',
                       password='asd-123ASD', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute('USE wikipedia')

def getUrl(pageId):
    cur.execute('SELECT url FROM pages WHERE id = %s', (int(pageId)))
    return cur.fetchone()[0]

def getLinks(fromPageId):
    cur.execute('SELECT toPageId FROM links WHERE fromPageId = %s', (int(fromPageId)) )
    if cur.rowcount == 0:
        return []
    return [x[0] for x in cur.fetchall()]

def searchBreath(targetId, paths=[[1]]):
    newPaths = []
    for path in paths:
        links = getLinks(path[-1])
        for link in links:
            if link == targetId:
                return path + [link]
            else:
                newPaths.append(path+[link])
    print(newPaths)
    return searchBreath(targetId, newPaths)

nodes = getLinks(1)
targetId = 200
pageIds = searchBreath(targetId)
for pageId in pageIds:
    print(getUrl(pageId))
