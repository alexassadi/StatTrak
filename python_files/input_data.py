def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item

def get_headers(table):
    headers = []
    for i in table.find_all('th'):
        if 'col' in str(i):
            title = i.text
            headers.append(title)
    return headers
            
def get_stats(table):
    names = []
    stats = []
    
    body = table.find('tbody')
    
    for j in body.find_all('tr'):
        name = j.find('th')
        names.append(name.text)
        player = []
        for jj in j.find_all('td'):
            player.append(jj.text)
        stats.append(player)
            
    overall = list(zip(names,stats))
    return overall

def clean_data(overall,n,form):
    final = []
    if form == False:
        for player in overall:
            for i in player:
                final.append(i)
    elif form == True:
        for match in overall:
            if match[1][1] == 'Premier League':
                for i in match:
                    final.append(i)

    final = list(flatten(final))
    
    chunk = [final[x:x+n] for x in range(0, len(final), n)]
    
    chunks = []
    for i in chunk:
        if not '' in i:
            chunks.append(i)
        else:
            continue
    return chunks

def input_data(chunks,mydata):
    for i in chunks:
        length = len(mydata)
        mydata.loc[length] = i
    return mydata