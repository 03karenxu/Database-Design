#!/usr/bin/env python3

import psycopg2
import re

MAX_QUERIES = 10
PAGE_LENGTH = 70

Q_NUM = 0
QUESTION = 1
HEADER = 2
PRINT = 3

#########################
# FORMATTING FUNCTIONS #
########################

def print_double_line(length):
    print("\n" + "=" * length)

def print_single_line(length):
    print("-" * length)

def visualize_funds(inflow, outflow):
    max_width = 50
    
    # calculate percentages of inflow and outflow relative to max
    inflow_percentage = min(100, (inflow / (inflow + outflow)) * 100)
    outflow_percentage = min(100, (outflow / (inflow + outflow)) * 100)
    
    # calculate num characters for inflow and outflow
    inflow_chars = int((inflow_percentage / 100) * max_width)
    outflow_chars = int((outflow_percentage / 100) * max_width)
    
    # create ASCII chart strings
    inflow_chart = '#' * inflow_chars
    outflow_chart = '#' * outflow_chars
    
    # print ASCII chart
    print("\n  Here is a visualization of the current state of the campaign's funds:")
    print("\n  Amount funded:  " + inflow_chart)
    print("  Total cost:     " + outflow_chart)

########################
# VALIDATING FUNCTIONS #
########################

def is_valid_query(query_num):
    error_message = "Input is invalid. Please enter a valid query number: "
    while True:
        try:
            query_num = int(query_num)
            if query_num > 0 and query_num <= MAX_QUERIES:
                return query_num
            else:
                query_num = input(error_message)
        except ValueError:
            query_num = input(error_message)

def is_valid_date(date_string, time):
    # define regex pattern for YYYY-MM-DD
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    datetime_pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
    
    # check if the date_string matches pattern
    if time == False:
        while True:
            if re.match(pattern, date_string):
                return date_string
            else:
                date_string = input("  Invalid date. Please enter a valid date as YYYY-MM-DD: ")
    if time == True:
        while True:
            if re.match(datetime_pattern, date_string):
                return date_string
            else:
                date_string = input("  Invalid date. Please enter a valid date as YYYY-MM-DD HH:MM:SS: ")

def is_valid_num(num):
    error_message = "  Input was invalid. Please enter an integer: "
    while True:
        try:
            num = int(num)
            return num
        except ValueError:
            num = input(error_message)

####################
# INPUT FUNCTIONS #
###################

def get_campaign_info():
    while True:
        title = input('\n  Campaign title: ')
    
        campaign_id = input('\n  Campaign ID: ')
        campaign_id = is_valid_num(campaign_id)
            
        budget = input('\n  Budget: $')
        budget = is_valid_num(budget)
            
        start_date = input('\n  Start date (YYYY-MM-DD): ')
        start_date = is_valid_date(start_date, False)

        end_date = input('\n  Projected end date (YYYY-MM-DD): ')
        end_date = is_valid_date(end_date, False)

        print_double_line(PAGE_LENGTH)

        # check if correct
        print("\n  CONFIRM CAMPAIGN INFORMATION\n")
        print("  Title: %s" % title)
        print("  Campaign ID: %s" % campaign_id)
        print("  Budget: $%s" % budget)
        print("  Start date: %s" % start_date)
        print("  Projected end date: %s" % end_date)
    
        confirm = input("\n  Is the information correct? (Y/N): ")
        if confirm.lower() == 'y':
            return [campaign_id, title, budget, start_date, end_date]
        elif confirm.lower() != 'n':
            confirm = input("  Invalid input. Please enter Y or N: ")

    print_double_line(PAGE_LENGTH)

