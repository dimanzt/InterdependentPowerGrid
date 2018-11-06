start_node = dict(state='2011001100110011', row=0, col=0, prev=None);
target_state = '2101101001011010'

def swap(state, r1, c1, r2, c2):
    m, n = list(sorted([r1 * 4 + c1, r2 * 4 + c2]))
    return state[:m] + state[n] + state[m+1:n] + state[m] + state[n+1:]

q = [start_node]
visited = set(start_node['state'])
qi = 0
while qi < len(q):
    cur = q[qi]
    qi += 1
    s, r, c = cur['state'], cur['row'], cur['col']

    if s == target_state:
        def trace(node):
            if node['prev'] != None:
                trace(node['prev'])
            else:
                return
            r1, c1 = node['prev']['row'], node['prev']['col']
            r2, c2 = node['row'], node['col']
            if r2 == r1 - 1:
                print 'U',
            elif r2 == r1 + 1:
                print 'D',
            elif c2 == c1 - 1:
                print 'L',
            else:
                print 'R',

        trace(cur)
        break

    def move(row, col):
        if row >= 0 and row < 4 and col >= 0 and col < 4:
            state = swap(s, r, c, row, col)
            if state not in visited:
                visited.add(state)
                q.append(dict(state=state, row=row, col=col, prev=cur))

    move(r - 1, c)
    move(r + 1, c)
    move(r, c - 1)
    move(r, c + 1)


