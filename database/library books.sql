drop database library;
create database library;
use library;


create table admin(
	admin_id int auto_increment primary key,
	username varchar(255) not null,
	password varchar(255) not null
);

insert into admin(username,password) values('admin', 'admin');

create table location(
	location_id int auto_increment primary key,
	location_name varchar(255) not null unique
);

create table librarian(
	librarian_id int auto_increment primary key,
	name varchar(255) not null,
    phone varchar(255) not null unique,
	email varchar(255) not null unique,
	password varchar(255) not null,
	address varchar(255) not null,
	location_id  int not null,
    foreign key(location_id)references location(location_id)
);

create table student(
	student_id int auto_increment primary key,
	name varchar(255) not null,
	email varchar(255) not  null unique,
    password varchar(255) not null unique,
	phone varchar(255) not null unique,
	address varchar(255) not null,
	gender varchar(255) not null,
	dob varchar(255) not null 
); 

create table  book_categories(
	book_category_id int auto_increment primary key,
	book_category_name varchar(255) not  null
);

create table books(
book_id int auto_increment primary key,
book_title varchar(255) not null,
author varchar(255) not null,
year varchar(255) not null,
description text,
picture  varchar(255),
book_category_id int  not  null,
foreign key(book_category_id) references book_categories(book_category_id)
);


create table book_copies(
	book_copy_id int auto_increment primary key,
	book_copy_number varchar(255) not null,
	book_id int not null,
	librarian_id int not null,
    status varchar(255) default 'Available',
	foreign key(book_id)references books(book_id),
	foreign key(librarian_id)references librarian(librarian_id)
);



create table borrowings(
borrowing_id int auto_increment primary key,
status varchar(255) default 'Book Requested',
date datetime default CURRENT_TIMESTAMP,
return_date datetime,
fine int ,
student_id int not null,
librarian_id int not null,
book_id int not null,
book_copy_id int,
assigned_date datetime,
foreign key(student_id)references student(student_id),
foreign key(librarian_id)references librarian(librarian_id),
foreign key(book_id)references books(book_id),
foreign key(book_copy_id)references book_copies(book_copy_id)
);
