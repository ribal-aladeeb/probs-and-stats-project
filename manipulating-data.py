import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.stats as stats

Z_from_probability = stats.norm.ppf
probability_of_Z = stats.norm.cdf

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
        email_of_respondent = numerical_raw_survey.iloc[i, 17]
        gpa_of_respondent = float(numerical_raw_survey.iloc[i, 16])
        if email_of_respondent in blacklisted_emails or gpa_of_respondent <= 0.1:
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


def save_cleaned_dataframe(df):
    df.to_csv('./data/analysis.ready.data.csv', index=None, header=True)
    return


def plot_gpas_alone(data):
    questions = data.columns
    plt.plot(data[questions[5]], 'ro')
    plt.show()


def sample_size(data):
    return len(data.index)


def gpa_list(data):
    return list(data.iloc[:, 5])


def mean_gpa(data):
    gpas = gpa_list(data)
    sample_mean = sum(gpas)/len(gpas)
    return sample_mean


def sample_gpa_variance(data):
    # Extract gpas as numpy array to propagate math operations without looping
    # over each element.
    gpas = np.array(gpa_list(data))
    variance = (sum(gpas**2) - sum(gpas)**2/len(gpas)) / (len(gpas)-1)
    return variance


def std_dev_gpa(data):
    return math.sqrt(sample_gpa_variance(data))


def median_gpa(data):
    gpas = gpa_list(data)
    midpoint = int(len(gpas)/2)
    if len(gpas) % 2 == 0:
        return gpas[midpoint]
    lower = gpas[midpoint]
    upper = gpas[midpoint+1]
    median = (lower+upper)/2
    return median


def calculate_Z_value(mu0, X_bar, S, n):
    # because our sample size is greater than 200, we feel confident of
    # estimating sigma using S. In this way we can use the Z-distribution
    # instead of the T-distribution. This is often done when n > 30.
    Z = (X_bar - mu0)/(S/math.sqrt(n))
    return Z


def calculate_p_value(data, mu0=3.2):
    X_bar = mean_gpa(data)
    S = std_dev_gpa(data)
    n = sample_size(data)
    Z = abs(calculate_Z_value(mu0, X_bar, S, n))
    p_value = 2*probability_of_Z(-Z)
    return p_value, Z


def find_Z_alpha(confidence):
    alpha = 1-confidence
    Z_alpha_over2 = abs(Z_from_probability(1-alpha/2))
    return alpha, Z_alpha_over2


cleaned = clean(numerical_survey)

n = sample_size(cleaned)
xbar = mean_gpa(cleaned)
S_squared = sample_gpa_variance(cleaned)
S = std_dev_gpa(cleaned)

print("sample size:", n)
print("mean:", xbar)
print("variance:", S_squared)
print("standard dev:", S)
print("median:", median_gpa(cleaned))

alpha, cutoff_Z = find_Z_alpha(0.98)
print("alpha:", alpha)
print("Z alpha/2:", cutoff_Z)

p_value, actual_Z = calculate_p_value(cleaned)
print("actual Z:", actual_Z)
print("p_value:", p_value)
