BEGIN;

-- Create tables
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    slug TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email_token VARCHAR(20),
    verified INTEGER DEFAULT 0,
    token TEXT,
    token_expiration TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    photo TEXT,
    price DECIMAL(10, 2),
    category_id INTEGER,
    seller_id INTEGER,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories (id),
    FOREIGN KEY (seller_id) REFERENCES users (id)
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    buyer_id INTEGER NOT NULL,
    offer DECIMAL(10, 2) NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (product_id, buyer_id),
    FOREIGN KEY (buyer_id) REFERENCES users (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
);

CREATE TABLE IF NOT EXISTS confirmed_orders (
    order_id INTEGER PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders (id)
);

CREATE TABLE IF NOT EXISTS banned_products (
    id SERIAL PRIMARY KEY,
    reason TEXT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    product_id INTEGER,
    FOREIGN KEY (product_id) REFERENCES products (id)
);

CREATE TABLE IF NOT EXISTS blocked_user (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    blocked_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

COMMIT;

INSERT INTO "categories" VALUES (1,'Cocina','cocina');
INSERT INTO "categories" VALUES (2,'Deportes','deportes');
INSERT INTO "categories" VALUES (3,'Agricultura','agricultura');
INSERT INTO "categories" VALUES (4,'Muebles','muebles');
INSERT INTO "categories" VALUES (5,'Juguetes','juguetes');
INSERT INTO "users" VALUES (1,'Austin','mroscardev@gmail.com','pbkdf2:sha256:600000$B07HTrrJDXn0t9wE$d7927e4234bfc08b5531adfdab6e7d61de7b4fa749876f87cf4d1381f3a9eef0','admin','2023-11-24 14:41:16','2023-11-24 14:41:16','AEKwMffT9gRMjM-PxeiLX52_CgE',1,'17833f0efcac7ec454777224aedddc8e','2024-02-16 22:34:49.900499');
INSERT INTO "users" VALUES (2,'Rivi','rphysic1@home.pl','pbkdf2:sha256:600000$B07HTrrJDXn0t9wE$d7927e4234bfc08b5531adfdab6e7d61de7b4fa749876f87cf4d1381f3a9eef0','moderator','2023-11-24 14:41:16','2023-11-24 14:41:16',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (3,'Maurizio','mhathorn2@intel.com','pbkdf2:sha256:600000$B07HTrrJDXn0t9wE$d7927e4234bfc08b5531adfdab6e7d61de7b4fa749876f87cf4d1381f3a9eef0','wanner','2023-11-24 14:41:16','2023-11-24 14:41:16',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (4,'Brien','bambrozewicz3@mail.ru','wS8`@}1z''#f''u@','admin','2023-11-24 14:41:16','2023-11-24 14:41:16',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (5,'Kassandra','kbittany4@instagram.com','vW9/?7Q=`qi','moderator','2023-11-24 14:41:16','2023-11-24 14:41:16',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (6,'Melicent','mway5@prweb.com','rE2#i_Wl','wanner','2023-11-24 14:41:16','2023-11-24 14:41:16',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (7,'Doll','dtraill6@washingtonpost.com','aB6_?24h','admin','2023-11-24 14:41:16','2023-11-24 14:41:16',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (8,'Victoria','vrylance7@opensource.org','zP2+n/de<7hvM9','moderator','2023-11-24 14:41:16','2023-11-24 14:41:16',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (9,'Rheba','rarnaud8@people.com.cn','gZ3%<Vt_NF','wanner','2023-11-24 14:41:16','2023-11-24 14:41:16',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (10,'Corine','cwindrus9@biblegateway.com','pN7=Yhzfn3F4','admin','2023-11-24 14:41:16','2023-11-24 14:41:16',NULL,1,NULL,NULL);
INSERT INTO "users" VALUES (11,'test','amparedes2004@gmail.com','pbkdf2:sha256:600000$JqQNzSVdU4x1oCDS$37ae735f69a76bc298f2d03d9518583342d6c6d9490efef51ca3134023454b24','wanner','2023-11-24 15:26:27','2023-11-24 15:26:27','oPR5_s4eQbj5h5cGZtjp6oOcrWw',0,NULL,NULL);
INSERT INTO "users" VALUES (12,'oscar','oscargomezvng11@gmail.com','pbkdf2:sha256:600000$67TBWhOj1UkZK35a$de0df6ce0af36e953ba207ce1c1090e08743d623913d1118bebd1b5283f4236f','wanner','2023-11-24 16:38:44','2023-11-24 16:38:44','ArWOKfGSXJQNqHDYXooLLWjKC_I',0,NULL,NULL);
INSERT INTO "users" VALUES (14,'josejuan','alex1234750@gmail.com','pbkdf2:sha256:600000$dnzBFaOmOAkFLsSp$3a2b7019272d96e60e100efe244c5f25a50ca8dbd9560f720063c56d0ed3cd88','wanner','2023-11-24 16:48:12','2023-11-24 16:48:12','EoDsbfX7JaUlvvKx9mgmSTCLODY',0,NULL,NULL);
INSERT INTO "users" VALUES (16,'almapa','almapa@fp.insjoaquimmir.cat','pbkdf2:sha256:600000$CdVYjgy7aJofPwsG$21128907be12df1db5b087f3b98e147eaefbbde75f879d5d14981cda2bc31077','wanner','2023-11-24 17:48:13','2023-11-24 17:48:13','3gzbZCzwdMzC_3PZHSkPT_GWaLE',0,NULL,NULL);
INSERT INTO "users" VALUES (17,'ogomezd','ogomezd@fp.insjoaquimmir.cat','pbkdf2:sha256:600000$Mj1afIFwhrlH4UPM$640eeb7ad966b95adf2ba2857717e10680daad7f5d6d1aa5c585798f41d25742','wanner','2023-11-24 17:54:46','2023-11-24 17:54:46','QS75MizDN803VqGglCEWP77gZ7w',1,NULL,NULL);
INSERT INTO "users" VALUES (19,'adios','2daw.equip11@fp.insjoaquimmir.cat','pbkdf2:sha256:600000$IWdmVrBB8hXnL6uc$aba2bba5cf589d5d26060fb09c5270e92b36170357c13745492dc8b1974963d6','wanner','2023-11-24 18:43:35','2023-11-24 18:43:35','TFH9LpF05ZP9zlcrkDic4M6J9Qs',1,NULL,NULL);
INSERT INTO "products" VALUES (1,'Telefon rauw','lectus in quam fringilla rhoncus mauris enim leo rhoncus sed','a59ec155-ddbc-4c82-bba5-64b3f950576e-images.jpeg',600,2,2,'2023-11-24 14:41:16','2024-02-16 14:42:56');
INSERT INTO "products" VALUES (2,'Cookley','primis in faucibus orci luctus et ultrices','image-2',12,2,2,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (3,'Matsoft','eleifend donec ut dolor morbi vel lectus','image-3',38,1,5,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (4,'Telefon rauw','venenatis tristique fusce','a59ec155-ddbc-4c82-bba5-64b3f950576e-images.jpeg',600,1,5,'2023-11-24 14:41:16','2024-02-16 15:02:45');
INSERT INTO "products" VALUES (5,'Flowdesk','id luctus nec molestie sed justo pellentesque viverra pede','image-5',23,3,4,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (6,'Gembucket','adipiscing elit proin interdum mauris non ligula pellentesque ultrices','image-6',16,2,4,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (7,'Mat Lam Tam','donec vitae nisi nam ultrices','image-7',40,2,3,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (8,'Solarbreeze','ac nulla sed vel','image-8',50,5,1,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (9,'Job','dolor vel est','image-9',54,3,2,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (10,'Tampflex','vehicula consequat morbi a ipsum integer a nibh','image-10',80,2,3,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (11,'Asoka','non velit donec diam neque vestibulum eget vulputate ut','image-11',82,5,2,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (12,'Bamity','nulla integer pede','image-12',41,3,4,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (13,'Cookley','orci nullam molestie nibh in lectus','image-13',22,5,4,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (14,'Opela','lectus pellentesque eget nunc','image-14',9,5,2,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (15,'Toughjoyfax','vestibulum velit id pretium iaculis diam erat','image-15',20,2,5,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (16,'Sonsing','et commodo vulputate','image-16',20,3,2,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (17,'Quo Lux','venenatis tristique fusce congue diam id','image-17',73,4,1,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (18,'Vagram','tristique est et','image-18',7,2,1,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (19,'Namfix','vel accumsan tellus nisi eu orci','image-19',65,2,4,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "products" VALUES (20,'Bamity','ipsum primis in faucibus orci','image-20',80,1,1,'2023-11-24 14:41:16','2023-11-24 14:41:16');
INSERT INTO "banned_products" VALUES (26,'eee','2023-12-13 19:10:39',2);
INSERT INTO "banned_products" VALUES (27,'feo','2024-01-19 14:29:33',3);
INSERT INTO "banned_products" VALUES (28,'feo','2024-01-19 14:30:43',1);
INSERT INTO "blocked_user" VALUES (1,11,'por ser tonto','2023-12-13 19:01:44.599197');
INSERT INTO "blocked_user" VALUES (3,17,'tonto','2023-12-13 19:04:03.098226');
INSERT INTO "blocked_user" VALUES (4,10,'tonto','2024-01-26 14:23:02.998000');
INSERT INTO "orders" VALUES (1,1,2,100,'2024-02-16 14:55:20');
INSERT INTO "orders" VALUES (2,2,3,200.5,'2024-02-16 14:55:20');
INSERT INTO "orders" VALUES (3,3,1,150.75,'2024-02-16 14:55:20');
INSERT INTO "orders" VALUES (4,4,2,300,'2024-02-16 14:55:20');
COMMIT;