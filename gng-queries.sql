-- 1: Which events earned more than $5 000?
drop view Q1;
create view Q1 as
    select type, amnt_raised
    from Event
    where amnt_raised > 5000.00;

-- 2: How many volunteers signed up for Rivers Reborn events? (join) (aggr)
drop view Q2;
create view Q2 as
    select count(*) as num_volunteers
    from Volunteers
    join Event on Volunteers.event_id = Event.event_id and Volunteers.campaign_id = Event.campaign_id
    join Campaign on Volunteers.campaign_id = Campaign.campaign_id
    where Campaign.title = 'Rivers Reborn: Restoring Aquatic Ecosystems';

-- 3: What is the total donation amount per donor? (join) (grouping)
drop view Q3;
create view Q3 as
    select Donor.donor_id, Donor.name, sum(amount) as total_donation
    from Donor
    left join Donates on Donor.donor_id = Donates.donor_id
    group by Donor.donor_id, Donor.name;

-- 4: Who organized the event which raised the most money? (subquery as scalar) (aggr) (join)
drop view Q4;
create view Q4 as
    select Employee.name as employee, Employee.employee_id
    from Event
        join Organizes on Event.event_id = Organizes.event_id and Event.campaign_id = Organizes.campaign_id
        join Employee on Organizes.employee_id = Employee.employee_id
    where Event.amnt_raised = (select max(amnt_raised) from Event);

-- 5: Who are the employees who are not Project Managers? (set operation)
drop view Q5;
create view Q5 as
    (select name, employee_id
    from Employee)
    except
    (select name, employee_id
    from Employee
    where position = 'Project Manager');

-- 6: How many events have been organized by Jane Smith? (subquery) (aggr)
drop view Q6;
create view Q6 as
    select count(*) as total_events
    from Organizes
    where employee_id in (
        select employee_id
        from Employee
        where name = 'Jane Smith');

    
-- 7: What is the id and start date of the campaign which started most recently? (all)
drop view Q7;
create view Q7 as
    select campaign_id, start_date
    from Campaign
    where start_date >= all (
        select start_date
        from Campaign);

-- 8: Who are the employees who are also members of GnG? (any)
drop view Q8;
create view Q8 as
    select Employee.name, Employee.employee_id
    from Employee
    where Employee.name = any (select Member.name
                               from Member
                               where Member.name = Employee.name) and 
          Employee.phone = any (select Member.phone
                               from Member
                               where Member.phone = Employee.phone);

-- 9: What is the total allocated fund for each campaign?
drop view Q9;
create view Q9 as
    select Campaign.campaign_id, sum(Allocation.amount) as total_allocated_funds
    from Campaign
    left join Funds on Campaign.campaign_id = Funds.campaign_id
    left join Allocation on Funds.allocation_id = Allocation.allocation_id
    group by Campaign.campaign_id;

    
-- 10: How many web pushes were sent for each campaign?
drop view Q10;
create view Q10 as
    select Event.campaign_id, count(*) as total_web_pushes
    from Event
    join Push_to on Event.event_id = Push_to.event_id and Event.campaign_id = Push_to.campaign_id
    group by Event.campaign_id;


select * from Q1;
select * from Q2;
select * from Q3;
select * from Q4;
select * from Q5;
select * from Q6;
select * from Q7;
select * from Q8;
select * from Q9;
select * from Q10;
