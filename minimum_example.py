import markovify


STATE_SIZE = 2  # TODO: raise this once we are near the end
SAVE_MODELS = True


def split_line(line):
    """all_abracts.csv has file_name, abstract
    let's just grab abstracts for now"""
    try:
        strings = line.split(',', 1)
        return str(strings[1])
    except:
        pass


def at_least_20_words(text):
    try:
        return len(text.split()) >= 20
    except:  # for some reason we have some None's here
        pass


def text_to_model(text):
    '''given an abstract, train a markov model

    the 1 will be used for weights, later'''
    try:
        text_model = markovify.Text(text, state_size=STATE_SIZE)

        # class is not serializable, so extract json first
        # this makes a Text type object, so we coerce to str
        model_json = str(text_model.to_json())
        # TODO: change key for category
        return "_", model_json, 1
    #except KeyError:
    #l    pass
    except TypeError:  # recieved Nonetype
        pass



def combine_models(models_list):
    _, jsons, weights = [list(a) for a in zip(models_list)]

    # reconstitute classes from json
    reconstituted_models = [markovify.Text.from_json(json_i) for json_i in jsons]

    combined_model = markovify.combine([reconstituted_models], [weights])
    combined_json = str(combined_model.to_json())
    combined_weights = sum(weights)
    print("combined weight: {}".format(combined_weights))
    # TODO: change key for category
    return "_", combined_json, combined_weights


def model_to_json(model):
    if SAVE_MODELS:
        print("saved with count {}".format(model[2]))
        model_json = model[1]
        obj = open('model1.json', 'wb')
        obj.write(model_json)
        obj.close

models = []
with open("./results/all_abstracts-RICHARD.csv") as abstracts:
    count = 1
    for abstract in abstracts.readlines():
        abstract = split_line(abstract)
        if not abstract: # Nonetype
            continue
        if len(abstract) <= 20:
            continue
        models.append(text_to_model(abstract))
    combined = combine_models(models)
    model_to_json(old_model)

# # Print five randomly-generated sentences
# for i in range(5):
#     print(text_model.make_sentence())
#
# # Print three randomly-generated sentences of no more than 140 characters
# for i in range(3):
#     print(text_model.make_short_sentence(140))
