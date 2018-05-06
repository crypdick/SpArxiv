from pyspark import SparkContext
import markovify

sc = SparkContext(appName='SparkSpeechGenereator')

STATE_SIZE = 2
SAVE_MODELS = True


def split_line(line):
    """all_abracts.csv has file_name, abstract
    let's just grab abstracts for now"""
    strings = line.split(',')
    try:
        return strings[1]
    except IndexError:  # there's some fuckery in our CSV
        pass
    #return (strings[0], strings[1])


def at_least_20_words(text):
    return len(text.split()) >= 20

def text_to_model(text):
    '''given an abstract, train a markov model

    the 1 will be used for weights, later'''
    return (markovify.Text(text, state_size=STATE_SIZE, retain_original=False), 1)


def combine_models(model1, weight1, model2, weight2):
    combined_model = markovify.combine([model1, model2], [weight1, weight2])
    combined_weight = weight1 + weight2
    return (combined_model, combined_weight)

def model_to_json(model):
    jsonified = model.to_json()
    if SAVE_MODELS:
        obj = open('model1.json', 'wb')
        obj.write(jsonified)
        obj.close


abstracts = sc.textFile("./results/all_abstracts.csv")
abstracts = abstracts.map(split_line)
abstracts = abstracts.filter(at_least_20_words)
# TODO strip out all latex code so that we have only English
models = abstracts.map(text_to_model)
models = models.reduce(combine_models)

# # Print five randomly-generated sentences
# for i in range(5):
#     print(text_model.make_sentence())
#
# # Print three randomly-generated sentences of no more than 140 characters
# for i in range(3):
#     print(text_model.make_short_sentence(140))

