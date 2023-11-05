CREATE TABLE Game (
    name varchar(40) not null,
    Genre varchar(20) not null,
    Year int(4) not null,
    Platform  varchar(20),
    Mode varchar(20) not null,
    Publisher varchar(20),
    Developer varchar(20) not null
);
CREATE TABLE Platform (
    name varchar(40) not null,
    Price decimal(10,2) not null,
    Manufacturer  varchar(100) not null
);
CREATE TABLE Publisher (
    name varchar(40) not null,
    Country varchar(40) not null,
    Type varchar(40) not null
);
CREATE TABLE Developer (
    name varchar(40) not null,
    country varchar(40) not null,
    type varchar(40) not null,
    Founded int(4)
);
CREATE TABLE Store (
    name varchar(40) not null,
    Location varchar(40) not null,
    Game varchar(40) not null,
    number_of_copies int(40) not null,
    Form_of_copy varchar(40) not null,
    price decimal(10,2) not null
);
CREATE TABLE Customer (
    name varchar(40) not null,
    amount  decimal(8,0) not null,
    location varchar(40) not null,
    customer_id  decimal(8,0) not null
);
CREATE TABLE employee (
    name varchar(40) not null,
    employee_id decimal(8,0) not null,
    store_location varchar(40) not null
);