def get_event_info():
    while True:
        title = input('\n  Event title: ')
    
        event_id = input('\n  Event ID: ')
        event_id = is_valid_num(event_id)         
        location = input('\n  Location: ')
            
        date_time = input('\n  Start date and time (YYYY-MM-DD HH:MM:SS): ')
        date_time = is_valid_date(date_time, True)

        print_double_line(PAGE_LENGTH)

        # check if correct
        print("\n  CONFIRM EVENT INFORMATION\n")
        print("  Title: %s" % title)
        print("  Event ID: %s" % event_id)
        print("  Location: %s" % location)
        print("  Date/Time: %s" % date_time)
    
        confirm = input("\n  Is the information correct? (Y/N): ")
        if confirm.lower() == 'y':
            return [title, event_id, location, date_time]
        elif confirm.lower() != 'n':
            confirm = input("  Invalid input. Please enter Y or N: ")

########################
# VIEW QUERY FUNCTIONS #
########################

def execute_query(query_num, cursor):
    queries = {
        1: ['Q1', 
            "\n  SELECTED QUERY: Which events earned more than $5 000?\n",
            "  Event name" + " " * 21 + "Amount raised\n  ",
            lambda row: print("  %s %s" % (row[0], row[1]))],
        2: ['Q2',
            "\n  SELECTED QUERY: How many volunteers signed up for Rivers Reborn events?\n",
            "",
            lambda row: print("  There are currently %s volunteers signed up events under the Rivers Reborn campaign." % (row[0]))],
        3: ['Q3',
            "\n  SELECTED QUERY: What is the total donation amount per donor?\n",
            "  Donor id" + " " * 4 + "Donor name" + " " * 23 + "Amount donated\n  ",
            lambda row: print("  %s        %s   %s" % (row[0], row[1], row[2]))],
        4: ['Q4',
            "\n  SELECTED QUERY: Who organized the event which raised the most money?\n",
            "  Employee name" + " " * 8 + "Employee ID\n  ",
            lambda row: print ("  %s %s" % (row[0], row[1]))],
        5: ['Q5',
            "\n  SELECTED QUERY: Who are the employees who are not Project Managers?\n",
            "  Employee name" + " " * 8 + "Employee ID\n  ",
            lambda row: print ("  %s %s" % (row[0], row[1]))],
        6: ['Q6',
            "\n  SELECTED QUERY: How many events have been organized by Jane Smith?\n",
            "",
            lambda row: print ("  Jane Smith has organized %s events." % (row[0]))],
        7: ['Q7',
            "\n  SELECTED QUERY: What is the id and start date of the campaign which started most recently?\n",
            "  Campaign ID" + " " * 4 + "Start date\n  ",
            lambda row: print ("  %s            %s" % (row[0], row[1]))],
        8: ['Q8',
            "\n  SELECTED QUERY: Who are the employees who are also members of GnG?\n",
            "  Employee name" + " " * 8 + "Employee ID\n  ",
            lambda row: print ("  %s %s" % (row[0], row[1]))],
        9: ['Q9',
            "\n  SELECTED QUERY: What is the total allocated fund for each campaign?\n",
            "  Campaign ID" + " " * 4 + "Total allocated funds\n  ",
            lambda row: print ("  %s            %s" % (row[0], row[1]))],
        10: ['Q10',
             "\n  SELECTED QUERY: How many web pushes have been sent for each campaign?\n",
             "  Campaign ID" + " " * 4 + "Total web pushes\n  ",
             lambda row: print ("  %s            %s" % (row[0], row[1]))]
    }

    # get query from dict
    query = queries[query_num]

    # print selected query
    print(query[QUESTION])
    
    # execute query
    cursor.execute("""
    select *
    from Q%(num)s
    """ , {'num': query_num})

    # print table
    if query[HEADER] == "":
        row = cursor.fetchone()
        if row:
            query[PRINT](row)
    else:
        print(query[HEADER], end = '')
        print_single_line(PAGE_LENGTH - 4)
        for row in cursor.fetchall():
            query[PRINT](row)

