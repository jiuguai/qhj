

drop table if exists waybill_mail;
create table waybill_mail(
	`订单号` char(20) PRIMARY KEY,
	`运单号` char(20),
	`商品名` varchar(60),
	`规格` varchar(60),
	`单位` varchar(5) ,
	`数量` int ,
	`收件人姓名` varchar(20),
	`收件人地址` varchar(60),
	`收件人电话` varchar(30),
	`备注` text
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

drop table if exists waybill_conflict;
create table waybill_conflict(
	`订单号` char(20) PRIMARY KEY,
	`运单号_local` char(20),
	`商品名_local` varchar(60),
	`规格_local` varchar(60),
	`单位_local` varchar(5) ,
	`数量_local` int ,
	`收件人姓名_local` varchar(20),
	`收件人地址_local` varchar(60),
	`收件人电话_local` varchar(30),
	`备注_local` text,
	`运单号` char(20),
	`商品名` varchar(60),
	`规格` varchar(60),
	`单位` varchar(5) ,
	`数量` int ,
	`收件人姓名` varchar(20),
	`收件人地址` varchar(60),
	`收件人电话` varchar(30),
	`备注` text


)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
