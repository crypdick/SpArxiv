import pandas

abstract = pandas.read_csv('results/abstract_bysub.csv')

format = pandas.read_csv('results/all_abstracts-RICHARD.csv')
#abstract.head(n=5)

#format.head(n=5)


#find top occuring 
abstract['subject'].value_counts()

#Cryptography and Security (cs.CR)
crypto = abstract[abstract['subject']== 'Cryptography and Security (cs.CR)'] 
crypto = crypto[['old_file','abstract']]
#crypto.head(n=5)
#len(crypto.index) 99
crypto.to_csv("results/crypto_abstracts.csv", sep=',', index = False)

#Distributed, Parallel, and Cluster Computing (cs.DC)
Dist = abstract[abstract['subject']== 'Distributed, Parallel, and Cluster Computing (cs.DC)']
Dist = Dist[['old_file','abstract']]
#Dist.head(n=5)
#len(Dist.index) 124
Dist.to_csv("results/Dist_abstracts.csv", sep=',', index = False)


#High Energy Physics - Phenomenology (hep-ph)
Energy_Physics = abstract[abstract['subject']== 'High Energy Physics - Phenomenology (hep-ph)']
Energy_Physics = Energy_Physics[['old_file','abstract']]
#Energy_Physics.head(n=5)
#len(Energy_Physics.index) 144
Energy_Physics.to_csv("results/Energy_Physics_abstracts.csv", sep=',', index = False)


#Numerical Analysis (math.NA) 
Num_anal = abstract[abstract['subject']== 'Numerical Analysis (math.NA)']
Num_anal = Num_anal[['old_file','abstract']]
#Energy_Physics.head(n=5)
#len(Num_anal.index) 102
Num_anal.to_csv("results/Num_anal_abstracts.csv", sep=',', index = False)

#Machine Learning (stat.ML)
machine_learn = abstract[abstract['subject']== 'Machine Learning (stat.ML)']
machine_learn = machine_learn[['old_file','abstract']]
#machine_learn.head(n=5)
#len(machine_learn.index) 68
machine_learn.to_csv("results/machine_learn_abstracts.csv", sep=',', index = False)