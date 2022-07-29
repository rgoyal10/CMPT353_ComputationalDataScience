#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import sys
from scipy import stats

def count_used(data):
    if(data['search_count'] > 0):
        return True
    return False

def count_unused(data):
    if(data['search_count'] == 0):
        return True
    return False

OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value:  {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value:  {more_searches_p:.3g} \n'
    '"Did more/less instructors use the search feature?" p-value:  {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value:  {more_instr_searches_p:.3g}'
)


def main():
#     filename1 = 'searches.json'
    filename1 = sys.argv[1]

    data = pd.read_json(filename1,orient='records', lines=True)

    odd_data = data[(data['uid']% 2 !=0)]
    even_data = data[(data['uid']% 2 ==0)]


    odd_count_atleast_once = odd_data.apply(count_used,axis =1 )
    odd_count_used = len(odd_count_atleast_once[odd_count_atleast_once == True].index) #referred to https://thispointer.com/pandas-count-rows-in-a-dataframe-all-or-those-only-that-satisfy-a-condition/

    odd_count_not_used = odd_data.apply(count_unused,axis =1 )
    odd_count_unused = len(odd_count_not_used[odd_count_not_used == True].index) 

    even_count_atleast_once = even_data.apply(count_used,axis=1)
    even_count_used = len(even_count_atleast_once[even_count_atleast_once == True].index)

    even_count_not_used = even_data.apply(count_unused,axis=1)
    even_count_unused = len(even_count_not_used[even_count_not_used == True].index)

    contingency = [[odd_count_used,odd_count_unused],
                 [even_count_used,even_count_unused]]

    chi2_more_user, p_more_user, dof_more_user, expected_more_user = stats.chi2_contingency(contingency)

    p_often_user = stats.mannwhitneyu(odd_data['search_count'], even_data['search_count']).pvalue

    #after removing no-instructors
    instructor_odd_data = odd_data[(odd_data['is_instructor'] == True)]
    instructor_even_data = even_data[(even_data['is_instructor'] == True)]

    odd_count_atleast_once_instructor = instructor_odd_data.apply(count_used,axis =1 )
    instructor_odd_count_used = len(odd_count_atleast_once_instructor[odd_count_atleast_once_instructor == True].index)

    odd_count_not_used_instructor = instructor_odd_data.apply(count_unused,axis =1 )
    instructor_odd_count_unused = len(odd_count_not_used_instructor[odd_count_not_used_instructor == True].index) 

    even_count_atleast_once_instructor = instructor_even_data.apply(count_used,axis=1)
    instructor_even_count_used = len(even_count_atleast_once_instructor[even_count_atleast_once_instructor == True].index)

    even_count_not_used_instructor = instructor_even_data.apply(count_unused,axis=1)
    instructor_even_count_unused = len(even_count_not_used_instructor[even_count_not_used_instructor == True].index)

    new_contingency = [[instructor_odd_count_used,instructor_odd_count_unused],
                 [instructor_even_count_used,instructor_even_count_unused]]

    chi2_more_user_inst, p_more_user_inst, dof_more_user_inst, expected_more_user_inst = stats.chi2_contingency(new_contingency)

    p_often_user_inst = stats.mannwhitneyu(instructor_odd_data['search_count'], instructor_even_data['search_count']).pvalue


    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p=p_more_user,
        more_searches_p=p_often_user,
        more_instr_p=p_more_user_inst,
        more_instr_searches_p=p_often_user_inst,
    ))


if __name__ == '__main__':
    main()

