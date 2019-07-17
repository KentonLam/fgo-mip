from gurobipy import * 

import json 
from pprint import pprint
from itertools import combinations, zip_longest
from collections import defaultdict
from functools import lru_cache



def optimise_quests(quests_file, goals, bonuses, all_items=False):
    with open(quests_file) as f:
        quest_data = json.load(f)
    
    print('# FGO MIP')
    print('```')

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

    @lru_cache(None)
    def compute_group_bonuses(bonus_list):
        total = {}
        for bonus in bonus_list:
            for i, amt in bonus:
                if i not in total: total[i] = 0 
                total[i] += amt 
        return total

    combs_set = lru_cache(None)(lambda g, r: set(tuple(sorted(c)) 
                for c in combinations(GroupBonuses[g], r)))

    OptimalBonus = {}
    OptimalBonusAmounts = {}
    TotalQuestBonus = {}
    print('Computing optimal bonus configurations...')
    for q in Quests:
        dropped_items = {}
        for item, drops in Drops[q].items():
            if item not in dropped_items:
                dropped_items[item] = 0 
            for d in drops:
                dropped_items[d['item']] += d['percent']*d['num'] / 100
        priority = sorted(dropped_items.keys(), key=lambda k: dropped_items[k])
        priority = list(priority)
        # pprint(priority)

        OptimalBonus[q] = {}
        OptimalBonusAmounts[q] = {}
        for g in Groups:
            r = min(len(GroupBonuses[g]), GroupMax[g])
            combs = combs_set(g, r)
            dropped_set = set(priority)
            combs = [c for c in combs if set(compute_group_bonuses(c)) ^ (dropped_set)]
            for item in priority:
                combs.sort(key=lambda c: compute_group_bonuses(c).get(item, 0))
            OptimalBonus[q][g] = combs[-1]
            OptimalBonusAmounts[q][g] = compute_group_bonuses(combs[-1])
            # pprint(combs[-1])
        
        TotalQuestBonus[q] = {}
        for g, bonus in OptimalBonusAmounts[q].items():
            for i, amt in bonus.items():
                if i not in TotalQuestBonus[q]: TotalQuestBonus[q][i] = 0 
                TotalQuestBonus[q][i] += amt
    # pprint(BonusCombinations)
    # pprint(TotalBonus)
    # pprint(GIDs)

    m = Model('FGO')
    X = m.addVars(Quests, name='X', obj=AP, vtype=GRB.INTEGER)
    Z = m.addVars(Items, name='Z')

    @lru_cache(None)
    def quest_bonus(q, i):
        return sum(OptimalBonusAmounts[q][g].get(i, 0) for g in Groups)

    print('Adding model constraints...')
    for i in Items:
        if not (i in goals or all_items): continue
        # print(i)
        m.addConstr(Z[i] == quicksum( 
            X[q] * sum(
                d['percent']/100*(
                    d['num'] + quest_bonus(q, i))
                for d in Drops[q].get(i, ()) )
            for q in X))
    print(quest_bonus.cache_info())

    m.addConstrs(Z[i] >= goals[i] for i in goals)

    m.setAttr(GRB.Attr.ModelSense, GRB.MINIMIZE)
    # m.setParam(GRB.Attr.MIPGap, 0.9/100)
    # m.write('model.lp')
    m.optimize()
    print('```')

    def format_bonus(bonus, sep=' '):
        s = []
        for mat, amt in bonus:
            s.append(mat.replace('/item/', '') + f'+{amt}')
        return sep.join(s)


    def format_groups(group_bonuses):
        out = []
        for bonus in group_bonuses:
            out.append(format_bonus(bonus))
        return ' | '.join(out)

    def print_quest_details(q):
        print('###', int(X[q].x), f'x {q} ({Quests[q]["location"]})')
        print('**Total bonus:**', TotalQuestBonus[q])
        print('|', ' | '.join(Groups), '|')
        print('|', ' | '.join(('---', )*len(Groups)), '|')
        for bonus_row in zip_longest(*OptimalBonus[q].values()):
            print(
                '|', 
                ' | '.join(
                    format_bonus(b, '\n') if b else '' for b in bonus_row),
                '|')



    print('## Quest Runs')
    optimal_quests = [(X[q].x, q) for q in X if X[q].x]
    optimal_quests.sort()
    for _, q in optimal_quests:
        print_quest_details(q)
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
        iron: 1500-331,
        stone: 1500-581,
        food: 2700-1225,
        water: 2700-1568,
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