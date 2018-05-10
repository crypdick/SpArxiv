
import pandas


subjects = pandas.read_csv('all_subjects.csv', index_col=False, header=0)
#subjects.head(n=10)

abstract = pandas.read_csv('results/all_abstracts-RICHARD.csv')
#abstract.head(n=5)

#add another empty column
abstract["file_format"] = ""

#iterate through and input formated id's for the file
for index, row in abstract.iterrows():
    file = abstract.at[index,'file']
    #print(file)
    file_list = file.split("_")
    #print(file_list)
    try:
        formated = file_list[0] + "." + file_list[1]
    except IndexError:
        formated = ""
    #print(formated[0:10])
    abstract.set_value(index, 'file_format', formated[0:10])


#abstract.head(n=5)


#join abstracts and subjects
abstract.columns = ['old_file', 'abstract', 'file']
both  = abstract.join(subjects, lsuffix='file', rsuffix='file')


#both.head(n=5)


#only interested in old_file name and the subject
both.columns = ['old_file', 'abstract','id', 'delete', 'subject']
both_final = both[['old_file','id','abstract', 'subject']]
#both_final.head(n=5)


#write to csv when done
both_final.to_csv("results/abstract_bysub.csv", sep=',', index = False)

