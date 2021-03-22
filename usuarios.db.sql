BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Usuarios" (
	"id"	INTEGER NOT NULL,
	"username"	VARCHAR(50) NOT NULL,
	"lastname"	VARCHAR(50) NOT NULL,
	"dni"	VARCHAR(9) NOT NULL,
	"address"	VARCHAR(50) NOT NULL,
	"movilphone"	VARCHAR(20) NOT NULL,
	"phone"	VARCHAR(20) NOT NULL,
	"email"	VARCHAR(80) NOT NULL,
	"password"	VARCHAR(50) NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Admin" (
	"id"	INTEGER NOT NULL,
	"admname"	VARCHAR(50) NOT NULL,
	"admlastname"	VARCHAR(50) NOT NULL,
	"admdni"	VARCHAR(9) NOT NULL,
	"admpassword"	VARCHAR(50) NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "Servicios" (
	"id"	INTEGER NOT NULL,
	"nombre"	VARCHAR(50) NOT NULL,
	"especialidad"	VARCHAR(50) NOT NULL,
	"policlinica"	VARCHAR(50) NOT NULL,
	"fecha"	VARCHAR(50) NOT NULL,
	"horario"	VARCHAR(50) NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "reservas" (
	"id"	INTEGER NOT NULL,
	"atencion"	INTEGER,
	"numturnos"	INTEGER NOT NULL,
	"user_id"	INTEGER,
	FOREIGN KEY("atencion") REFERENCES "Servicios"("id"),
	FOREIGN KEY("user_id") REFERENCES "Usuarios"("id"),
	PRIMARY KEY("id")
);
INSERT INTO "Usuarios" ("id","username","lastname","dni","address","movilphone","phone","email","password") VALUES (1,'Cebolla','Rodriguez','2222','los aromos','908098','098098','cebo@cuti.com','sha256$LmYeHhC1$ec089dbca4f8aa9f9590daaac873899560b1af7457683949b6431fcffbf6bf7d'),
 (2,'Chengue','Morales','1111','la blanqueada','876876','87687687','chenguito@bolso.com','sha256$LV529KDB$7c1c74bab0cbe0e7d80a359df78727728b12dc7d342721154c8d113ab0dd660c'),
 (3,'Matias','Alvez','44450601','Bulevar 1515','09950950','47230905','gonzalvez163@gmail.com','sha256$L0sbsAOx$1a1734019bde1f7efaddfd308ebcb8bd3b5234bbe1a364e9e803f5767ea1afd7');
INSERT INTO "Admin" ("id","admname","admlastname","admdni","admpassword") VALUES (1,'patroco','casales','1111','sha256$ANkmC8R7$79390e206985efb8fc3f29bfc6a39163593818f800afe5528aac03af1e082887'),
 (2,'Juan Jose','Perex Lopes','11111111','sha256$SAruwihQ$f74ce50bab0db696eba5ba1c8b60342dd6b0d6541d4aebe4c9c5959f0280c69d'),
 (3,'Pedro Daniel','Lopez Lopez','456456456','sha256$v9PlWIMf$88fce5408ebcdb8ccbe8c4e9cc58831bdf06220cb4072a56a201932b968ba569'),
 (4,'Maria Julia','Alvez Falcon','321654987','sha256$tHMqkThD$7d6763cf8a3f63fed9a0e1d4843510a7ed361c3709544e0c7264b298169f7386'),
 (5,'Maria Julia','Lopez Lopez','4546456','sha256$0vsrE46c$ab3641295c5bbab14fe1703d9373f06f769c110ca516a22c0a80a1bd32224057'),
 (6,'Juan Jose','Lopez Lopez','1324564654','sha256$VZMcuwKZ$809cf8cb5860b10d8506e3a33a35e077740dd408bae7b62ee3c3916a97568f59');
INSERT INTO "Servicios" ("id","nombre","especialidad","policlinica","fecha","horario") VALUES (1,'Dr Martinez','cardiologo','barrio "Lima"','0345-05-31','12:23'),
 (2,'Dr Gomez','Neurologo','barrio "montevideo"','0123-03-12','12:23'),
 (3,'Juan Romero','Medicina General','barrio p3','2020-04-16','07:00'),
 (4,'Juan Lima','Medicina General','Barrio 5','2020-04-18','10:00'),
 (5,'Maria Sosa','Medicina General','Barrio Centro','2020-04-25','13:00'),
 (6,'Ana Gomez','Ginecología','Barrio Centro','2020-04-24','16:00'),
 (7,'Marcos Lopez','Ginecología','barrio p3','2020-04-20','15:30'),
 (8,'Javier Mendez','Cardiologia','Barrio 5','2020-04-12','13:15'),
 (9,'Matias Alvez','Ginecologia','Barrio Centro','2020-04-30','13:50'),
 (10,'Juan Lima','Ginecología','barrio p3','2020-04-23','16:00'),
 (11,'Alfredo Soca','Cardiologia','Barrio 5','2020-04-10','10:30'),
 (12,'Ana Sosa','Urología','Barrio Centro','2020-04-22','11:45'),
 (13,'Javier Mendez','Ginecología','Base Norte','2020-04-22','14:30'),
 (14,'Mario Garcia','Medicina General','Barrio Centro','2020-04-26','17:30'),
 (15,'Maria Garcia','Ginecología','Barrio Centro','2020-04-15','15:00'),
 (16,'Matias Alvez','Medicina General','barrio p3','2020-04-16','08:00'),
 (17,'Emiliano Montaldo','Ginecología','Barrio Centro','2020-04-22','12:00'),
 (18,'Juan Sosa','Medicina General','Barrio Centro','2020-04-21','13:15'),
 (19,'Marcelo Vargas','Cardiologia','barrio p3','2020-04-24','09:30'),
 (20,'Mariana Santana','Urología','Base Norte','2020-04-23','10:15'),
 (21,'Juan Suarez','Medicina General','Barrio Centro','2020-04-25','12:00'),
 (22,'Juan Lima','Medicina General','Base Norte','2020-04-26','15:30'),
 (23,'Juan Lima','Ginecología','Base Norte','2020-04-25','12:00'),
 (24,'Juan Lima','Medicina General','Base Norte','2020-04-26','12:00');
COMMIT;
