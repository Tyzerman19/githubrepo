# a script to automate the monthly outbreak report using both iphis and ccm data
# there are two required inputs for this script:
#       a csv of CCM outbreaks
#       a xlsx of iPHIS outbreak data

# import helpful modules

import pandas as pd
from datetime import date
from datetime import datetime
import time

# this line will suppress the pandas "SettingWithCopyWarning"
pd.options.mode.chained_assignment = None  # default='warn'

# grab our data

iphis = pd.read_excel('iphis.xlsx')
ccm = pd.read_csv('ccm.csv')

# clean for select blanks in iphis extract
# create a master DQ issues list to hold all the DQ issues identified

dq_issues = []

# clean for blank reported date
# create dataframe with DQ issues

blank_reported_date = iphis[["Outbreak Number", "Investigator Last Name"]].loc[
    (iphis["Reported Date"].isnull()) & (iphis["Outbreak Classification"] != "DOES NOT MEET OUTBREAK DEFINITION")]
blank_reported_date["DQ Issue"] = "Blank Reported Date"

# generate list of issues and append to master DQ issues list
blank_reported_date_list = blank_reported_date.values.tolist()
for i in blank_reported_date_list:
    dq_issues.append(i)

# replace blank reported date with the created date
iphis.loc[iphis["Reported Date"].isnull(), "Reported Date"] = iphis["Created Date"]

# clean for blank onset date/time of index case

blank_onset_date = iphis[["Outbreak Number", "Investigator Last Name"]].loc[
    (iphis["Onset Date / Time of Index Case"].isnull()) & (
            iphis["Outbreak Classification"] != "DOES NOT MEET OUTBREAK DEFINITION")]
blank_onset_date["DQ Issue"] = "Blank Onset Date/Time of Index Case"

blank_onset_date_list = blank_onset_date.values.tolist()
for i in blank_onset_date_list:
    dq_issues.append(i)

# clean for blank outbreak declared over

blank_outbreak_declared_over = iphis[["Outbreak Number", "Investigator Last Name"]].loc[
    (iphis["Date Outbreak Declared Over"].isnull()) & (
                iphis["Outbreak Classification"] != "DOES NOT MEET OUTBREAK DEFINITION") & (
                iphis["Outbreak Status Description"] != "OPEN")]
blank_outbreak_declared_over["DQ Issue"] = "Blank Date Outbreak Declared Over"

blank_outbreak_declared_over_list = blank_outbreak_declared_over.values.tolist()
for i in blank_outbreak_declared_over_list:
    dq_issues.append(i)

# clean for open outbreak that should be closed

open_outbreak_1 = iphis[["Outbreak Number", "Investigator Last Name"]].loc[
    (iphis["Outbreak Status Description"] == "OPEN") & (iphis["Date Outbreak Declared Over"].notnull())]
open_outbreak_1["DQ Issue"] = "Open Outbreak Should be Closed"

open_outbreak_1_list = open_outbreak_1.values.tolist()
for i in open_outbreak_1_list:
    dq_issues.append(i)

open_outbreak_2 = iphis[["Outbreak Number", "Investigator Last Name", "Reported Date"]].loc[
    (iphis["Outbreak Status Description"] == "OPEN")]
open_outbreak_2["Current Date"] = date.today()
open_outbreak_2["Current Date"] = pd.to_datetime(open_outbreak_2["Current Date"], format="%Y-%m-%d")
open_outbreak_2["Days Since Reported Date"] = (
        open_outbreak_2["Current Date"] - open_outbreak_2["Reported Date"]).dt.days
open_outbreak_2 = open_outbreak_2[["Outbreak Number", "Investigator Last Name"]].loc[
    open_outbreak_2["Days Since Reported Date"] > 30]
open_outbreak_2["DQ Issue"] = "Outbreak Has Been Open for More than 30 Days, Close if Appropriate"

open_outbreak_2_list = open_outbreak_2.values.tolist()
for i in open_outbreak_2_list:
    dq_issues.append(i)

# clean for disease/agent

gastroenteritis = "GASTROENTERITIS, INSTITUTIONAL OUTBREAKS"
gastro_agents = ["GASTROENTERITIS UNSPECIFIED", "NOROVIRUS"]
respiratory_infection = "RESPIRATORY INFECTION, INSTITUTIONAL OUTBREAKS"
resp_agents = ["CORONAVIRUS", "RSV - RESPIRATORY SYNCYTIAL VIRUS", "RHINOVIRUS", "RESPIRATORY INFECTION UNSPECIFIED",
               "PARAINFLUENZA VIRUS", "METAPNEUMOVIRUS", "ENTERO/RHINOVIRUS", "COVID-19"]
flu_agents = ["INFLUENZA A", "INFLUENZA B"]

disease = iphis[["Outbreak Number", "Investigator Last Name", "Outbreak Classification", "Disease", "Aetiologic Agent"]]

gastro = disease.loc[(disease["Disease"] == gastroenteritis) & (~disease["Aetiologic Agent"].isin(gastro_agents))]
gastro = gastro[["Outbreak Number", "Investigator Last Name"]]
gastro["DQ Issue"] = "Update Agent to match disease"

