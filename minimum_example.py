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
    except KeyError:
        pass
    except TypeError:  # recieved Nonetype
        pass



def combine_models(model1_tup, model2_tup):
    try:
        _, model1_json, weight1 = model1_tup
    except TypeError:
        try:
            _, model2_json, weight2 = model2_tup
            return model2_tup
        except:
            return None
    # if model 1 but not model 2
    try:
        _, model2_json, weight2 = model2_tup
    except:
        return model1_tup

    # reconstitute classes from json
    magic_1, magic_2 = 0, 0
    if model1_json:  # catch Nonetypes
        model1 = markovify.Text.from_json(model1_json)
    else:
        magic_1 = 1
    if model2_json:
        model2 = markovify.Text.from_json(model2_json)
    else:
        magic_2 = 1

    if magic_1 + magic_2 == 2:
        pass
    elif magic_1 == 1:
        return "_", model1_json, weight1
    elif magic_2 == 1:
        return "_", model2_json, weight2


    combined_model = markovify.combine([model1, model2], [weight1, weight2])
    model_json = str(combined_model.to_json())
    combined_weight = weight1 + weight2
    print("combined weight: {}".format(combined_weight))
    # TODO: change key for category
    print("here")
    return "_", model_json, combined_weight


def model_to_json(model):
    if SAVE_MODELS:
        print("saved with count {}".format(model[2]))
        model_json = model[1]
        obj = open('model1.json', 'wb')
        obj.write(model_json)
        obj.close

old_model = ("", None, 0)
with open("./results/all_abstracts.csv") as abstracts:
    for abstract in abstracts.readlines():
        abstract = split_line(abstract)
        if not abstract: # Nonetype
            continue
        if len(abstract) <= 20:
            continue
        model = text_to_model(abstract)
        combined = combine_models(old_model, model)
        old_model = combined
    model_to_json(old_model)

# # Print five randomly-generated sentences
# for i in range(5):
#     print(text_model.make_sentence())
#
# # Print three randomly-generated sentences of no more than 140 characters
# for i in range(3):
#     print(text_model.make_short_sentence(140))
