from pyspark import SparkContext
import markovify

sc = SparkContext("local[*]", "App Name")

def map_text_to_model(text):
    '''given an abstract, train a markov model'''
    return markovify.Text(text)


def combine_models(model1, weight1, model2, weight2):
    return markovify.combine([model1, model2], [weight1, weight2])

def split_line(line):
    """all_abracts.csv has file_name, abstract
    let's just grab abstracts for now"""
    strings = line.split(',')
    return strings[1]
    #return (strings[0], strings[1])

def extract_population(data_point):
    return (data_point[3], 1)

def add_pops(pop_pairA, pop_pairB):
    popA = pop_pairA[0]
    countA = pop_pairA[1]
    popB = pop_pairB[0]
    countB = pop_pairB[1]
    return (popA + popB, countA + countB)

abstracts = sc.textFile("./results/all_abstracts.csv")
abstracts = abstracts.map(split_line)
pop_pairs = abstracts.map(extract_population)
total_pop, total_count = pop_pairs.reduce(add_pops)

print("The average population is:")
print(total_pop/total_count)


# Get raw text as string.
with open("/path/to/my/corpus.txt") as f:
    text = f.read()

# # Print five randomly-generated sentences
# for i in range(5):
#     print(text_model.make_sentence())
#
# # Print three randomly-generated sentences of no more than 140 characters
# for i in range(3):
#     print(text_model.make_short_sentence(140))