gastro_list = gastro.values.tolist()
for i in gastro_list:
    dq_issues.append(i)

resp = disease.loc[(disease["Disease"] == respiratory_infection) & (~disease["Aetiologic Agent"].isin(resp_agents))]
resp = resp[["Outbreak Number", "Investigator Last Name"]]
resp["DQ Issue"] = "Update Agent to match disease"

resp_list = resp.values.tolist()
for i in resp_list:
    dq_issues.append(i)

flu = disease.loc[(disease["Disease"] == "INFLUENZA") & (~disease["Aetiologic Agent"].isin(flu_agents))]
flu = flu[["Outbreak Number", "Investigator Last Name"]]
flu["DQ Issue"] = "Update Agent to match disease"

flu_list = flu.values.tolist()
for i in flu_list:
    dq_issues.append(i)

unknown = disease.loc[(disease["Disease"] == "UNKNOWN") & (
        disease["Outbreak Classification"] != "DOES NOT MEET OUTBREAK DEFINITION")]
unknown = unknown[["Outbreak Number", "Investigator Last Name"]]
unknown["DQ Issue"] = "Update Disease and Agent"

unknown_list = unknown.values.tolist()
for i in unknown_list:
    dq_issues.append(i)

# replace unknown disease/agent

iphis.loc[(iphis["Disease"] == "UNKNOWN") & (
        iphis["Outbreak Type"] == "FB / WB / ENTERIC - INSTITUTIONAL"),
 "Aetiologic Agent"] = "GASTROENTERITIS UNSPECIFIED"
iphis.loc[(iphis["Disease"] == "UNKNOWN") & (
        iphis["Outbreak Type"] == "FB / WB / ENTERIC - INSTITUTIONAL"), "Disease"] = gastroenteritis

iphis.loc[(iphis["Disease"] == "UNKNOWN") & (
        iphis["Outbreak Type"] == "RESPIRATORY / DIRECT CONTACT - INSTITUTIONAL"
), "Aetiologic Agent"] = "RESPIRATORY INFECTION UNSPECIFIED"
iphis.loc[(iphis["Disease"] == "UNKNOWN") & (
            iphis["Outbreak Type"] == "FB / WB / ENTERIC - INSTITUTIONAL"), "Disease"] = respiratory_infection

# institutions that do not have an ID number
inst_list = ["albright", "bella", "chippawa", "crescent", "deer park", "lawson", "extendicare", "richelieu", "garden",
             "gilmore", "heidehof", "edelweiss", "henley", "kilean", "linhaven", "maple", "millennium", "grafton",
             "chartwell", "niagara health", "northland", "oakwood", "radiant", "heritage", "tabor", "rapelje",
             "royal rose", "shalom", "tufford", "united", "mennonite", "upper canada", "valley park", "west park",
             "woodlands", "school", "ltch", "long term", "long-term", "meadows", "westhills"]

ob_name = iphis[["Outbreak Number", "Outbreak Name", "Investigator Last Name"]].loc[
    iphis["Outbreak Classification"] != "DOES NOT MEET OUTBREAK DEFINITION"]
ob_name["Outbreak Name Lower"] = ob_name["Outbreak Name"].str.lower()

inst_names = ob_name[ob_name["Outbreak Name Lower"].str.contains("|".join(inst_list))]

missing_id_number = inst_names.loc[~inst_names["Outbreak Name Lower"].str.contains("^[0-9][0-9][0-9][0-9]")]
missing_id_number["Outbreak Name Upper"] = ob_name["Outbreak Name Lower"].str.upper()
missing_id_number["DQ Issue"] = "Institution Number not in Outbreak Name"
missing_id_number = missing_id_number[["Outbreak Number", "Investigator Last Name", "DQ Issue", "Outbreak Name Upper"]]

missing_id_number_list = missing_id_number.values.tolist()

for i in missing_id_number_list:
    print("Is the following Outbreak Name missing an Institution ID Number prefix?")
    print(i[3])
    print("y/n")
    response = input()
    time.sleep(1)
    if response == "y":
        dq_issues.append(i[0:3])

# OB names that do not have correct date at end of name field

missing_date = ob_name.loc[~ob_name["Outbreak Name"].str.contains("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$")]
missing_date["DQ Issue"] = "Outbreak Name missing Reported Date"
missing_date = missing_date[["Outbreak Number", "Investigator Last Name", "DQ Issue", "Outbreak Name"]]

missing_date_list = missing_date.values.tolist()
for i in missing_date_list:
    dq_issues.append(i[0:3])

# OB type is incorrect

ob_type = iphis[["Outbreak Number", "Outbreak Name", "Investigator Last Name"]].loc[
    iphis["Outbreak Type"].str.contains("COMMUNITY")]
ob_type["DQ Issue"] = "Outbreak Type should be Institutional"
ob_type = ob_type[["Outbreak Number", "Investigator Last Name", "DQ Issue", "Outbreak Name"]]

