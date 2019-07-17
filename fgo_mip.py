from gurobipy import * 

import json 
from pprint import pprint
from itertools import combinations
from collections import defaultdict
from functools import lru_cache



def optimise_quests(quests_file, goals, bonuses, all_items=False):
    with open(quests_file) as f:
        quest_data = json.load(f)
    
    AP = {}
    Quests = {}
    Drops = {}
    Items = set()
    print('Initialising quest data...')
    for q in quest_data:
        assert q['title'] not in Quests
        Quests[q['title']] = q 
        AP[q['title']] = q['ap']
        Drops[q['title']] = drops = {}
        for drop in q['drops']:
            if drop['item'] not in drops:
                drops[drop['item']] = []
            drops[drop['item']].append(drop)
            Items.add(drop['item'])
    # pprint(Drops)
    
    GroupBonuses = {}
    GroupMax = {}
    Groups = tuple(bonuses.keys())
    for g, (limit, bonuses) in bonuses.items():
        GroupMax[g] = limit 
        GroupBonuses[g] = tuple(tuple(sorted(b.items())) for b in bonuses)

    BonusCombinations = {}
    TotalBonus = {}
    GIDs = []
    print('Enumerating bonus combinations...')
    for g in Groups:
        BonusCombinations[g] = {}
        TotalBonus[g] = {}
        r = min(len(GroupBonuses[g]), GroupMax[g])
        combs = set(tuple(sorted(c)) 
            for c in combinations(GroupBonuses[g], r))
        gid = 0
        for comb in combs:
            TotalBonus[g][gid] = {}
            BonusCombinations[g][gid] = comb 
            for bonus in comb:
                for item, amount in bonus:
                    if item not in TotalBonus[g][gid]:
                        TotalBonus[g][gid][item] = 0
                    TotalBonus[g][gid][item] += amount
            gid += 1
        GIDs.append(list(range(gid)))
    # pprint(BonusCombinations)
    # pprint(TotalBonus)
    # pprint(GIDs)

    class APShim(dict):
        def get(self, x, default=None):
            return AP[x[0]]

    m = Model('FGO')
    X = m.addVars(Quests, *GIDs, name='X', obj=APShim(), vtype=GRB.INTEGER)
    Z = m.addVars(Items, name='Z')

    @lru_cache(None)
    def gids_bonus(i, gids):
        return sum(TotalBonus[g][gid].get(i, 0) 
            for g, gid in zip(Groups, gids))

    print('Adding model constraints...')
    for i in Items:
        if not (i in goals or all_items): continue
        # print(i)
        m.addConstr(Z[i] == quicksum( 
            X[q_gids] * sum(
                d['percent']/100*(
                    d['num'] + gids_bonus(i, q_gids[1:]))
                for d in Drops[q_gids[0]].get(i, ()) )
            for q_gids in X))
    print(gids_bonus.cache_info())

    m.addConstrs(Z[i] >= goals[i] for i in goals)

    m.setAttr(GRB.Attr.ModelSense, GRB.MINIMIZE)
    m.setParam(GRB.Attr.MIPGap, 0.9/100)
    # m.write('model.lp')
    m.optimize()

    def format_gids(g, gid):
        out = []
        for bonus in BonusCombinations[g][gid]:
            s = []
            for mat, amt in bonus:
                s.append(mat.replace('/item/', '') + f'+{amt}')
            out.append(' '.join(s))
        return ' | '.join(out)

    def print_q_gids(q_gids):
        q, *gids = q_gids
        print(str(int(X[q_gids].x)).rjust(3)+f' x {q} ({Quests[q]["location"]})')
        print('      total bonus:', 
            {i: gids_bonus(i, tuple(gids)) for i in Items if gids_bonus(i, tuple(gids))})
        for g, gid in zip(Groups, gids):
            print(f'      {g}:', format_gids(g, gid))



    print('X')
    optimal_quests = [(X[q_g].x, q_g) for q_g in X if X[q_g].x]
    optimal_quests.sort()
    for _, q_g in optimal_quests:
        print_q_gids(q_g)
        print()
    print('Z')
    total_drops = [(Z[i].x, i) for i in Items if Z[i].x]
    total_drops.sort(reverse=True)
    pprint(total_drops)
    print()
    print('Total AP:', m.objVal)

def main():
    water = '/item/fresh-water'
    food = '/item/food'
    wood = '/item/lumber'
    stone = '/item/stone'
    iron = '/item/iron'
    
    GOALS = {
        iron: 1500-223,
        stone: 1500-5,
        food: 2700-1117,
        water: 2700-1536,
        wood: 2800-1512,
    }

    SHOP_CE = {water: 2, food: 2}
    WOOD_CE = {wood: 1}
    STONE_CE = {stone: 1}
    IRON_CE = {iron: 1}

    SERVANTS = []
    for i in (water, food, wood, stone, iron):
        SERVANTS.extend(({i:1}, )*5)
    SERVANTS = tuple(SERVANTS)

    

    Bonuses = {
        'servants': (5, SERVANTS),
        'ces': (5, (SHOP_CE, WOOD_CE, WOOD_CE)),
        'sup serv': (1, SERVANTS),
        'sup ce': (1, ({water: 2, food: 2}, {wood: 2}, {stone: 2}, {iron: 2})),
    }
    
    optimise_quests('summer1_quests.json', 
        GOALS, Bonuses)

if __name__ == "__main__":
    main()