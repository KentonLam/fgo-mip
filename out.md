# FGO MIP
```
Initialising quest data...
Computing optimal bonus configurations...
Academic license - for non-commercial use only
Adding model constraints...
CacheInfo(hits=28, misses=78, maxsize=None, currsize=78)
Optimize a model with 10 rows, 67 columns and 88 nonzeros
Variable types: 31 continuous, 36 integer (0 binary)
Coefficient statistics:
  Matrix range     [1e+00, 2e+02]
  Objective range  [1e+01, 4e+01]
  Bounds range     [0e+00, 0e+00]
  RHS range        [9e+02, 1e+03]
Found heuristic solution: objective 2350.0000000
Presolve removed 5 rows and 42 columns
Presolve time: 0.00s
Presolved: 5 rows, 25 columns, 54 nonzeros
Variable types: 0 continuous, 25 integer (0 binary)

Root relaxation: objective 1.340490e+03, 5 iterations, 0.00 seconds

    Nodes    |    Current Node    |     Objective Bounds      |     Work
 Expl Unexpl |  Obj  Depth IntInf | Incumbent    BestBd   Gap | It/Node Time

     0     0 1340.49042    0    5 2350.00000 1340.49042  43.0%     -    0s
H    0     0                    1380.0000000 1340.49042  2.86%     -    0s
     0     0 1351.18181    0    6 1380.00000 1351.18181  2.09%     -    0s
     0     0 1353.22848    0    7 1380.00000 1353.22848  1.94%     -    0s
     0     0 1354.65978    0    7 1380.00000 1354.65978  1.84%     -    0s
     0     0 1356.38289    0    7 1380.00000 1356.38289  1.71%     -    0s
     0     0 1356.79966    0    8 1380.00000 1356.79966  1.68%     -    0s
     0     0 1357.07836    0    8 1380.00000 1357.07836  1.66%     -    0s
     0     0 1357.15320    0    9 1380.00000 1357.15320  1.66%     -    0s
     0     0 1358.36279    0    8 1380.00000 1358.36279  1.57%     -    0s
     0     0 1358.78018    0    8 1380.00000 1358.78018  1.54%     -    0s
     0     0 1358.86289    0    8 1380.00000 1358.86289  1.53%     -    0s
     0     0 1359.08291    0    8 1380.00000 1359.08291  1.52%     -    0s
     0     0 1359.20598    0    8 1380.00000 1359.20598  1.51%     -    0s
     0     2 1359.20598    0    8 1380.00000 1359.20598  1.51%     -    0s

Cutting planes:
  Gomory: 1
  MIR: 6

Explored 16 nodes (68 simplex iterations) in 0.03 seconds
Thread count was 4 (of 4 available processors)

Solution count 2: 1380 2350 

Optimal solution found (tolerance 1.00e-04)
Best objective 1.380000000000e+03, best bound 1.380000000000e+03, gap 0.0000%
```
## Quest Runs
### 2 x private-beach-novice (Beach)
**Total bonus:** {'/item/fresh-water': 10, '/item/food': 4, '/item/lumber': 2}
| servants | ces | sup serv | sup ce |
| --- | --- | --- | --- |
| fresh-water+1 | food+2
fresh-water+2 | fresh-water+1 | food+2
fresh-water+2 |
| fresh-water+1 | lumber+1 |  |  |
| fresh-water+1 | lumber+1 |  |  |
| fresh-water+1 |  |  |  |
| fresh-water+1 |  |  |  |

### 4 x private-beach-storm (Beach)
**Total bonus:** {'/item/fresh-water': 10, '/item/food': 4, '/item/lumber': 2}
| servants | ces | sup serv | sup ce |
| --- | --- | --- | --- |
| fresh-water+1 | food+2
fresh-water+2 | fresh-water+1 | food+2
fresh-water+2 |
| fresh-water+1 | lumber+1 |  |  |
| fresh-water+1 | lumber+1 |  |  |
| fresh-water+1 |  |  |  |
| fresh-water+1 |  |  |  |

### 5 x mystery-zone-storm (Primeval Forest)
**Total bonus:** {'/item/food': 10, '/item/fresh-water': 4, '/item/lumber': 2}
| servants | ces | sup serv | sup ce |
| --- | --- | --- | --- |
| food+1 | food+2
fresh-water+2 | food+1 | food+2
fresh-water+2 |
| food+1 | lumber+1 |  |  |
| food+1 | lumber+1 |  |  |
| food+1 |  |  |  |
| food+1 |  |  |  |

### 7 x picnic-field-storm (Grasslands)
**Total bonus:** {'/item/stone': 8, '/item/food': 2, '/item/fresh-water': 2, '/item/lumber': 2}
| servants | ces | sup serv | sup ce |
| --- | --- | --- | --- |
| stone+1 | food+2
fresh-water+2 | stone+1 | stone+2 |
| stone+1 | lumber+1 |  |  |
| stone+1 | lumber+1 |  |  |
| stone+1 |  |  |  |
| stone+1 |  |  |  |

### 9 x jungle-adventure-storm (Jungle)
**Total bonus:** {'/item/lumber': 10, '/item/food': 2, '/item/fresh-water': 2}
| servants | ces | sup serv | sup ce |
| --- | --- | --- | --- |
| lumber+1 | food+2
fresh-water+2 | lumber+1 | lumber+2 |
| lumber+1 | lumber+1 |  |  |
| lumber+1 | lumber+1 |  |  |
| lumber+1 |  |  |  |
| lumber+1 |  |  |  |

### 9 x romantic-cave-storm (Cave)
**Total bonus:** {'/item/iron': 8, '/item/food': 2, '/item/fresh-water': 2, '/item/lumber': 2}
| servants | ces | sup serv | sup ce |
| --- | --- | --- | --- |
| iron+1 | food+2
fresh-water+2 | iron+1 | iron+2 |
| iron+1 | lumber+1 |  |  |
| iron+1 | lumber+1 |  |  |
| iron+1 |  |  |  |
| iron+1 |  |  |  |

Z
[(1482.2000000000003, '/item/food'),
 (1360.8000000000002, '/item/lumber'),
 (1188.0, '/item/iron'),
 (1144.4, '/item/fresh-water'),
 (924.0, '/item/stone')]

Total AP: 1380.0
