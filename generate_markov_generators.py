from pyspark import SparkContext
import markovify

sc = SparkContext("local[*]", "App Name")

def split_line(line):
    strings = line.split(',')
    return (strings[0], strings[1], int(strings[2]), int(strings[3]))

def extract_population(data_point):
    return (data_point[3], 1)

def add_pops(pop_pairA, pop_pairB):
    popA = pop_pairA[0]
    countA = pop_pairA[1]
    popB = pop_pairB[0]
    countB = pop_pairB[1]
    return (popA + popB, countA + countB)

line_set = sc.textFile("./states.csv")
split_lines = line_set.map(split_line)
pop_pairs = split_lines.map(extract_population)
total_pop, total_count = pop_pairs.reduce(add_pops)

print("The average population is:")
print(total_pop/total_count)


# Get raw text as string.
with open("/path/to/my/corpus.txt") as f:
    text = f.read()

# Build the model.
text_model = markovify.Text(text)

# Print five randomly-generated sentences
for i in range(5):
    print(text_model.make_sentence())

# Print three randomly-generated sentences of no more than 140 characters
for i in range(3):
    print(text_model.make_short_sentence(140))

# combinging models
model_a = markovify.Text(text_a)
model_b = markovify.Text(text_b)

model_combo = markovify.combine([ model_a, model_b ], [ 1.5, 1 ])