"""
an example for using markovify without Spark
"""

import markovify


STATE_SIZE = 6
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
    if text is None:
        return False
    return len(text.split()) >= 20
    #except:  # for some reason we have some None's here
    #    pass


def text_to_model(text):
    '''given an abstract, train a markov model

    the 1 will be used for weights, later'''
    try:
        text_model = markovify.Text(text, state_size=STATE_SIZE, \
                                    retain_original=False)

        # class is not serializable, so extract json first
        # this makes a Text type object, so we coerce to str
        model_json = str(text_model.to_json())
        # TODO: change key for category
        return "_", model_json
    except:
        # TODO FIXME: many articles being lost due to illegal characters. see issue tracker.
        #print(text)
        pass



def combine_models(models_list):
    unzipped = zip(models_list)
    _ = []
    jsons = []
    for tup in unzipped:
        tup = tup[0]  # unnest 1 level
        if tup is None:
            continue  # FIXME I don't know how these Nonetypes keep sneaking in
        try:
            _name, json = tup
            jsons.append(json)
        except ValueError:
            print(tup)

    # reconstitute classes from json
    reconstituted_models = [markovify.Text.from_json(json_i) for json_i in jsons]

    # hella redundant but combine() method only smashes 2 models at a time
    combined_model = reconstituted_models.pop()
    weights = [1., 1.]
    for model in reconstituted_models:
        combined_model = markovify.combine([model, combined_model], weights)
        weights[-1] += 1
    combined_json = str(combined_model.to_json())
    # TODO: change key for category
    return "_", combined_json


def model_to_json(model):
    if SAVE_MODELS:
        model_name, model_json = model
        fname = open('./energy_physics_models/{}_model.json'.format(model_name), 'w')
        fname.write(model_json)
        fname.close

models = []
with open("./results/Energy_Physics_abstracts.csv") as abstracts:
    while len(models) < 5:
        for abstract in abstracts.readlines():
            print(len(models))
            abstract = split_line(abstract)
            #print(abstract)
            #if not abstract: # Nonetype
            #    continue
            if len(abstract) <= 20 or abstract is None:
                continue
            models.append(text_to_model(abstract))
            if len(models) > 5:
                break
    combined = combine_models(models)
    model_to_json(combined)