def view_acc_info(campaign_id, cursor):
    print_double_line(PAGE_LENGTH)

    # get campaign outflow
    cursor.execute("""
    select campaign.cost
    from campaign
    where campaign.campaign_id = %(cid)s
    """, {'cid': campaign_id})

    # get result
    row = cursor.fetchone()
    
    # check if row exists
    if row:
        # get cost
        outflow = row[0]
        # display total cost
        print(f"\n  Total cost of campaign: ${outflow:.2f}")
    else:
        print("\n  No data found")

    # get campaign inflow
    cursor.execute("""
    select sum(funds.amount)
    from campaign c
    join (
        select funds.campaign_id, allocation.amount
        from allocation
        join funds on allocation.allocation_id = funds.allocation_id
    ) as funds on c.campaign_id = funds.campaign_id
    where c.campaign_id = %(cid)s;
    """, {'cid': campaign_id})
    
    # get result
    row = cursor.fetchone()
    
    # check if row exists
    if row:
        # get cost
        inflow  = row[0]
        if not inflow:
             inflow = 0
        # display total cost
        print(f"\n  Total amount allocated: ${inflow:.2f}")
    else:
        print("\n  No data found")

    # find remaining needed funding amount
    amnt_needed = outflow - inflow
    if amnt_needed < 0:
        amnt_needed = 0

    print(f"\n  Funds needed: ${amnt_needed:.2f}") 

    # print bar charts to visualize info
    visualize_funds(inflow, outflow)

def view_campaigns(cursor):
    cursor.execute("""
    select *
    from campaign
    """)

    # header
    print(f"\n  {'ID':<5}{'Title':<80}{'Budget':<10}{'Status':<20}{'Start date':<12}{'End date':<12}")
    print_single_line(139)

    # table
    for row in cursor.fetchall():
        # convert date type to string
        s_date = row[4].strftime('%Y-%m-%d') if row[4] else ''
        e_date = row[5].strftime('%Y-%m-%d') if row[5] else ''
        print(f"  {row[0]:<5}{row[1]:<80}{row[2]:<10}{row[3]:<20}{s_date:<12}{e_date:<12}")

def view_member_history(cursor):
    print_double_line(PAGE_LENGTH)
    member_id = input("\n  Please enter the member ID of the member whose history you would like to browse: ")

    cursor.execute("""
    select participates.campaign_id, campaign.start_date
    from participates
    join campaign on campaign.campaign_id = participates.campaign_id
    where participates.member_id = %(mid)s
    union
    select volunteers.campaign_id, campaign.start_date
    from volunteers
    join campaign on campaign.campaign_id = volunteers.campaign_id
    where volunteers.member_id = %(mid)s
    """, {'mid': member_id})

    print(f"\n  SELECTED MEMBER:  {member_id}\n")
    
    # display membership history
    print(f"  {'Campaign ID':<13}{'Date participated': <20}")
    print_single_line(50)
    for row in cursor.fetchall():
        s_date = row[1].strftime('%Y-%m-%d') if row[1] else ''
        print(f"  {row[0]:<13}{s_date:<20}")

def view_members(cursor):
    # Fetch and display membership history
    cursor.execute("""
    select *
    from member
    order by start_date asc
    """)

    # display membership history
    print(f"  {'Member ID':<12}{'Name':<30}{'Phone': <18}{'Email': <30}{'Start date':<20}")
    print_single_line(90)
    for row in cursor.fetchall():
        s_date = row[4].strftime('%Y-%m-%d') if row[4] else ''
        print(f"  {row[0]:<12}{row[1]:<30}{row[2]:<18}{row[3]:<30}{s_date:<20}")
        
def view_annotations(a_type, cursor, dbconn):
    if a_type == 'c':
        type_str = "Campaign"
        cursor.execute("""
        select *
        from c_annotations
        """)
    else:
        type_str = "Member"
        cursor.execute("""
        select *
        from m_annotations
        """)

    header_str = f"{type_str} ID"
    print(f"  {header_str:<13}{'Annotation': <100}")
    print_single_line(70)
    for row in cursor.fetchall():
        print(f"  {row[0]:<13}{row[1]:<100}")

