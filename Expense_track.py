import numpy as np
import pandas as pd
import os
from datetime import date
import matplotlib.pyplot as plt;

plt.rcdefaults()
import matplotlib.pyplot as plt


def create_category(category, category_name):
    name = input("\n\tEnter the Category Name : ")
    if name not in category_name:
        category_name.append(name)


def allocate_expense(category, category_name, Final_Chart_Table):
    if len(category_name) == 0:
        print("\n\n\tFirst Create a Category and then Add Expenses")
        return
    while True:
        print("\n\n\tThe Catagories are as Follows : \n")
        for i in range(len(category_name)):
            print(f"\t{i + 1}.{category_name[i]}")
        select = int(input("\n\tSelect your Category : "))
        if select < len(category_name) + 1:
            break
        else:
            print("\n\n\tPlease enter a valid Category !")
    amount = float(input("\n\t\tEnter the Expense amount : "))
    if category_name[select - 1] not in category:
        category[category_name[select - 1]] = []
        category[category_name[select - 1]].append(amount)
    else:
        category[category_name[select - 1]].append(amount)
    Final_Chart_Table["Amount"].append(amount)
    Final_Chart_Table["Category"].append(category_name[select - 1])
    date_choice = input("\n\t\tUse Current Date : (y/n)  ")
    if date_choice == 'y':
        Final_Chart_Table["Date"].append(str(date.today().strftime("%d/%m/%Y")))
    else:
        while True:
            manual_date = (input("\n\t\tEnter the Date (dd/mm/year) : "))
            if len(manual_date) != 10:
                print("\n\t\tEnter a valid Date !")
            elif int(manual_date[:2]) > 31 or int(manual_date[:2]) < 1 or int(manual_date[3:5]) < 1 or int(
                    manual_date[3:5]) > 12 or int(manual_date[6:10]) < 2001 or int(manual_date[6:10]) > 2019:
                print("\n\t\tEnter a valid Date !")
            else:
                break
        Final_Chart_Table["Date"].append(manual_date)


def daily_expense_chart(chartFinal):
    current_date = str(date.today().strftime("%d/%m/%Y"))
    df = chartFinal["Date"] == current_date
    print("\nToday's Expense Chart is\n")
    print(chartFinal[df])


"""def monthly_expense_chart():
    current_date=str(date.today().strftime("%d/%m/%Y"))
    #df=chartFinal["Date"][3:10]==current_date[3:10]
    #chartFinal.loc[chartFinal.Category=="a"]
    print("\nToday's Expense Chart is\n")
    print(chartFinal.loc[chartFinal.Date[3:10]==current_date.iloc[3:10]])

def yearly_expense_chart():
    current_date=str(date.today().strftime("%d/%m/%Y"))
    df=chartFinal["Date"][6:10]==current_date[6:10]
    print("\nThe Year's Expense Chart is\n")
    print(chartFinal[df])"""


def Entire_Expense(chartFinal):
    print("\nThe entire Expense is as follows : ")
    print("\n\n", chartFinal)
    print()


def Pie_Chart(category, category_name):
    labels = category_name
    sizes = []
    for element in category:
        sizes.append(sum(category[element]))
    print(sizes)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')
    plt.show()


def Bar_Chart(category, category_name):
    sizes = []
    for element in category:
        sizes.append(sum(category[element]))
    y_pos = np.arange(len(category))
    plt.bar(y_pos, sizes, align='center', alpha=0.5)
    plt.xticks(y_pos, category)
    plt.ylabel('Amount')
    plt.title('Expense')
    plt.show()
    return


def print_to_file_category_name(category_name):
    f = open("category_name.txt", "r+")
    f.truncate(0)
    f.close()
    string = " ".join(category_name)
    f = open("category_name.txt", "w")
    f.write(str(string))
    f.close()
    return


def print_to_file_category(category, category_name):
    f = open("category.txt", "r+")
    f.truncate(0)
    f.close()
    f = open("category.txt", "w")
    for e in category_name:
        for i in range(0, len(category[e])):
            category[e][i] = str(category[e][i])
        string = " ".join(category[e])

        f.write(str(string))
        f.write("\n")
    f.close()
    return


print("\n\n*****Expense Tracker*****\n\n")
Final_Chart_Table = {"Amount": [], "Category": [], "Date": []}
if os.stat("category_name.txt").st_size == 0:
    category_name = []
else:
    f = open("category_name.txt", "r")
    string = str(f.readline())
    category_name = string.split(" ")
    f.close()
category = {}
if os.stat("category.txt").st_size == 0:
    category = {}
else:
    f = open("category.txt", "r")
    for e in category_name:
        string = str(f.readline())
        category[e] = list(map(float, string.split(" ")))
    f.close()
if os.stat("Final_Expense_Chart.csv").st_size != 0:
    Previous = pd.read_csv("Final_Expense_Chart.csv", index_col=0)
check = False
while True:
    print("\n\nMENU\n")
    print(
        "\n0.To exit from Interface\n1.Set Catagories\n2.Enter Expense for Respective Date\n3.Show Daily Expense Chart\n4.Entire Expense till now\n5.Statistics based on Pie Chart\n6.Statistics based on Bar chart\n7.Clear Screen\n\n")
    choice = int(input("\nEnter Your Choice : "))
    if choice == 1:
        create_category(category, category_name)
    elif choice == 2:
        allocate_expense(category, category_name, Final_Chart_Table)
        chartFinal = pd.DataFrame(Final_Chart_Table,
                                  index=[i for i in range(1, int(len(Final_Chart_Table["Amount"])) + 1)],
                                  columns=["Amount", "Category", "Date"])
        if os.stat("Final_Expense_Chart.csv").st_size != 0:
            Previous = Previous.append(chartFinal)
            chartFinal = Previous.copy()
            chartFinal.set_index(i for i in range(1, chartFinal.Date.size))
            c = chartFinal["Date"].count()
            chartFinal.index = range(1, c + 1)
        check = True
    elif choice == 3:
        if check:
            daily_expense_chart(chartFinal)
        else:
            daily_expense_chart(Previous)
    elif choice == 4:
        if check:
            Entire_Expense(chartFinal)
        else:
            Entire_Expense(Previous)
    elif choice == 5:
        Pie_Chart(category, category_name)
    elif choice == 6:
        Bar_Chart(category, category_name)
    elif choice == 7:
        clear = lambda: os.system('cls')
        clear()
    else:
        print_to_file_category_name(category_name)
        print_to_file_category(category, category_name)
        break
if check:
    chartFinal.to_csv('Final_Expense_Chart.csv')
else:
    Previous.to_csv('Final_Expense_Chart.csv')
print("\n\nThank You!\n")
