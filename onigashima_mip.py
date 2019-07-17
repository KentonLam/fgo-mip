import json
from collections import defaultdict

from itertools import combinations, product

from gurobipy import * 

def onigashima():
    with open('onigashima_quests.json') as f:
        quests = json.load(f)
    for q in quests:
        del q['drops']['length']
        q['drops'] = list(q['drops'].values())

    coral = '/item/dragon-palace-coral'
    roll = '/item/roll-brocade'
    basket = '/item/onis-wicker-basket'

    CE_BONUSES = defaultdict(lambda: 0)
    CE_BONUSES[coral] = 3
    CE_BONUSES[roll] = 2
    CE_BONUSES[basket] = 2

    CRAFT_ESSENCES = [(coral, 1)]*3

    FRIEND_CES = [(coral, 2), (roll, 2), (basket, 1)]

    GOALS = {
        coral: 1500,
        roll: 2000,
        basket: 2400
    }

    HAVE = {
        coral: 3283,
        roll: 1530,
        basket: 2051
    }

    for k in HAVE.keys():
        GOALS[k] -= HAVE[k]

    item_names = set(i['item'] for q in quests for i in q['drops'])
    item_names = list(sorted(item_names))

    quest_names = [q['title'] for q in quests]
    
    quest_data = {q['title']: q for q in quests}
    m = Model('FGO')

    Y_C = list(combinations(
        range(len(CRAFT_ESSENCES)), min(5, len(CRAFT_ESSENCES))))
    F_C = range(len(FRIEND_CES))

    quest_costs = {(q['title'], )+y_c+(f_c,) : q['ap'] for q in quests for y_c in Y_C for f_c in F_C }

    Q = m.addVars(quest_names, Y_C, F_C, name='Quest', vtype=GRB.INTEGER, obj=quest_costs)
    I = m.addVars(item_names, name='Item', obj=0)
    m.update()
    bonuses = { 
        (y_c, f_c): {
            i: sum(CRAFT_ESSENCES[ce][1] for ce in y_c if CRAFT_ESSENCES[ce][0] == i) 
                + (FRIEND_CES[f_c][1] if FRIEND_CES[f_c][0] == i else 0)
            for i in item_names
        } for y_c in Y_C for f_c in F_C 
    }
    # print(bonuses)
    # print(Q.keys())

    for item in item_names:
        m.addConstr(I[item] == quicksum(
            Q[(q,)+y_c+(f_c,)] * quicksum(min(d['num']+bonuses[y_c,f_c][item], d['max'])*d['percent']/100 
                for d in quest_data[q]['drops'] if d['item'] == item)
        for q in quest_names
        for y_c in Y_C for f_c in F_C ))

    m.addConstrs(I[item] >= num for item, num in GOALS.items())

    m.setAttr(GRB.Attr.ModelSense, GRB.MINIMIZE)
    m.update()
    m.optimize()

    quest_perms = [(a,)+b+(c,) for a, b, c in product(quest_names, Y_C, F_C)]
    
    print('# Quests')
    runs = [ (round(Q[q].x), q) for q in quest_perms if Q[q].x]
    runs.sort(reverse=True)
    for n, q in runs:
        print(str(n).rjust(5), 'x ', q[0])
        print(' '*9, 'CEs:', ' '.join(str(CRAFT_ESSENCES[i]) for i in q[1:-1]))
        print(' '*9, 'Friend:', FRIEND_CES[q[-1]])
    print() 

    print('# Items')
    item_results = [ (round(I[i].x, 2), i) for i in item_names if I[i].x ]
    item_results.sort(reverse=True)
    for n, i in item_results:
        print(str(n).rjust(5), 'x ', i) 
        

if __name__ == "__main__":
    onigashima()