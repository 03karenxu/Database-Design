drop table Campaign cascade;
create table Campaign(
    campaign_id     serial primary key,
    title           char(80),
    cost            numeric,
    status          char(20),
    start_date      date,
    end_date        date
);

insert into Campaign values (100, 'Rivers Reborn: Restoring Aquatic Ecosystems', 50000, 'In progress', '2024-03-01', '2024-05-01');
insert into Campaign values(101, 'Green Canopy Initiative: Planting Trees for Tomorrow', 100000, 'Planned', '2024-06-01', '2025-05-31');
insert into Campaign values(102, 'Ocean Guardians: Protecting Marine Sanctuaries', 75000, 'Completed', '2024-03-15', '2024-12-15');
insert into Campaign values(103, 'Air Purity Project: Breathing Life into Cities', 80000, 'In progress', '2024-07-01', '2025-06-30');
insert into Campaign values(104, 'Wildlife Watch: Preserving Habitats, Saving Species', 60000, 'Planned', '2024-05-01', '2025-10-30');
insert into Campaign values(105, 'Sustainable Seas: A Call to Action for Clean Oceans', 90000, 'Completed', '2024-04-15', '2025-03-15');

drop table Event cascade;
create table Event(
    campaign_id     serial,
    event_id        serial,
    location        char(40),
    type            char(30),
    date_time       timestamp(2),
    amnt_raised     numeric default 0.00,
    primary key(event_id, campaign_id),
    foreign key (campaign_id) references Campaign(campaign_id)
);

insert into Event values(100, 01, 'River Park, Victoria', 'Fundraising Gala', '2024-03-15 18:00:00', 5000.00);
insert into Event values(100, 02, 'Waterfront Pavilion, Victoria', 'Volunteer Cleanup', '2024-04-05 09:00:00', NULL);
insert into Event values(101, 01, 'City Arboretum, Nanaimo', 'Tree Planting Workshop', '2024-06-10 14:00:00', 2000.00);
insert into Event values(101, 02, 'Community Center, Parksville', 'Educational Seminar', '2024-07-20 10:30:00', NULL);
insert into Event values(102, 01, 'Marine Research Institute, Tofino', 'Public Exhibition', '2024-03-25 11:00:00', 8000.00);
insert into Event values(103, 01, 'Downtown Plaza, Victoria', 'Air Quality Awareness Day', '2024-07-05 12:00:00', NULL);
insert into Event values(104, 01, 'National Park, Nanaimo', 'Wildlife Photography Tour', '2024-05-15 08:00:00', 3000.00);
insert into Event values(105, 01, 'Coastal Center, Victoria', 'Beach Cleanup Event', '2024-04-20 09:30:00', 6000.00);

drop table Member cascade;
create table Member(
    member_id       serial primary key,
    name            char(30),
    phone           char(16),
    email           char(30),
    start_date      timestamp(2)
);

insert into Member values (1001, 'Alice Johnson', '555-1234', 'alice@example.com', '2023-12-10 08:00:00');
insert into Member values (1002, 'Bob Smith', '555-5678', 'bob@example.com', '2024-01-05 09:30:00');
insert into Member values (1003, 'Charlie Brown', '555-9012', 'charlie@example.com', '2024-02-20 11:15:00');
insert into Member values (1004, 'David Lee', '555-3456', 'david@example.com', '2024-03-10 13:45:00');
insert into Member values (1005, 'Emily Davis', '555-7890', 'emily@example.com', '2024-04-15 15:00:00');
insert into Member values (1006, 'Frank Wilson', '555-2345', 'frank@example.com', '2024-05-20 16:30:00');
insert into Member values (1007, 'Grace Taylor', '555-6789', 'grace@example.com', '2024-06-25 18:00:00');

drop table Volunteer cascade;
create table Volunteer(
    member_id       serial primary key,
    name            char(30),
    phone           char(16),
    email           char(30),
    start_date      timestamp(2),
    tier            char(10),
    times_vol       int,
    foreign key (member_id) references Member(member_id)
);

insert into Volunteer values (1001, 'Alice Johnson', '555-1234', 'alice@example.com', '2023-12-10 08:00:00', 'Junior', 1);
insert into Volunteer values (1002, 'Bob Smith', '555-5678', 'bob@example.com', '2024-01-05 09:30:00', 'Senior', 10);
insert into Volunteer values (1003, 'Charlie Brown', '555-9012', 'charlie@example.com', '2024-02-20 11:15:00', 'Junior', 2);
insert into Volunteer values (1004, 'David Lee', '555-3456', 'david@example.com', '2024-03-10 13:45:00', 'Junior', 1);
insert into Volunteer values (1005, 'Emily Davis', '555-7890', 'emily@example.com', '2024-04-15 15:00:00', 'Senior', 5);
insert into Volunteer values (1007, 'Grace Taylor', '555-6789', 'grace@example.com', '2024-06-25 18:00:00', 'Junior', 1);

drop table Web_push cascade;
create table Web_push(
    push_id            serial primary key,
    content            char(80),
    time_of_push       timestamp(2)
);

