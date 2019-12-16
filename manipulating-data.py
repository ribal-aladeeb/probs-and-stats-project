import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# list respondents who gave fake answers or made mistakes in answering.
# They have to be removed from the analysis in order not to skew the results
blacklisted_emails = [
    'CleanYourData@Hal3anneh.com',
    'nope@hotmail.com',
    'eyePISSEDandFARDEDandSHIDDEDandCAMEallOVERthePLACE@lmao.pwned.com',
    'chadi.sargi@gmail.com'
]

original_survey = "./data/condensed.actual.latest.csv"
numerical_survey = './data/condensed.numerical.latest.csv'


def clean(survey_filename: str):
    '''
    Remove the data points where people purpusefully tried to lie.
    Remove all metadata unrelated to business logic
    '''
    file = survey_filename
    numerical_raw_survey = pd.read_csv(file)
    total_rows = len(numerical_raw_survey.index)

    print(total_rows)

    indexes_to_be_removed = []

    for i in range(1, total_rows):
        email_of_respondent_i = numerical_raw_survey.iloc[i, 17]
        if email_of_respondent_i in blacklisted_emails:
            indexes_to_be_removed.append(i)

    numerical_raw_survey = numerical_raw_survey.drop(
        axis=0, index=indexes_to_be_removed)
    print(len(numerical_raw_survey.index))

    # only keep answers to survey questions, exclude the faculty question
    # 17 is the index of the email column
    responses = numerical_raw_survey.iloc[1:, list(range(11, 17))]

    # cast string entries to float
    responses = pd.DataFrame.astype(responses, float)
    return responses


# def save_cleaned_dataframe(df):

#     df.to_csv('./data/analysis.ready.data.csv', index=None, header=True)
#     return


# def plot_gpas_alone(data: str):
#     questions = data.columns
#     plt.plot(data[questions[6]], 'ro')
#     plt.show()


def analysis(filename: str):
    raw_survey = pd.read_csv(filename)
    # 17 is the index of the email column
    survey_responses = raw_survey.iloc[1:, list(range(9, 17))]
    questions = survey_responses.columns
    # print(type(questions))
    # print(questions[0])
    # questions[7] contains GPAs
    for i in range(len(survey_responses)):
        survey_responses.iloc[i, 7] = float(survey_responses.iloc[i, 7])
    print(survey_responses)
    plt.plot(survey_responses[questions[7]], 'ro')
    plt.show()


# Do not run this function if you have already generated those two files because
# it will overwrite them.
def write_csv_files():
    raw_data = pd.read_csv('./data/condensed.actual.csv')
    emails = pd.DataFrame(raw_data.iloc[1:, 17])
    survey_answers = raw_data.iloc[1:, list(range(9, 17))]
    emails.to_csv('./data/emails.csv', index=None, header=True)
    survey_answers.to_csv('./data/questions.only.csv', index=None, header=True)


cleaned = clean(numerical_survey)

print(cleaned)
