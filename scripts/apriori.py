import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

df = pd.read_csv('./data/processed.csv')

def filter_df(df, questions):
    cols = [*df]
    selected = []
    for q in questions:
        #Get associated columns
        selected.extend([c for c in cols if c == q or c.startswith(q + '_')])
    return df[selected]

filtered = filter_df(df, ['Q3', 'Q5', 'Q8', 'Q9', 'Q10','Q11','Q16','Q30'])

#filtered = filter_df(df, ['Q23', 'Q24', 'Q25', 'Q26', 'Q27', 'Q28','Q29','Q30'])

df = filtered.copy()

print(df.head())

df = pd.get_dummies(df)

# Gera itens frequentes
print("Gerando itens frequentes...")
frequent_items = apriori(df, min_support=0.12, use_colnames=True)

print("Gerando regras de associação...")
# Regras de associação
rules = association_rules(frequent_items, metric='lift', min_threshold=0.8)
rules = rules.sort_values(by='lift', ascending=False)

print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_csv('./results/rules.csv', index=False)
