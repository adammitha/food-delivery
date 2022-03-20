CREATE TABLE Driver (
	driver_id integer,
	first_name char(50),
    last_name char(50),
	drivers_license_number integer,
	PRIMARY KEY (driver_id),
	UNIQUE (drivers_license_number)
);

INSERT INTO Driver(driver_id, first_name, last_name, drivers_license_number)
    VALUES (1, 'Raymond', 'Ng', 123456);   
INSERT INTO Driver(driver_id, first_name, last_name, drivers_license_number)
    VALUES (2, 'Norm', 'Hutchinson', 867530);   
INSERT INTO Driver(driver_id, first_name, last_name, drivers_license_number)
    VALUES (3, 'Randy', 'Jackson', 456901);
INSERT INTO Driver(driver_id, first_name, last_name, drivers_license_number)
    VALUES (4, 'Paul', 'Walker', 987654);
INSERT INTO Driver(driver_id, first_name, last_name, drivers_license_number)
    VALUES (5, 'Ben', 'Simmons', 554327);
    

CREATE TABLE VehicleDrives (
    license_plate char(20),
    vehicle_color char(20),
    vehicle_model char(20),
    vehicle_make char(20),
    distance integer,
    driver_id integer NOT NULL,
    PRIMARY KEY (license_plate),
    FOREIGN KEY (driver_id) REFERENCES Driver
);

INSERT INTO VehicleDrives(license_plate, vehicle_color, vehicle_model, vehicle_make, distance, driver_id)
    VALUES('123 BCF', 'Blue', 'Camry', 'Toyota', 1254, 2);
INSERT INTO VehicleDrives(license_plate, vehicle_color, vehicle_model, vehicle_make, distance, driver_id)
    VALUES('420 HGT', 'Grey', 'Civic', 'Honda', 2342, 1);
INSERT INTO VehicleDrives(license_plate, vehicle_color, vehicle_model, vehicle_make, distance, driver_id)
    VALUES('502 FRG', 'Black', '911', 'Porsche', 129, 3);
INSERT INTO VehicleDrives(license_plate, vehicle_color, vehicle_model, vehicle_make, distance, driver_id)
    VALUES('786 TRD', 'White', 'Mustang', 'Ford', 5476, 5);
INSERT INTO VehicleDrives(license_plate, vehicle_color, vehicle_model, vehicle_make, distance, driver_id)
    VALUES('143 DSE', 'Red', 'Camaro', 'Chevrolet', 1029, 4);



CREATE TABLE City(
	postal_code char(6), 
	city char(30),
	PRIMARY KEY (postal_code)
);

INSERT INTO City(postal_code, city)
    VALUES  ("60185", "West Chicago");
INSERT INTO City(postal_code, city)
    VALUES  ("60174", "St. Charles");
INSERT INTO City(postal_code, city)
    VALUES  ("60103", "Bartlett");
INSERT INTO City(postal_code, city)
    VALUES  ("V9L4G8", "Vancouver");
INSERT INTO City(postal_code, city)
    VALUES  ("V3K9G2", "Vancouver");


CREATE TABLE Address (
	address_id integer,
	unit_number integer,
	street_number integer,
	street_name char(50),
	postal_code char(6),
    neighbourhood char(50), 
    PRIMARY KEY (address_id),
    FOREIGN KEY (postal_code) REFERENCES City
);

INSERT INTO Address(address_id, unit_number, street_number, street_name, postal_code, neighbourhood)
    VALUES (1234, NULL, 2922, "Stockberry Street", "60185", "Lincoln Park");
INSERT INTO Address(address_id, unit_number, street_number, street_name, postal_code, neighbourhood)
    VALUES (5432, 14, 1010, "Lemon Lane", "60174", "Gold Coast");
INSERT INTO Address(address_id, unit_number, street_number, street_name, postal_code, neighbourhood)
    VALUES (2134, NULL, 321, "Watermelon Dr", "60103", "Chinatown");
INSERT INTO Address(address_id, unit_number, street_number, street_name, postal_code, neighbourhood)
    VALUES (8674, NULL, 394, "Alma Street", "V9L4G8", "Kitsilano");
INSERT INTO Address(address_id, unit_number, street_number, street_name, postal_code, neighbourhood)
    VALUES (2546, 21, 785, "Georgia Street", "V3K9G2", "Downtown");


CREATE TABLE Restaurant (
    restaurant_id integer,
	restaurant_name char(20),
	cuisine char(20),
	address_id integer,
	business_license_number integer,
	PRIMARY KEY (restaurant_id),
	FOREIGN KEY (address_id) REFERENCES Address
);

INSERT INTO Restaurant(restaurant_id, restaurant_name, cuisine, address_id, business_license_number)
    VALUES (1, "Sushi Town", "Japanese", 2546, 355342);
INSERT INTO Restaurant(restaurant_id, restaurant_name, cuisine, address_id, business_license_number)
    VALUES (2, "Mumu's", "Korean", 8674, 134636);
