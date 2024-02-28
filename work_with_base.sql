CREATE database customers;
USE customers;
CREATE TABLE Customer (id integer PRIMARY KEY NOT NULL auto_increment,
customer_name varchar (20),
customer_surname varchar (30),
street varchar(30),
poste_code integer,
city varchar(20),
country varchar(20),
email varchar(30),
registration_date date);
INSERT INTO Customer (customer_name, customer_surname, street, poste_code, city, country, email, registration_date)
VALUES
("Bill", "Gates", "124 av", 23456, "Washington", "USA", "billy@gmail", "2023-01-01"),
("Elon", "Musk", "555 av", 23455, "London", "GB", "tesla@gmail", "2023-02-01"),
("Jeff", "Bezos", "88 av", 27892, "Toronto", "CN", "jeff@yahoo", "2023-03-01"),
("Steve", "Jobs", "123 av", 27877, "Rome", "IT", "st@yahoo", "2023-03-01");
SELECT * FROM Customer;
CREATE TABLE Orders 
(customer_id integer,
order_date date,
product_name varchar(30),
product_description text,
photo text,
price decimal(6,2));
INSERT INTO Orders (customer_id, order_date, product_name, product_description, photo, price)
VALUES
(1, "2024-02-28", "New York Yankees", "New Era 9Forty Adjustable Strapback Cap", "https://www.amazon.fr/New-Era-11157579-Casquette-Fabricant/dp/B00UCC59F2/ref=zg_bs_c_sports_d_sccl_1/262-1645526-9885068?pd_rd_w=PgHq4&content-id=amzn1.sym.44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_p=44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_r=SY4TH5XKEX4G28TFJRTF&pd_rd_wg=3tKkK&pd_rd_r=b9b5a971-c6f8-4a27-b180-6963ff983357&pd_rd_i=B00UCC59F2&psc=1", 
13.99);
SELECT * FROM orders;
INSERT INTO Orders (customer_id, order_date, product_name, product_description, photo, price)
VALUES
(1, "2024-01-28", "REDimpact", "Taille Standard - Format : Sac a Main Femme, Manteau Femme, Sacoche Homme, Veste, Sac a Dos", "https://www.amazon.fr/SAFE-DEFENSE-Spray-Anti-Agresión-REDimpact/dp/B07NLKZS8K/ref=zg_bs_c_sports_d_sccl_2/262-1645526-9885068?pd_rd_w=PgHq4&content-id=amzn1.sym.44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_p=44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_r=SY4TH5XKEX4G28TFJRTF&pd_rd_wg=3tKkK&pd_rd_r=b9b5a971-c6f8-4a27-b180-6963ff983357&pd_rd_i=B07NLKZS8K&psc=1", 
19.95),
(1, "2024-01-23", "INTEX Matelas", "Queen Raised 2-pers, Mixte Adulte, Noir/Bleu, 152 cm x 203 cm x 42 cm", "https://www.amazon.fr/Matelas-gonflable-électrique-Raised-2-pers/dp/B01IZVSAKC/ref=zg_bs_c_sports_d_sccl_4/262-1645526-9885068?pd_rd_w=PgHq4&content-id=amzn1.sym.44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_p=44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_r=SY4TH5XKEX4G28TFJRTF&pd_rd_wg=3tKkK&pd_rd_r=b9b5a971-c6f8-4a27-b180-6963ff983357&pd_rd_i=B01IZVSAKC&psc=1", 
56.49),
(1, "2024-01-18", "Imou Caméra", "ntérieure Caméra 360° Connectée Smartphone 1080P avec Détection Humaine AI Suivi Intelligent Sirène Audio Bidirectionnel Compatible Alexa pour Bébé/Animaux", "https://www.amazon.fr/Matelas-gonflable-électrique-Raised-2-pers/dp/B01IZVSAKC/ref=zg_bs_c_sports_d_sccl_4/262-1645526-9885068?pd_rd_w=PgHq4&content-id=amzn1.sym.44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_p=44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_r=SY4TH5XKEX4G28TFJRTF&pd_rd_wg=3tKkK&pd_", 
21.99),
(2, "2024-01-23", "Apple AirTag", "Apple AirTag", "https://www.amazon.fr/SAFE-DEFENSE-Spray-Ant-id=amzn1._rd_p=44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_r=SY4TH5XKEX4G28TFJRTF&pd_rd_wg=3tKkK&pd_rd_r=b9b5a971-c6f8-4a27-b180-6963ff983357&pd_rd_i=B07NLKZS8K&psc=1", 
29.99),
(2, "2024-01-24", "Vikaster Gourde", "500 ML Bouteille d'eau, sans BPA, Étanche & Réutilisable, avec Filtre et Marqueur de Temps, Convient pour en Plein Air", "https://www.amazon.fr/Matelas-gonflable-électrique-Raised-2-pers/dp/B01IZVSAKC/ref=zg_bs_c_sports_d_sccl_4/262-1645526-9885068?pd_rd_w=PgHq4&content-id=amzn1.sym.44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_p=44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_r=SY4TH5XKEX4G28TFJRTF&pd_rd_wg=3tKkK&pd_rd_r=b9b5a971-c6f8-4a27-b180-6963ff983357&pd_rd_i=B01IZVSAKC&psc=1", 
12.95),
(2, "2024-01-17", "Blukar Lampe", "Super Lumineux Léger Torche Frontale LED Puissante avec Voyant Rouge,8 Modes d'Éclairage,Capteur Mouvement,IPX5 Étanche,30H d'autonomie pour Camping/Pêche/Urgence ", "https://www.amazon.fr/Matelas-gonflable-électrique-Raised-2-pers/dp/B01IZVSAKC/ref=zg_bs_c_sports_d_sccl_4/262-1645526-9885068?pd_rd_w=PgHq4&content-id=amzn1.sym.44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_p=44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_r=SY4TH5XKEX4G28TFJRTF&pd_rd_wg=3tKkK&pd_", 
15.99),
(3, "2024-01-15", "Amazon Fire", "Lite avec télécommande vocale Alexa | Lite (sans boutons de contrôle de la TV) | Streaming HD", "https://www.amazon.fr/Matelas-gonflable-électrique-Raised-2-pers/dp/B01IZVSAKC/ref=zg_bs_c_sports_d_sccl_4/262-1645526-9885068?pd_rd_w=PgHq4&content-id=amzn1.sym.44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_p=44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_r=SY4TH5XKEX4G28TFJRTF&pd_rd_wg=3tKkK&pd_", 
34.99),
(3, "2024-01-14", "Babolat", "Tube de 4 Balles de Tennis", "https://www.amazon.fr/Matelas-gonflable-électrique-Raised-2-pers/dp/B01IZVSAKC/ref=zg_bs_c_sports_d_sccl_4/262-1645526-9885068?pd_rd_w=PgHq4&content-id=amzn1.sym.44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_p=44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_r=SY4TH5XKEX4G28TFJRTF&pd_rd_wg=3tKkK&pd_", 
6.99),
(4, "2024-01-13", "KTEBO", "OTG - Anti-Buée Masque de Ski Protection UV400 Lunettes de Snowboard, Compatible avec Casque pour Lunette Ski Snowboard Autres Sports Hiver", "https://www.amazon.fr/Matelas-gonflable-électrique-Raised-2-pers/dp/B01IZVSAKC/ref=zg_bs_c_sports_d_sccl_4/262-1645526-9885068?pd_rd_w=PgHq4&content-id=amzn1.sym.44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_p=44b1633f-7064-4b68-a62f-1fab9d1e6ad8&pf_rd_r=SY4TH5XKEX4G28TFJRTF&pd_rd_wg=3tKkK&pd_", 
10.99);
ALTER TABLE customer
ADD last_modify date DEFAULT (CURDATE());
SELECT * FROM customer;
ALTER TABLE orders
ADD discounter_price decimal(6,2) DEFAULT (price*0.9);
SELECT * FROM orders


