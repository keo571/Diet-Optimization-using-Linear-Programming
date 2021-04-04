#!/usr/bin/env python
# coding: utf-8

# The diet problem is one of the first large-scale optimization problems to be studied in practice. Back in the 1930’s and 40’s, the Army wanted to meet the nutritional
# requirements of its soldiers while minimizing the cost.) 
# 
# 1. Formulate an optimization model (a linear program) to find the cheapest diet that satisfies the maximum and minimum daily nutrition constraints, and solve it using PuLP.

# In[29]:


from pulp import *
import pandas as pd

df = pd.read_excel(r'diet.xls')
diet = df[:64]
lowbounds = df.iloc[65, 3:]
upbounds = df.iloc[66, 3:]

# Create a list of the foods
foods = list(diet['Foods'])    
    
# Crate a dictionary for the costs of each of the foods
costs = pd.Series(list(diet['Price/ Serving']), index=foods).to_dict()

# Craet a list of dictionaries of each nutrition ingredient
nutrition = [pd.Series(list(diet[col]), index=foods).to_dict()for col in diet.columns[3:]]

# Crate the 'prob' variable to contain the problem data
prob = LpProblem('The_Diet_Problem', LpMinimize)
    
# Crate a dictionary called 'food_vars' to contain the referenced variables
food_vars = LpVariable.dicts("amount",foods, 0)

# The objective function is added to 'prob' first
prob += lpSum([costs[i]*food_vars[i] for i in foods]) 

# The constraints are added to 'prob'
for i in range(len(nutrition)):
    prob += lpSum([nutrition[i][j] * food_vars[j] for j in foods]) <= upbounds[i] 
    prob += lpSum([nutrition[i][j] * food_vars[j] for j in foods]) >= lowbounds[i]
    
# The problem data is written to an .lp file
prob.writeLP("DietModel.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# The selected variables is printed with it's resolved optimum value
for v in prob.variables():
    if v.varValue != 0:
        print(v.name, "=", v.varValue)

# The optimised objective function value is printed   
print("Total Cost of the diet =", value(prob.objective))


# 2. Add the following constraints (which might require adding more variables) and solve the new model:
# 
#     a. If a food is selected, then a minimum of 1/10 serving must be chosen. (Hint: now you will need two variables for each food i: whether it is chosen, and how much is part of the diet. You’ll also need to write a constraint to link them.)
# 
#     b. Many people dislike celery and frozen broccoli. So at most one, but not both, can be selected.
# 
#     c. To get day-to-day variety in protein, at least 3 kinds of meat/poultry/fish/eggs must be selected. 

# In[30]:


# Create two variables 'chosen' and 'size'
chosen = LpVariable.dicts("chosen", foods, cat='Binary')
size = LpVariable.dicts("size", foods, lowBound=0)

# Crate the 'prob2' variable to contain the problem data
prob2 = LpProblem('The_Diet_Problem2', LpMinimize)

# The objective function is added to 'prob2' first 
prob2 += lpSum([costs[i]*size[i] for i in foods]) 

meat = ['Roasted Chicken', 'Poached Eggs', 'Scrambled Eggs', 'Bologna,Turkey', 'Frankfurter, Beef', 
        'Ham,Sliced,Extralean', 'Kielbasa,Prk', 'Pork', 'Sardines in Oil', 'White Tuna in Water']

# The constraints are added to 'prob2'
for i in range(len(nutrition)):    
    prob2 += lpSum([nutrition[i][j] * size[j] for j in foods]) <= upbounds[i] 
    prob2 += lpSum([nutrition[i][j] * size[j] for j in foods]) >= lowbounds[i]

# M is the maximum serving size
M = 100
for j in foods:
    prob2 += size[j] >= chosen[j]*0.1
    prob2 += size[j] <= chosen[j]*M

prob2 += chosen['Frozen Broccoli'] + chosen['Celery, Raw'] <= 1

prob2 += lpSum([chosen[m] for m in meat]) >= 3

# The problem data is written to an .lp file
prob2.writeLP("DietModel.lp")

# The problem is solved using PuLP's choice of Solver
prob2.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob2.status])

# The selected variables is printed with it's resolved optimum value
for v in prob2.variables():
    if v.varValue != 0:
        print(v.name, "=", v.varValue)
        
# The optimised objective function value is printed   
print("Total Cost of the diet =", value(prob2.objective))


# Solving the models for the file diet_large.xls, which is a low-cholesterol diet model (rather than minimizing cost, the goal is to minimize cholesterol intake).

# In[31]:


df_large = pd.read_excel(r'diet_large.xls').fillna(0)
diet_large = df_large[:7145]
lowbounds = df_large.iloc[7147, 1:28]
upbounds = df_large.iloc[7149, 1:28]

foods = list(diet_large['Long_Desc'])    
cholesterol = pd.Series(list(diet_large['Cholesterol']), index=foods).to_dict()
nutrition = [pd.Series(list(diet_large[col]), index=foods).to_dict()for col in diet_large.columns[1:28]]

prob3 = LpProblem('The_Cholesterol_Problem', LpMinimize)
food_vars = LpVariable.dicts("amount",foods, 0)

prob3 += lpSum([cholesterol[i]*food_vars[i] for i in foods]) 

for i in range(len(nutrition)):
    prob3 += lpSum([nutrition[i][j] * food_vars[j] for j in foods]) <= upbounds[i] 
    prob3 += lpSum([nutrition[i][j] * food_vars[j] for j in foods]) >= lowbounds[i]
    
prob3.writeLP("CholesterolModel.lp")
prob3.solve()

print("Status:", LpStatus[prob3.status])

for v in prob3.variables():
    if v.varValue != 0:
        print(v.name, "=", v.varValue)

print("Total Cholesterol of the diet =", value(prob3.objective))

