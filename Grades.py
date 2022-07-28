from tokenize import group
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np
import functools as ft


def calculate_total_average(row):
    homework1 = row["Homework 1"]
    homework2 = row["Homework 2"]
    homework3 = row["Homework 3"]
    homework_avg = (homework1 + homework2 + homework3) / 3
    quiz1 = row["Grade_x"]
    quiz2 = row["Grade_y"]
    quiz_avg = (quiz1 + quiz2) / 2
    exam = row["Exam"]
    total_grade = (0.1 * homework_avg +
                   0.25 * quiz_avg + 0.65 * exam)
    return total_grade


homework_exams_data = pd.read_csv('homework-exams.csv')
df_homework_exams_data = pd.DataFrame(homework_exams_data)
filtered_df_homework_exams_data = df_homework_exams_data[[
    "SID", "Homework 1", "Homework 2", "Homework 3", 'Exam']]

quiz_1_grades_data = pd.read_csv('quiz_1_grades.csv')
df_quiz_1_grades_data = pd.DataFrame(quiz_1_grades_data)
filtered_df_quiz_1_grades_data = df_quiz_1_grades_data[[
    "SID", "Grade"]]


quiz_2_grades_data = pd.read_csv('quiz_2_grades.csv')
df_quiz_2_grades_data = pd.DataFrame(quiz_2_grades_data)
filtered_df_quiz_2_grades_data = df_quiz_2_grades_data[[
    "SID", "Grade"]]


with open('students.json', 'r') as filename:
    students_data = json.load(filename)
    df_json = pd.read_json(students_data)


dfs = [filtered_df_quiz_2_grades_data,
       filtered_df_quiz_1_grades_data, filtered_df_homework_exams_data]

df_final_grades = ft.reduce(
    lambda left, right: pd.merge(left, right, on='SID'), dfs)

df_json['NetID'] = df_json['NetID'].str.lower()
df_final = df_final_grades.merge(df_json, left_on='SID', right_on='NetID')


df_final['final grade'] = df_final.apply(
    lambda row: calculate_total_average(row), axis=1)

group1 = df_final[df_final['Group'] == 1].sort_values('final grade')
group2 = df_final[df_final['Group'] == 2].sort_values('final grade')
group3 = df_final[df_final['Group'] == 3].sort_values('final grade')

group1 = group1.rename(columns={"Name": "student name", "ID": "ID number"})
group1 = group1[["student name", "ID number", "final grade"]]


group2 = group2.rename(columns={"Name": "student name", "ID": "ID number"})
group2 = group2[["student name", "ID number", "final grade"]]

group3 = group3.rename(columns={"Name": "student name", "ID": "ID number"})
group3 = group3[["student name", "ID number", "final grade"]]


writer = pd.ExcelWriter('group1_grades.xlsx')
group1.to_excel(writer)
# writer.save()

writer = pd.ExcelWriter('group2_grades.xlsx')
group2.to_excel(writer)
# writer.save()

writer = pd.ExcelWriter('group3_grades.xlsx')
group3.to_excel(writer)
# writer.save()


# todo show all the groups in a bar or histogram chart with matplotlib and extract functions (refactor)

# x = np.arange(3)
# y1 = group1['final grade'][:3]
# y2 = group2['final grade'][:3]
# y3 = group3['final grade'][:3]

# width = 0.2

# plt.bar(x-0.2, y1, width, color='cyan')
# plt.bar(x, y2, width, color='orange')
# plt.bar(x+0.4, y3, width, color='pink')


# plt.xlabel("Type of exercise")
# plt.ylabel("Grades")
# plt.legend(["Group 1", "Group2", "Group3"])

# plt.show()
