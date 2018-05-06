from pyspark import SparkContext
import markovify

sc = SparkContext("local[*]", "App Name")

STATE_SIZE = 2

def text_to_model(text):
    '''given an abstract, train a markov model

    the 1 will be used for weights, later'''
    return (markovify.Text(text, state_size=STATE_SIZE), 1)


def combine_models(model1, weight1, model2, weight2):
    combined_model = markovify.combine([model1, model2], [weight1, weighgstt2])
    combined_weight = weight1 + weight2
    return (combined_model, combined_weight)

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
models = abstracts.map(text_to_model)
models = models.reduce(combine_models)

# # Print five randomly-generated sentences
# for i in range(5):
#     print(text_model.make_sentence())
#
# # Print three randomly-generated sentences of no more than 140 characters
# for i in range(3):
#     print(text_model.make_short_sentence(140))

