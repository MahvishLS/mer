from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

model = DiscreteBayesianNetwork([
    ('EmailSource', 'ContainsLink'),
    ('EmailSource', 'Spam'),
    ('ContainsLink', 'Spam')
])

cpd_source = TabularCPD(variable='EmailSource', variable_card=2, values=[[0.8], [0.2]])

cpd_link = TabularCPD(
    variable='ContainsLink', variable_card=2,
    values=[[0.9, 0.3], 
            [0.1, 0.7]],
    evidence=['EmailSource'],
    evidence_card=[2]
)

cpd_spam = TabularCPD(
    variable='Spam', variable_card=2,
    values=[
        [0.95, 0.6, 0.3, 0.1],  
        [0.05, 0.4, 0.7, 0.9]  
    ],
    evidence=['EmailSource', 'ContainsLink'],
    evidence_card=[2, 2]
)

model.add_cpds(cpd_source, cpd_link, cpd_spam)

print("Model valid?", model.check_model())
# Query: What's the probability email is from suspicious source given it's spam?
posterior_source = infer.query(variables=['EmailSource'], evidence={'Spam': 1})
print("\nProbability EmailSource given Spam=True:")
print(posterior_source)

# Query
posterior_link = infer.query(variables=['ContainsLink'], evidence={'Spam': 1, 'EmailSource': 0})
print("\nProbability ContainsLink given Spam=True:")
print(posterior_link)