INSERT INTO Restaurant(restaurant_id, restaurant_name, cuisine, address_id, business_license_number)
    VALUES (3, "Dario's", "Italian", 5432, 123434);
INSERT INTO Restaurant(restaurant_id, restaurant_name, cuisine, address_id, business_license_number)
    VALUES (4, "Le Crocodile", "French", 2546, 785423);
INSERT INTO Restaurant(restaurant_id, restaurant_name, cuisine, address_id, business_license_number)
    VALUES (5, "KFC", "American", 8674, 422356);


CREATE TABLE Customer (
	customer_id integer,
	addressID int,
	first_name char(50),
    last_name char(50),
	PRIMARY KEY (customer_id),
	FOREIGN KEY (addressID) REFERENCES Address
);

INSERT INTO Customer(customer_id, addressID, first_name, last_name) 
    VALUES (11, 1234, "John", "Cena");
INSERT INTO Customer(customer_id, addressID, first_name, last_name) 
    VALUES (22, 1234, "Rey", "Mysterio");
INSERT INTO Customer(customer_id, addressID, first_name, last_name) 
    VALUES (33, 5432, "Brock", "Lesnar");
INSERT INTO Customer(customer_id, addressID, first_name, last_name) 
    VALUES (44, 5432, "Dwayne", "Johnson");
INSERT INTO Customer(customer_id, addressID, first_name, last_name) 
    VALUES (55, 5432, "Dave", "Bautista");


CREATE TABLE DeliveryReceivesMakes (
    delivery_id integer, 
    location_from integer,
    location_to integer,
    cost real,
    delivery_priority char(20),
    customer_id integer NOT NULL,
    driver_id integer NOT NULL,
    delivery_timestamp datetime,
    PRIMARY KEY (delivery_id),
    FOREIGN KEY (customer_id) REFERENCES Customer,
    FOREIGN KEY (location_to) REFERENCES Address(address_id),
    FOREIGN KEY (location_from) REFERENCES Address(address_id)
);

INSERT INTO DeliveryReceivesMakes(delivery_id, location_from, location_to, cost, delivery_priority, customer_id, driver_id, delivery_timestamp)
    VALUES (1, 1234, 5432, 200, 'High', 11, 3, "2022-01-08 12:35:29");
INSERT INTO DeliveryReceivesMakes(delivery_id, location_from, location_to, cost, delivery_priority, customer_id, driver_id, delivery_timestamp)
    VALUES (2, 2134, 8674, 150, 'Medium', 22, 2, "2022-01-10 1:14:43");
INSERT INTO DeliveryReceivesMakes(delivery_id, location_from, location_to, cost, delivery_priority, customer_id, driver_id, delivery_timestamp)
    VALUES (3, 2456, 2134, 250, 'High', 33, 5, "2022-02-12 14:33:15");
INSERT INTO DeliveryReceivesMakes(delivery_id, location_from, location_to, cost, delivery_priority, customer_id, driver_id, delivery_timestamp)
    VALUES (4, 5674, 1234, 45, 'Low', 44, 1, '2022-02-28 2:35:59');
INSERT INTO DeliveryReceivesMakes(delivery_id, location_from, location_to, cost, delivery_priority, customer_id, driver_id, delivery_timestamp)
    VALUES (5, 5432, 5674, 25, 'Low', 55, 4, "2022-03-01 10:06:09");


CREATE TABLE DependentHas(
	dependent_id integer,
	customer_id integer NOT NULL,
	dependent_first_name char(50),
    dependent_last_name char(50),
	allocated_budget real,
	PRIMARY KEY (dependent_id, customer_id),
	FOREIGN KEY (customer_id) REFERENCES Customer ON DELETE CASCADE
);

INSERT INTO DependentHas(dependent_id, customer_id, dependent_first_name, dependent_last_name, allocated_budget)
    VALUES (100, 11, 'Stephen', 'Curry', 100);
INSERT INTO DependentHas(dependent_id, customer_id, dependent_first_name, dependent_last_name, allocated_budget)
    VALUES (101, 22, 'Lebron', 'James', 550);
INSERT INTO DependentHas(dependent_id, customer_id, dependent_first_name, dependent_last_name, allocated_budget)
    VALUES (102, 33, 'Fred', 'VanVleet', 60);
INSERT INTO DependentHas(dependent_id, customer_id, dependent_first_name, dependent_last_name, allocated_budget)
    VALUES (103, 44, 'Lamar', 'Odom', 45);
INSERT INTO DependentHas(dependent_id, customer_id, dependent_first_name, dependent_last_name, allocated_budget)
    VALUES (100, 55, 'Delonte', 'West', 10);

CREATE TABLE OrderTakesHas(
	order_id integer,
	total real,
	tip real,
	order_timestamp datetime,
	restaurant_id integer NOT NULL,
	customer_id integer NOT NULL,
	PRIMARY KEY (order_id),
	FOREIGN KEY (restaurant_id) REFERENCES Restaurant,
	FOREIGN KEY (customer_id) REFERENCES Customer
);