ob_type_list = ob_type.values.tolist()
ob_type_change_list = []

for i in ob_type_list:
    print("Should this Outbreak Type be set to INSTITUTIONAL?")
    print(i[3])
    print("y/n")
    response = input()
    time.sleep(1)
    if response == "y":
        dq_issues.append(i[0:3])
        ob_type_change_list.append(i[0])

iphis.loc[(iphis["Outbreak Number"].isin(ob_type_change_list)) & (
        iphis["Outbreak Type"] == "RESPIRATORY / DIRECT CONTACT - COMMUNITY"), "Outbreak Type"
] = "RESPIRATORY / DIRECT CONTACT - INSTITUTIONAL"
iphis.loc[(iphis["Outbreak Number"].isin(ob_type_change_list)) & (
        iphis["Outbreak Type"] == "FB / WB / ENTERIC - COMMUNITY"
), "Outbreak Type"] = "FB / WB / ENTERIC - INSTITUTIONAL"

# create a cleaning summary

print(".")
print("..")
print(".")
print("..")
print(".")
print("Number of DQ issues identified: " + str(len(dq_issues)))
print("DQ Issues to be sent out to staff for cleaning:")
for i in dq_issues:
    print(i)

# create a csv log of DQ issues and save

dq_csv = pd.DataFrame(dq_issues, columns=["Outbreak Number", "Investigator Last Name", "DQ Issue"])
dq_csv.to_csv("DQ_Issues.csv", header=True, index=False)


# combine iphis and ccm data sets

# pull required columns from iphis df into prep df

iphis_prep = iphis[["Outbreak Number",
                    "Outbreak Name",
                    "Reported Date",
                    "Outbreak Classification",
                    "Outbreak Status Description",
                    "Outbreak Type",
                    "Disease",
                    "Aetiologic Agent"]]

# add system column for tracking

iphis_prep["System"] = "iPHIS"

# rename column to match between both systems

iphis_prep.rename(columns={'Outbreak Status Description': 'Outbreak Status'}, inplace=True)

# pull required columns from ccm df into prep df

ccm_prep = ccm[['Outbreak Number',
                'Outbreak Name',
                'Reported Date',
                'Outbreak Classification',
                'Outbreak Status',
                'Outbreak Type']]

# fill in system column and columns not present

ccm_prep["Outbreak Type"] = "RESPIRATORY / DIRECT CONTACT - INSTITUTIONAL"
ccm_prep["Disease"] = "COVID-19"
ccm_prep["Aetiologic Agent"] = "COVID-19"
ccm_prep["System"] = "CCM"

# combine the two sets into one df

both_sets = [iphis_prep, ccm_prep]
combined = pd.concat(both_sets)

# Reported Date to datetime data type

combined["Reported Date"] = pd.to_datetime(combined["Reported Date"])

# filter out non-confirmed OBs and sort table by Reported Date

combined["Outbreak Classification"] = combined["Outbreak Classification"].str.upper()
combined = combined.loc[combined["Outbreak Classification"] == "CONFIRMED"]
combined = combined.sort_values(by=["Reported Date"])

# add month and year info to label by month

combined["Year"] = combined["Reported Date"].dt.year
combined["Month"] = combined["Reported Date"].dt.month
combined["Month-Year"] = combined["Reported Date"].dt.strftime("%b") + " " + combined["Reported Date"].dt.strftime("%Y")

# remove any OBs that may have been reported within the current month (report is looking at full previous months)

current_time = datetime.now()
current_month = datetime.now().month
current_year = datetime.now().year
month_year = str(current_month) + "-" + str(current_year)
current_month_year = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

# create the working df of 'valid' OBs to use moving forward

working_set = combined.loc[combined["Reported Date"] < current_month_year]
# identify each unique month from the df to be used to organize later tables

months_list = []
unique_months = working_set["Month-Year"].unique()
for i in unique_months:
    months_list.append(i)

# create the "Summary" table

summary_pivot = working_set.pivot_table(
    index="Month-Year", columns="Outbreak Type", values="Outbreak Number", aggfunc='count'
)
summary_pivot = summary_pivot.reindex(unique_months, axis=0)
print(summary_pivot)

# create the "Agent" table

agent_pivot = working_set.pivot_table(index=["Outbreak Type", "Aetiologic Agent"],
                                      values="Outbreak Number", aggfunc='count')
print(agent_pivot)
agent_pivot_month = working_set.pivot_table(index=["Outbreak Type", "Aetiologic Agent"],
                                            columns="Month-Year", values="Outbreak Number", aggfunc='count')
agent_pivot_month = agent_pivot_month.reindex(unique_months, axis=1)
print(agent_pivot_month)


# Package for export

excel_file_name = "OB_Report.xlsx"

print(f"Exporting summary as: {excel_file_name}")
with pd.ExcelWriter(excel_file_name) as writer:
    summary_pivot.to_excel(writer, sheet_name="OB Type by Month")
    agent_pivot.to_excel(writer, sheet_name="OB Type and Agent")
    agent_pivot_month.to_excel(writer, sheet_name="OB Type and Agent by Month")
