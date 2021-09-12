import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')
    total = df.shape[0]

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.race.value_counts()

    # What is the average age of men?
    average_age_men = round(df.loc[df['sex'] == 'Male'].age.mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round((
        df.loc[df['education'] == 'Bachelors'].shape[0] / total) * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    high_ed_labels = ('Bachelors', 'Masters', 'Doctorate')

    higher_education = df.query('education in @high_ed_labels')
    lower_education = df.query('education not in @high_ed_labels')

    # percentage with salary >50K
    high = '>50K'

    higher_education_rich = round((higher_education.query(
        'salary == @high').shape[0] / higher_education.shape[0]) * 100, 1)
    lower_education_rich = round((lower_education.query(
        'salary == @high').shape[0] / lower_education.shape[0]) * 100, 1)
    round(higher_education_rich, 1)
    round(lower_education_rich, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    min_workers = df.loc[df['hours-per-week'] == min_work_hours]
    num_min_workers = min_workers.shape[0]

    rich_percentage = (min_workers.query(
        'salary == @high').shape[0] / num_min_workers) * 100

    # What country has the highest percentage of people that earn >50K?
    rich_count = df.query(
        'salary == @high')[['native-country', 'salary']].groupby('native-country').count()

    percentages = pd.concat(
        [rich_count, df['native-country'].value_counts()], axis=1)
    percentages.dropna(inplace=True)
    percentages['rich_percentage'] = (
        percentages['salary']/percentages['native-country'])*100
    percentages.sort_values(by='rich_percentage',
                            ascending=False, inplace=True)

    highest_earning_country = percentages.iloc[0].name
    highest_earning_country_percentage = round(percentages.iloc[0][2], 1)

    # Identify the most popular occupation for those who earn >50K in India.
    india_rich = df[(df['native-country'] == 'India') & (df['salary'] == high)]

    top_IN_occupation = india_rich['occupation'].value_counts().index[0]

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(
            f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(
            f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(
            f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(
            f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
