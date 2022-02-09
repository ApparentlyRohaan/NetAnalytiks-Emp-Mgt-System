CREATE TABLE users( id integer primary key AUTOINCREMENT, name text not null, password text not null, admin boolean not null DEFAULT '0');
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE empmasterdata ( slno INTEGER PRIMARY KEY AUTOINCREMENT,empid varchar(50), name text NOT NULL, location text, startdate DATE);
CREATE TABLE empadddata (empid varchar(50), name text NOT NULL, ctc INTEGER(20), billable text, costcodes  INTEGER(20));
CREATE TABLE billingmasterdata (empid varchar(50), name text NOT NULL, clientname text, startdate DATE, billrate INTEGER(20));
CREATE TABLE costcodes ( costcodes INTEGER PRIMARY KEY, deparment text );
CREATE TABLE sowdetails (clientname text, year year, signeddata text,sowdescription text,sowamount INTEGER(20));
CREATE TABLE monthlyexp (type_m text, description_m text, amount_m INTEGER(20) );
CREATE TABLE yearlyexp (type_y text, description_y text, amount_y INTEGER(20) );
CREATE TABLE billingdetails (empid varchar(50), name text NOT NULL, month text, year year,sowdescription text, amount INTEGER(20),noofdays INTEGER(20),noofhours INTEGER(20));