insert into Web_push values (1, 'Campaign "Rivers Reborn" launched!', '2024-03-18 08:00:00');
insert into Web_push values (2, 'Join our Volunteer cleanup for "Green Canopy Initiative"', '2024-03-18 12:30:00');
insert into Web_push values (3, 'Update: "Ocean Guardians" Event rescheduled', '2024-03-18 15:45:00');
insert into Web_push values (4, 'Reminder: "Air Purity Project" community meeting tomorrow', '2024-03-19 09:15:00');

drop table Employee cascade;
create table Employee(
    employee_id     serial primary key,
    name            char(20),
    phone           char(16),
    email

           char(30),
    start_date      timestamp(2),
    position        char(30),
    salary          real
);

insert into Employee values (2001, 'John Doe', '555-1234', 'john.doe@example.com', '2023-12-10 08:00:00', 'Project Manager', 65000.00);
insert into Employee values (2002, 'Jane Smith', '555-5678', 'jane.smith@example.com', '2024-01-05 09:30:00', 'Project Manager', 65000.00);
insert into Employee values (2003, 'Michael Johnson', '555-9012', 'michael.johnson@example.com', '2024-02-20 11:15:00', 'Project Manager', 65000.00);
insert into Employee values (2004, 'Emily Davis', '555-3456', 'emily.davis@example.com', '2024-03-10 13:45:00', 'Marketing Specialist', 60000.00);
insert into Employee values (2005, 'Alex Wilson', '555-7890', 'alex.wilson@example.com', '2024-04-15 15:00:00', 'HR Manager', 60000.00);

drop table Office cascade;
create table Office(
    address         char(40) primary key,
    rent_amount     numeric,
    rent_due        timestamp(2)
);

insert into Office values ('123 Main Street, Suite 100', 2000.00, '2024-03-18 12:00:00');

drop table Donor cascade;
create table Donor(
    donor_id        serial primary key,
    name            char(30),
    phone           char(16),
    email           char(40),
    address         char(40)
);

insert into Donor values (3001, 'Green Earth Foundation', '555-1234', 'contact@greenearthfoundation.org', '123 Park Avenue');
insert into Donor values (3002, 'Ocean Preservation Fund', '555-5678', 'info@oceanpreservationfund.org', '456 Ocean Boulevard');
insert into Donor values (3003, 'Wildlife Conservation Society', '555-9012', 'support@wildlifeconservation.org', '789 Jungle Way');
insert into Donor values (3004, 'Clean Energy Initiative', '555-3456', 'info@cleanenergyinitiative.org', '1011 Solar Street');
insert into Donor values (3005, 'Community Health Alliance', '555-7890', 'contact@communityhealthalliance.org', '1213 Wellness Drive');

drop table Fund cascade;
create table Fund(
    fund_id   serial primary key,
    name      char(40),
    amount    numeric
);

insert into Fund values (1, 'Environmental Conservation Fund', 500000.00);
insert into Fund values (2, 'Wildlife Protection Fund', 300000.00);
insert into Fund values (3, 'Operations Fund', 2000000.00);

drop table Allocation cascade;
create table Allocation(
    allocation_id   serial primary key,
    amount          numeric,
    date_time       timestamp(2)
);

insert into Allocation values (201, 65000.00, '2022-01-18 10:00:00');
insert into Allocation values (202, 50000.00, '2023-09-19 11:30:00');
insert into Allocation values (203, 2000.00, '2024-03-01 09:45:00');
insert into Allocation values (204, 65000.00, '2024-03-18 11:00:00');
insert into Allocation values (205, 100000.00, '2024-03-18 12:00:00');
insert into Allocation values (206, 65000.00, '2024-03-18 12:00:00');
insert into Allocation values (207, 60000.00, '2024-03-18 12:00:00');
insert into Allocation values (208, 60000.00, '2024-03-18 12:00:00');

drop table Funds cascade;
create table Funds(
    allocation_id  serial,
    campaign_id    serial,
    primary key(allocation_id, campaign_id),
    foreign key (allocation_id) references Allocation(allocation_id),
    foreign key (campaign_id) references Campaign(campaign_id)
);

insert into Funds values (201, 100);
insert into Funds values (202, 101);
insert into Funds values (203, 102);

drop table Participates cascade;
create table Participates(
    member_id      serial,
    campaign_id    serial,
    primary key(member_id, campaign_id),
    foreign key (member_id) references Member(member_id),
    foreign key (campaign_id) references Campaign(campaign_id)
);

insert into Participates values (1001, 100);
insert into Participates values (1002, 101);
insert into Participates values (1003, 102);

drop table Volunteers cascade;
create table Volunteers(
    member_id      int,
    event_id       int,
    campaign_id    int,
    primary key (member_id, event_id, campaign_id),
    foreign key (member_id) references Member(member_id),
    foreign key (event_id, campaign_id) references Event(event_id, campaign_id)
);