def view_pushes(cursor):
    # show web pushes
    cursor.execute("""
    select *
    from web_push
    """)

    # header
    print(f"\n  {'ID':<5}{'Content':<80}{'Time':<20}")
    print_single_line(112)

    # table
    for row in cursor.fetchall():
        curr_time = row[2].strftime('%Y-%m-%d %H:%M:%S') if row[2] else ''
        print(f"  {row[0]:<5}{row[1]:<80}{curr_time:<20}")

def view_campaign_events(cursor, campaign_id):
    # view campaign events
    cursor.execute("""
    select *
    from event
    where (event.campaign_id = %(id)s)
    """, {'id': campaign_id})

    # header
    print(f"\n  {'Campaign ID':<13}{'Event ID':<10}{'Location':<40}{'Title':<30}{'Date/time':<20}{'Amount raised':<10}")
    print_single_line(130)
    # table
    for row in cursor.fetchall():
        # convert date type to string
        s_date = row[4].strftime('%Y-%m-%d %H:%M:%S') if row[4] else ''
        print(f"  {row[0]:<13}{row[1]:<10}{row[2]:<40}{row[3]:<30}{s_date:<20}{row[5]:<10}")
        
#######################
# INSERTING FUNCTIONS #
#######################

def schedule_event(cursor, campaign_id, dbconn):
    print_double_line(PAGE_LENGTH)

    # get event info from user
    event_info = get_event_info()
    title = event_info[0]
    event_id = event_info[1]
    location = event_info[2]
    date_time = event_info[3]

    # add to event table
    cursor.execute("""
    insert into event
    values (%(id)s, %(e)s, %(l)s, %(t)s, %(d)s, 0)
    """, {'id': campaign_id, 'e': event_id, 'l': location, 't': title, 'd': date_time})

    dbconn.commit()

    print_double_line(PAGE_LENGTH)

    print("\n  New event added: ")
    view_campaign_events(cursor, campaign_id)

    print_double_line(PAGE_LENGTH)
    
    choice = input("\n  Would you like to add volunteers to this event? (Y/N): ")
    
    if choice.lower() == 'y':
        add_volunteers(event_id, campaign_id, cursor, dbconn)
        while True:
            more = input("\n  Would you like to add more volunteers? (Y/N): ")
            if more.lower() == 'y':
                add_volunteers(event_id, campaign_id, cursor, dbconn)
            else:
                break

def add_volunteers(event_id, campaign_id, cursor, dbconn):  
    new = input("\n  Is this a first-time volunteer? (Y/N): ")

    # if this is a new volunteer, ask for input
    if new.lower() == 'y':
        # get volunteer info
        print("\n  Please provide the following volunteer information:")
        member_id = input("\n  Member id: ")
        name = input("\n  Name: ")
        phone = input("\n  Phone number: ")
        email = input("\n  Email: ")
        start_date = input("\n  Start date (YYYY-MM-DD HH:MM:SS): ")
        start_date = is_valid_date(start_date, True)

        # add to member table
        cursor.execute("""
        insert into member
        values (%(mid)s, %(n)s, %(p)s, %(e)s, %(sd)s)
        """, {'mid': member_id, 'n': name,'p': phone, 'e': email,'sd': start_date})
        
        # add to volunteer table
        cursor.execute("""
        insert into volunteer
        values (%(mid)s, %(n)s, %(p)s, %(e)s, %(sd)s, 'Junior', 0)
        """, {'mid': member_id, 'n': name,'p': phone, 'e': email,'sd': start_date})
        
        dbconn.commit()

    # if this is an existing volunteer, ask for member id
    else:
        # show volunteer table
        cursor.execute("""
        select *
        from volunteer
        """)
        print("\n  Here are all the volunteers who currently exist in the system:")
        
        # header
        print(f"\n  {'Volunteer ID':<14}{'Name':<30}{'Phone':<18}{'Email':<30}{'Start date':<15}{'Tier':<10}{'Vol count': <4}")
        print_single_line(139)
        
        # table
        for row in cursor.fetchall():
            # convert date type to string
            s_date = row[4].strftime('%Y-%m-%d %H:%M:%S') if row[4] else ''
            print(f"  {row[0]:<14}{row[1]:<30}{row[2]:<18}{row[3]:<30}{s_date:<15}{row[5]:<10}{row[6]:<4}")

        member_id = input("\n  Please enter the volunteer ID of the desired volunteer: ")

    # add to volunteers table
    cursor.execute("""
    insert into volunteers
    values (%(vid)s, %(eid)s, %(cid)s)
    """, {'cid': campaign_id, 'eid': event_id, 'vid': member_id})

    dbconn.commit()

    print("\n  New volunteer added:")

    # show volunteers table
    cursor.execute("""
    select *
    from volunteers
    where volunteers.event_id = %(eid)s and volunteers.campaign_id = %(cid)s
    """, {'cid': campaign_id, 'eid': event_id})

    # header
    print(f"\n  {'Volunteer ID':<14}{'Event ID':<10}{'Campaign ID':<13}")
    print_single_line(30)
    
    # table
    for row in cursor.fetchall():
        print(f"  {row[0]:<14}{row[1]:<10}{row[2]:<13}")

