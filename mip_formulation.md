# FGO Farming Optimisation 

Implemented as a MIP problem.

# Data 

```
q in Quests
i in Items
b in Bonuses, where b = {item: amount, ...}
g in Groups
GroupBonuses[g] = [b1, b2, ..., bn] (all possible bonuses in this group)
GroupMax[g] 
BonusCombinations[g][gid] = [b1, b2, ...] (selected bonuses in this group, in this gid)

TotalBonus[g][gid][i] (computed)

AP[q]
Drops[q][i] = [{num: , percent:}, ...]
Goals[i]
```

# Variables
```
X[q][gid1][gid2]...[gidn] = number of runs of quest q, with the identified bonuses.
Z[i] = total amount of item i
```

# Constraints
```
goals met 
Goals[i] <= Z[i] \forall i 

Z[i] = \sum_q \sum_{gid1...gidn} X[q][gid1][gid2]...[gidn] * \sum_{drop in Drops[q][i]} 
    drop[percent]*(drop[num]+\sum_{b in gid1...gidn if i in b} b[i])
```

# Objective 
```
\min  \sum_q \sum_{gid1...gidn} AP[q] * X[q][gid1][gid2]...[gidn]
```