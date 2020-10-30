#!/usr/bin/python
import os 
import psycopg2
import datetime
import time
import json
import decimal
import requests
import csv

from config import CORP_TYPES_IN_SCOPE, corp_num_with_prefix, bare_corp_num


def compare_bc_reg_orgbook(bc_reg_corp_types, orgbook_corp_types, future_corps):
    # check if all the BC Reg corps are in orgbook (with the same corp type)
    for bc_reg_corp_num in bc_reg_corp_types:
        bc_reg_corp_type = bc_reg_corp_types[bc_reg_corp_num]
        if bare_corp_num(bc_reg_corp_num) in future_corps:
            #print("Future corp ignore:", row["corp_num"])
            pass
        elif not bc_reg_corp_num in orgbook_corp_types:
            # not in orgbook
            #print("Topic not found for:", row)
            print("./manage -e prod queueOrganization " + bare_corp_num(bc_reg_corp_num))
        elif (not orgbook_corp_types[bc_reg_corp_num]) or (orgbook_corp_types[bc_reg_corp_num] != bc_reg_corp_type):
            # in orgbook but has the wrong corp type in orgbook
            #print("Corp Type mis-match for:", row, orgbook_corp_types[row["corp_num"]])
            print("./manage -p bc -e prod deleteTopic " + bc_reg_corp_num)
            print("./manage -e prod requeueOrganization " + bare_corp_num(bc_reg_corp_num))

    # now check if there are corps in orgbook that are *not* in BC Reg database
    for orgbook_corp in orgbook_corp_types:
        if not (orgbook_corp in bc_reg_corp_types):
            print("OrgBook corp not in BC Reg:", orgbook_corp)