def add_annotation(a_type, cursor, dbconn):
    # ask if user wants to add annotation
    add = input("\n  Would you like to add an annotation? (Y/N): ")
    while True:
        if add.lower() == 'y':
            break
        elif add.lower() == 'n':
            return
        else:
            add = input("  Invalid input. Enter Y or N: ")

    print_double_line(PAGE_LENGTH)
    
    # get annotation
    annotation = input("\n  Please enter your annotation (max 100 characters): ")
    
    if a_type == 'm': # member annotation
        # get member id
        member_id = input("\n  Please enter the member ID: ")
        member_id = is_valid_num(member_id)
        
        cursor.execute("""
        insert into m_annotations
        values(%(mid)s, %(ann)s)
        """, {'mid': member_id, 'ann': annotation})

    else: # campaign annotation
        campaign_id = input("\n  Please enter the campaign ID: ")
        campaign_id = is_valid_num(campaign_id)
        
        cursor.execute("""
        insert into c_annotations
        values(%(cid)s, %(ann)s)
        """, {'cid': campaign_id, 'ann': annotation})

    dbconn.commit()
    print_double_line(PAGE_LENGTH)

    print("\n  New annotation has been added:\n")

    view_annotations(a_type, cursor, dbconn)

def add_push(cursor, dbconn):
    print_double_line(PAGE_LENGTH)

    print("\n  Please enter the following information:\n")
    
    # get info
    push_id = input("  Push ID: ")
    content = input("  Push content: ")
    curr_time = input("  Time of push: ")

    # show campaigns
    print("\n  Select the campaign for this push: ")
    view_campaigns(cursor)

    # get campaign id
    campaign_id = input("\n  Enter your selected campaign ID: ")

    # get event id
    print("\n  Select the event for this push: ")
    view_campaign_events(cursor, campaign_id)

    # get event id
    event_id = input("\n  Enter your selected event ID: ")

    # confirm input

    # insert into web_push
    cursor.execute("""
    insert into web_push
    values (%(pid)s, %(c)s, %(t)s)
    """, {'pid': push_id, 'c': content, 't': curr_time})

    # insert into push_to
    cursor.execute("""
    insert into push_to
    values (%(eid)s, %(pid)s, %(cid)s)
    """, {'pid': push_id, 'cid': campaign_id, 'eid': event_id})

    # commit insertions
    dbconn.commit()

    print_double_line(PAGE_LENGTH)

    # view pushes
    print("\n New web push added: ")

    view_pushes(cursor)
                          
###########################
# MENU PRINTING FUNCTIONS #
###########################