INSERT INTO OrderTakesHas(order_id, total, tip, order_timestamp, restaurant_id, customer_id)
    VALUES(2001, 120.00, 40.00, '2022-01-08 12:35:29', 1, 11);
INSERT INTO OrderTakesHas(order_id, total, tip, order_timestamp, restaurant_id, customer_id)
    VALUES(2002, 67.00, 12.00, '2022-01-10 1:14:43', 2, 22);
INSERT INTO OrderTakesHas(order_id, total, tip, order_timestamp, restaurant_id, customer_id)
    VALUES(2003, 42.00, 5.00, '2022-02-12 14:33:15', 3, 33);
INSERT INTO OrderTakesHas(order_id, total, tip, order_timestamp, restaurant_id, customer_id)
    VALUES(2004, 120.00, 40.00, '2022-02-28 2:35:59', 4, 44);
INSERT INTO OrderTakesHas(order_id, total, tip, order_timestamp, restaurant_id, customer_id)
    VALUES(2005, 120.00, 40.00, '2022-03-01 10:06:09', 5, 55);


CREATE TABLE Requires(
	delivery_id integer NOT NULL,
	order_id integer NOT NULL,
	PRIMARY KEY (delivery_id),
	UNIQUE (order_id),
	FOREIGN KEY (delivery_id) REFERENCES DeliveryReceivesMakes,
	FOREIGN KEY (order_id) REFERENCES OrderTakesHas
);

INSERT INTO Requires(delivery_id, order_id)
    VALUES(1113, 2001);
INSERT INTO Requires(delivery_id, order_id)
    VALUES(1114, 2002);
INSERT INTO Requires(delivery_id, order_id)
    VALUES(1115, 2003);
INSERT INTO Requires(delivery_id, order_id)
    VALUES(1116, 2004);
INSERT INTO Requires(delivery_id, order_id)
    VALUES(1117, 2005);


CREATE TABLE PaymentMethod (
	payment_id integer,
	payment_type char(20),
	PRIMARY KEY (payment_id)
);

INSERT INTO PaymentMethod(payment_id, payment_type)
    VALUES (2352, "Credit Card");
INSERT INTO PaymentMethod(payment_id, payment_type)
    VALUES (2353, "Credit Card");
INSERT INTO PaymentMethod(payment_id, payment_type)
    VALUES (2354, "Gift Card");
INSERT INTO PaymentMethod(payment_id, payment_type)
    VALUES (2355, "Debit Card");
INSERT INTO PaymentMethod(payment_id, payment_type)
    VALUES (2356, "Credit Card");


CREATE TABLE Pays (
	order_id integer NOT NULL,
	payment_id integer NOT NULL,
	payment_processor char(20),
	PRIMARY KEY (order_id),
	UNIQUE (payment_id),
	FOREIGN KEY (payment_id) REFERENCES PaymentMethod,
	FOREIGN KEY (order_id) REFERENCES OrderTakesHas
);

INSERT INTO Pays(order_id, payment_id, payment_processor)
    VALUES (2001, 2352, "Visa");
INSERT INTO Pays(order_id, payment_id, payment_processor)
    VALUES (2002, 2353, "Visa");
INSERT INTO Pays(order_id, payment_id, payment_processor)
    VALUES (2003, 2354, "Paypal");
INSERT INTO Pays(order_id, payment_id, payment_processor)
    VALUES (2004, 2355, "Mastercard");
INSERT INTO Pays(order_id, payment_id, payment_processor)
    VALUES (2005, 2356, "Mastercard");


CREATE TABLE Promotion (
	promotion_id integer,
	promotion_type char(20),
	PRIMARY KEY(promotion_id)
);

INSERT INTO Promotion(promotion_id, promotion_type)
    VALUES (1101, "Percent Off");
INSERT INTO Promotion(promotion_id, promotion_type)
    VALUES (1102, "Percent Off");
INSERT INTO Promotion(promotion_id, promotion_type)
    VALUES (1103, "Free Delivery");
INSERT INTO Promotion(promotion_id, promotion_type)
    VALUES (1104, "Free Item");
INSERT INTO Promotion(promotion_id, promotion_type)
    VALUES (1105, "Free Delivery");


CREATE TABLE Discounts(
	promotion_id integer,
	payment_id integer,
	PRIMARY KEY(promotion_id),
	UNIQUE (payment_id),
	FOREIGN KEY (promotion_id) REFERENCES Promotion,
	FOREIGN KEY (payment_id) REFERENCES PaymentMethod
);

INSERT INTO Discounts(promotion_id, payment_id)
    VALUES (1101, 2352);
INSERT INTO Discounts(promotion_id, payment_id)
    VALUES (1102, 2353);
INSERT INTO Discounts(promotion_id, payment_id)
    VALUES (1103, 2354);
INSERT INTO Discounts(promotion_id, payment_id)
    VALUES (1104, 2355);
INSERT INTO Discounts(promotion_id, payment_id)
    VALUES (1105, 2356);