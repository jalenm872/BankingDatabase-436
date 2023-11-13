create database banking_database;

use banking_database;

# Bank Department Table

create table bank_department(
location varchar(50),
name varchar(25),
department_id int
);


insert into bank_department(department_id,location, name) values(2819, '54 Sycamore Lane, Lincoln NE 3829', 'Peoples Bank');
insert into bank_department(department_id,location, name) values(9238, '128 Spring Street, Boston MA 2812', 'Bank of Massachusett');
insert into bank_department(department_id,location, name) values(7262, NULL, 'Autumn Bank');
insert into bank_department(department_id,location, name) values(0972,'72 King Avenue, Warwick RI 0928', 'Rhode Island Bank');
insert into bank_department(department_id,location, name) values(71897,'72 King Avenue, Albany NY 1872', 'Big Bank');

#Branch Table

create table bank_branches(
branch_name varchar(32),
branch_id int primary key,
branch_city varchar(32),
department_id int
);

insert into bank_branches(branch_name, branch_id, branch_city, department_id) values('Boston Branch', 1, 'Boston, MA',9238);
insert into bank_branches(branch_name, branch_id, branch_city, department_id) values('Rochester Branch', 2, 'Rochester, NY',71897);
insert into bank_branches(branch_name, branch_id, branch_city, department_id) values('Chicago Branch', 3, 'Chicago, IL',2819);
insert into bank_branches(branch_name, branch_id, branch_city, department_id) values('Houston Branch', 4, 'Houston, TX',2819);
insert into bank_branches(branch_name, branch_id, branch_city, department_id) values('Providence Branch', 5, 'Providence, RI',0972);

#Accounts table

create table accounts(
account_number int primary key,
account_type varchar(32),
balance float,
routing_number varchar(16),
department_id int
);

insert into accounts(account_number, account_type, balance, routing_number, department_id) values (12345, 'Checking', 2500.00, '1234123412341234', 9238);
insert into accounts(account_number, account_type, balance, routing_number, department_id) values (54321, 'Savings',10500 , '4321432143214321', 71897);
insert into accounts(account_number, account_type, balance, routing_number, department_id) values (11234, 'Checking', 1250.00, '1123112311231123', 71897);
insert into accounts(account_number, account_type, balance, routing_number, department_id) values (23456, 'Checking', 900.00, '2345234523452345', 2819);
insert into accounts(account_number, account_type, balance, routing_number, department_id) values (34567, 'Savings', 99000.00, '3456345634563456', 71897);


#Loans table


create table loans(
loan_type varchar(15),
loan_id int primary key,
interest float,
amount int,
duration int #years
);


insert into loans(loan_type, loan_id, interest, amount, duration) values ('Home', 1, .07, 60000, 30);
insert into loans(loan_type, loan_id, interest, amount, duration) values ('Personal',2, .25, 5000, 5);
insert into loans(loan_type, loan_id, interest, amount, duration) values ('Personal',3, .32, 8000, 6);
insert into loans(loan_type, loan_id, interest, amount, duration) values ('Personal',4, .28, 27000, 3);
insert into loans(loan_type, loan_id, interest, amount, duration) values ('Auto', 5, .067, 22000, 6);

create table customers(
customer_name varchar(32),
credit_score int,
customer_id int primary key,
address varchar(45),
state varchar(25),
account_number int,
age int check(age>=18),
INDEX get_credit(credit_score)
);

insert into customers(customer_name, credit_score, customer_id, address, state, account_number, age) values ('John Smith', 720, 1, '223 North Street, South City RI 92832', 'RI', 12345, 36);
insert into customers(customer_name, credit_score, customer_id, address, state, account_number, age) values ('Kate Williams', 540, 2, '19 West Avenue, Springfield CT 82819', 'CT', 54321, 23);
insert into customers(customer_name, credit_score, customer_id, address, state, account_number,age) values ('Kyle Richards', 652, 3, '56 Pine Lane, Franklin MA 02817', 'MA', 11234, 48);
insert into customers(customer_name, credit_score, customer_id, address, state, account_number,age) values ('Sandra Anderson', 421, 4, '92 Sycamore Street, Providence RI 99212','RI', 23456,63);
insert into customers(customer_name,credit_score, customer_id, address, state, account_number,age) values ('Richard Gonzales', 680, 5, '128 King Street, Rochester NY 98172','NY', 34567,28);
insert into customers(customer_name,credit_score, customer_id, address, state, account_number,age) values ('John Peterson', NULL, 6, '52 Queen Ave, Lincoln NE 28172','NE', NULL,17);

create table user_info(
username varchar(32),
password varchar(32),
customer_id int,
account_number int,
primary key(username),
foreign key(customer_id) references customers(customer_id),
foreign key(account_number) references accounts(account_number)
); 

insert into user_info(username, password, customer_id, account_number) values ('johnsmith', 'password', 1, 12345);