def print_menu():
    # header
    print_double_line(PAGE_LENGTH)
    padding = " " * 22
    print("\n"+ padding + "WELCOME TO THE GNG DATABASE\n")
    print_single_line(PAGE_LENGTH)

    # subheader
    print('\n  What would you like to do?\n')

    # body
    padding = " " * 4
    print(padding + "S - Select and view queries\n")
    print(padding + "C - Create a new campaign\n")
    print(padding + "A - Accounting information\n")
    print(padding + "M - Membership history\n")
    print(padding + "W - Manage web pushes\n")

def print_query_menu():
    # header
    print_double_line(PAGE_LENGTH)
    padding = " " * 22
    print("\n"+ padding + "VIEW QUERIES\n")
    print_single_line(PAGE_LENGTH)

    # subheader
    print("\n  Which question would you like to pose?\n")

    # body
    padding = " " * 4
    print(padding + "1 - Which events earned more than $5 000?\n")
    print(padding + "2 - How many volunteers signed up for Rivers Reborn events?\n")
    print(padding + "3 - What is the total donation amount per donor?\n")
    print(padding + "4 - Who organized the event which raised the most money?\n")
    print(padding + "5 - Who are the employees who are not Project Managers?\n")
    print(padding + "6 - How many events have been organized by Jane Smith?\n")
    print(padding + "7 - What is the id and start date of the campaign which started most recently?\n")
    print(padding + "8 - Who are the employees who are also members of GnG?\n")
    print(padding + "9 - What is the total allocated fund for each campaign?\n")
    print(padding + "10 - How many web pushes have been sent for each campaign?\n")

def print_creator_menu():
    # header
    print_double_line(PAGE_LENGTH)
    padding = " " * 22
    print("\n"+ padding + "CREATE A NEW CAMPAIGN\n")
    print_single_line(PAGE_LENGTH)

    # subheader
    print("\n  Here is an overview of your existing campaigns:\n")

def print_acc_menu():
    # header
    print_double_line(PAGE_LENGTH)
    padding = " " * 22
    print("\n"+ padding + "ACCOUNTING INFORMATION\n")
    print_single_line(PAGE_LENGTH)

    # subheader
    print("\n  Here is an overview of your existing campaigns:\n")
    
def print_annotations_menu(cursor, dbconn):
    print_double_line(PAGE_LENGTH)
    
    # get type of annotation
    choice = input("\n  View annotations for Members (M) or Campaigns (C)? (M/C): ")

    while True:
        if choice.lower() == 'm':
            print("\n Now viewing all member annotations:\n")
            view_annotations('m', cursor, dbconn)
            add_annotation('m', cursor, dbconn)
            break
        elif choice.lower() == 'c':
            print("\n Now viewing all campaign annotations:\n")
            view_annotations('c', cursor, dbconn)
            add_annotation('c', cursor, dbconn)
            break
        else:
            choice = input("  Invalid input. Enter either M or C: ")
            
def print_membership_menu(cursor, dbconn):
    # print menu for membership history and annotations
    print("\n  M - Browse Membership History\n")
    print("  V - View Annotations\n")

    choice = input("  Please enter the letter next to your desired action: ")

    if choice.lower() == 'm':
        view_member_history(cursor)
    elif choice.lower() == 'v':
        print_annotations_menu(cursor, dbconn)
    else:
        print("  Invalid choice.")

def print_push_menu(cursor, dbconn):
    # show options
    add = input("\n  Would you like to add a new web push? (Y/N): ")

    # validate input
    while True:
        if add.lower() == 'y':
            add_push(cursor, dbconn)
            break
        elif add.lower() == 'n':
            break
        else:
            add = input("Invalid input. Please enter Y or N: ")
    
##############################                      
# PHASE EXECUTION FUNCTIONS #
#############################
     
def phase_1(cursor):
    print_query_menu()
    
    # receive input
    query_num = input('  Please enter the number next to your selected query: ')

    # validate input
    query_num = is_valid_query(query_num)

    print_double_line(PAGE_LENGTH)

    # execute the specified query
    execute_query(query_num, cursor)

