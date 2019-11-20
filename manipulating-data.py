import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# list respondents who gave fake answers.
# They have to be removed from the analysis in order not to skew the results
blacklisted_emails = [
    'CleanYourData@Hal3anneh.com',
    'nope@hotmail.com',
    'eyePISSEDandFARDEDandSHIDDEDandCAMEallOVERthePLACE@lmao.pwned.com',
]


def analysis():
    raw_survey = pd.read_csv('./data/condensed.actual.csv')
    # 17 is the index of the email column
    survey_responses = raw_survey.iloc[1:, list(range(9, 17))]
    questions = survey_responses.columns
    # print(type(questions))
    # print(questions[0])
    # questions[7] contains GPAs
    points=[]
    for i in range(len(survey_responses)):
        survey_responses.iloc[i,7] = float(survey_responses.iloc[i,7])
    # points = [None]+survey_responses.iloc[:,7]
    # print(points)
    plt.plot(survey_responses[questions[7]],'ro')
    plt.show()

# Do not run this function if you have already generated those two files because
# it will overwrite them.
def write_csv_files():
    raw_data = pd.read_csv('./data/condensed.actual.csv')
    emails = pd.DataFrame(raw_data.iloc[1:, 17])
    survey_answers = raw_data.iloc[1:, list(range(9, 17))]
    emails.to_csv('./data/emails.csv', index=None, header=True)
    survey_answers.to_csv('./data/questions.only.csv',
                          index=None, header=True)



analysis()
exit(0)

graph = {
    1: 25,
    3: 4,
    10: 10
}
x = []
y = []
for key in graph.keys():
    x.append(key)
    y.append(graph[key])

print(x)
print(y)

plt.plot(x,y,'ro')
plt.show()
