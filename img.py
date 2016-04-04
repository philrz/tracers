import json

f = open('img.json', 'r')
o = json.load(f)
taglist = ['base']
depth = 0

for event in o:
    if event['evt.type'] == 'tracer':
        dir = event['evt.dir']
        info = event['evt.info'].split()
        tags = info[1].split('tags=')[1]
        print(dir + ' ' + tags)
        if dir == '>' and tags != taglist[-1]:
            taglist.append(tags)
            depth += 1
            print('push:' + tags + ' depth = ' + str(depth))
        elif dir == '<' and tags == taglist[-1]:
            print(' pop:' + tags + ' depth = ' + str(depth))
            taglist.pop()
            depth -= 1
        else:
            print('THIS SHOULD NEVER HAPPEN!')
f.close()
