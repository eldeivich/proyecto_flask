DROP TABLE IF EXISTS cryptos;

CREATE TABLE "cryptos" (
	"id"	INTEGER,
	"Symbol"	TEXT,
	"name"	TEXT,
	PRIMARY KEY("id")
);

DROP TABLE IF EXISTS movements;

CREATE TABLE "movements" (
	"id"	INTEGER,
	"date"	TEXT,
	"time"	TEXT,
	"from_currency"	INTEGER,
	"from_quantity"	REAL,
	"to_currency"	INTEGER,
	"to_quantity"	REAL,
	PRIMARY KEY("id"),
	FOREIGN KEY("to_currency") REFERENCES "cryptos",
	FOREIGN KEY("from_currency") REFERENCES "cryptos"
);