def phase_2(cursor, dbconn):
    print_creator_menu()

    view_campaigns(cursor)

    print('\n  To create a new campaign, please provide the following information: \n')
    
    # get campaign info
    campaign_info = get_campaign_info()

    campaign_id = campaign_info[0]
    title = campaign_info[1]
    budget = campaign_info[2]
    start_date = campaign_info[3]
    end_date = campaign_info[4]

    # add to campaign table
    cursor.execute("""
    insert into campaign
    values (%(id)s, %(t)s, %(b)s, 'Planned', %(s_date)s, %(e_date)s)
    """, {'id': campaign_id, 't': title, 'b': budget, 's_date': start_date, 'e_date': end_date})

    dbconn.commit()

    print_double_line(PAGE_LENGTH)

    print("\n  Here is the updated overview of your campaigns: ")
    
    view_campaigns(cursor)

    print_double_line(PAGE_LENGTH)

    choice = input('\n  Would you like to schedule a new event for this campaign? (Y/N): ')

    # schedule events for campaign?
    while True:
        if choice.lower() == 'y':
            # schedule event
            schedule_event(cursor, campaign_id, dbconn)
            break

        elif choice.lower() != 'n':
            choice = input('  Invalid input. Please enter Y for yes, N for no: ')
        else:
            break

def phase_3(cursor):
    # print menu
    print_acc_menu()
    
    # view all campaigns
    view_campaigns(cursor)

    # receive input: which campaign to view funding info for
    campaign_id = input("\n  Enter the campaign ID to view accounting information for that campaign: ")
    campaign_id = is_valid_num(campaign_id)

    view_acc_info(campaign_id, cursor)

def phase_4(cursor, dbconn):
    # print header
    print_double_line(PAGE_LENGTH)
    padding = " " * 22
    print("\n"+ padding + "MEMBERSHIP HISTORY\n")
    print_single_line(PAGE_LENGTH)
    
    # subheader
    print("\n  Here are all the members who currently exist in the database:\n")

    # show member table
    view_members(cursor)

    # print options menu
    print_membership_menu(cursor, dbconn)

def phase_5(cursor, dbconn):
    # print header
    print_double_line(PAGE_LENGTH)
    padding = " " * 22
    print("\n"+ padding + "WEB PUSH HISTORY\n")
    print_single_line(PAGE_LENGTH)
    
    # subheader
    print("\n Viewing all web push history:\n")

    # show web push table
    view_pushes(cursor)

    # print options menu
    print_push_menu(cursor, dbconn)
    
def execute_action(choice, cursor, dbconn):
    while True:
        if choice.lower() == 's':
            phase_1(cursor)
            return
        elif choice.lower() == 'c':
            phase_2(cursor, dbconn)
            return
        elif choice.lower() == 'a':
            phase_3(cursor)
            return
        elif choice.lower() == 'm':
            phase_4(cursor, dbconn)
            return
        elif choice.lower() == 'w':
            phase_5(cursor, dbconn)
            return
        else:
            choice = input('  Invalid input. Please enter a valid letter: ')

def main():
    # establish connection
    dbconn = psycopg2.connect(host='studentdb.csc.uvic.ca', user='c370_s147', password='HuVgCRfV')

    # set cursor
    cursor = dbconn.cursor()
    
    while True:
    
        # print main menu
        print_menu()

        # receive desired action from user
        choice = input('  Please enter the letter next to your desired action: ')

        # execute desired action
        execute_action(choice, cursor, dbconn)
    
        print_double_line(PAGE_LENGTH)

        # check if exiting
        stay = input("\n Enter Q to quit/any other key to stay: ")
        if stay.lower() == 'q':
            break
    
    print_double_line(PAGE_LENGTH)

    # close cursor and connection
    cursor.close()
    dbconn.close()

if __name__ == "__main__": main()
    