insert into Volunteers values (1001, 01, 100);
insert into Volunteers values (1002, 01, 100);
insert into Volunteers values (1001, 02, 100);
insert into Volunteers values (1003, 02, 100);
insert into Volunteers values (1005, 01, 101);
insert into Volunteers values (1006, 02, 101);
insert into Volunteers values (1004, 01, 102);
insert into Volunteers values (1003, 02, 101);
insert into Volunteers values (1002, 01, 103);
insert into Volunteers values (1001, 01, 103);
insert into Volunteers values (1005, 01, 104);
insert into Volunteers values (1006, 01, 105);

drop table Push_to cascade;
create table Push_to(
    event_id      int,
    push_id       int primary key,
    campaign_id   int,
    foreign key (event_id, campaign_id) references Event(event_id, campaign_id),
    foreign key (push_id) references Web_push(push_id)
);

insert into Push_to values (01, 1, 100);
insert into Push_to values (02, 2, 101);
insert into Push_to values (01, 3, 102);
insert into Push_to values (01, 4, 102);

drop table Organizes cascade;
create table Organizes(
    employee_id    int,
    event_id       int,
    campaign_id    int,
    primary key (employee_id, event_id, campaign_id),
    foreign key (employee_id) references Employee(employee_id),
    foreign key (event_id, campaign_id) references Event(event_id, campaign_id)
);

insert into Organizes values (2001, 01, 100);
insert into Organizes values (2001, 02, 100);
insert into Organizes values (2002, 01, 101);
insert into Organizes values (2002, 02, 101);
insert into Organizes values (2003, 01, 102);
insert into Organizes values (2003, 01, 103);
insert into Organizes values (2003, 01, 104);
insert into Organizes values (2003, 01, 105);

drop table Works_at cascade;
create table Works_at(
    employee_id    serial,
    address        char(40),
    primary key (employee_id, address),
    foreign key (address) references Office(address),
    foreign key (employee_id) references Employee(employee_id)
);

insert into Works_at values (2001, '123 Main Street, Suite 100');
insert into Works_at values (2002, '123 Main Street, Suite 100');
insert into Works_at values (2003, '123 Main Street, Suite 100');
insert into Works_at values (2004, '123 Main Street, Suite 100');
insert into Works_at values (2005, '123 Main Street, Suite 100');

drop table Pays_rent cascade;
create table Pays_rent(
    allocation_id   serial,
    address         char(40),
    primary key (allocation_id, address),
    foreign key (allocation_id) references Allocation(allocation_id),
    foreign key (address) references Office(address)
);

insert into Pays_rent values (203, '123 Main Street, Suite 100');

drop table Pays_salary cascade;
create table Pays_salary(
    allocation_id  serial,
    employee_id    serial,
    primary key (employee_id, allocation_id),
    foreign key (employee_id) references Employee(employee_id),
    foreign key (allocation_id) references Allocation(allocation_id)
);

insert into Pays_salary values (201, 2001);
insert into Pays_salary values (204, 2002);
insert into Pays_salary values (206, 2003);
insert into Pays_salary values (207, 2004);
insert into Pays_salary values (208, 2005);

drop table Donates cascade;
create table Donates(
    donor_id      serial,
    fund_id       serial,
    amount        numeric,
    date_time     timestamp,
    primary key (donor_id, date_time),
    foreign key (donor_id) references Donor(donor_id),
    foreign key (fund_id) references Fund(fund_id)
);

insert into Donates values (3001, 1, 10000.00, '2021-03-18 10:00:00');
insert into Donates values (3002, 2, 20000.00, '2022-03-18 10:00:00');
insert into Donates values (3003, 2, 10000.00, '2022-09-18 10:00:00');
insert into Donates values (3004, 3, 15000.00, '2022-10-18 10:00:00');
insert into Donates values (3005, 3, 8000.00, '2023-03-18 10:00:00');
insert into Donates values (3005, 1, 5000.00, '2023-03-18 11:00:00');

drop table Leads cascade;
create table Leads(
    employee_id serial,
    campaign_id serial,
    primary key (employee_id, campaign_id),
    foreign key (employee_id) references Employee(employee_id),
    foreign key (campaign_id) references Campaign(campaign_id)
);

insert into Leads values (2001, 100);
insert into Leads values (2002, 101);
insert into Leads values (2001, 102);
insert into Leads values (2003, 103);
insert into Leads values (2004, 104);
insert into Leads values (2005, 105);

drop table Allocates cascade;
create table Allocates(
    fund_id         serial,
    allocation_id   serial primary key,
    foreign key (fund_id) references Fund(fund_id),
    foreign key (allocation_id) references Allocation(allocation_id)
);

insert into Allocates values (3, 201);
insert into Allocates values (3, 203);
insert into Allocates values (3, 204);
insert into Allocates values (1, 202);
insert into Allocates values (2, 205);
insert into Allocates values (3, 206);
insert into Allocates values (3, 207);
insert into Allocates values (3, 208);

drop table M_annotations cascade;
create table M_annotations (
    member_id    serial,
    annotation   char(100),
    primary key (member_id, annotation)
);

drop table C_annotations cascade;
create table C_annotations (
    campaign_id   serial,
    annotation    char(100),
    primary key (campaign_id, annotation)
);