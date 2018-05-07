from pyspark import SparkContext
import markovify

sc = SparkContext(appName='SparkSpeechGenereator')

STATE_SIZE = 4
SAVE_MODELS = True
ABSTRACTS_FILE = "./results/all_abstracts-RICHARD.csv"

def clean_text_for_markovify(text):
    '''
    Markovify has a few symbols it hates. we'll filter them
    https://github.com/jsvine/markovify/blob/master/markovify/text.py#L104
    '''
    text = text.replace("'", "").replace('"', "").replace("(", "")\
        .replace(")", "").replace("[", "").replace("]", "")
    return text


def split_line(line):
    """all_abracts.csv has file_name, abstract
    let's just grab abstracts for now"""
    try:
        strings = line.split(',', 1)
        # TODO: return category of the text
        return str(strings[1])
    except:
        print("line skipped in split_line")
        pass

def combine_abstract_text(text1, text2):
    """markovify works best when each corpus is a single huge string. theefore,
    reduce by key here"""
    return text1+text2

def text_to_model(text):
    '''given an abstract, train a markov model

    the 1 will be used for weights, later'''
    try:
        # retain_original set to False to save lots of RAM
        text_model = markovify.Text(text, state_size=STATE_SIZE, \
                                    retain_original=False)

        # class is not serializable, so extract json first
        # this makes a Text type object, so we coerce to str
        model_json = str(text_model.to_json())
        # TODO: change key for category
        return "_", model_json
    except:
        # TODO FIXME: many articles being lost due to illegal characters. see issue tracker.
        print("model skipped in text_to_model:", text)
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
    #weights = [1., 1.]
    for model in reconstituted_models:
        combined_model = markovify.combine([model, combined_model]) #, weights)
        #weights[-1] += 1
    combined_json = str(combined_model.to_json())
    # TODO: change key for category
    return "_", combined_json


def model_to_json(_, model):
    try:
        model_name, model_json = model
    except TypeError:  # TODO FIXME somehow STILL Nonetypes leaking through
        return None
    if SAVE_MODELS:
        fname = open('./models/{}_model.json'.format(model_name), 'w')
        fname.write(model_json)
        fname.close


abstracts = sc.textFile(ABSTRACTS_FILE)
abstracts = abstracts.map(clean_text_for_markovify)
abstracts = abstracts.map(split_line)
abstracts = abstracts.filter(lambda text: text is not None)
abstracts = abstracts.filter(lambda text: len(text) >= 12)
print(abstracts.take(1))
abstracts = abstracts.reduce(combine_abstract_text)
print(abstracts.take(1))
models = abstracts.map(text_to_model)
combine_models = models.reduceByKey(combine_models)
models.map(model_to_json)

