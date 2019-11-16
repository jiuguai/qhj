
CREATE DATABASE IF EXISTS QHJ DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

UPDATE order_details SET 运单号 = "1"

UPDATE order_details t1, waybill_mail t2 SET t1.运单号 = t2.运单号 
	WHERE t1.订单号 = t2.订单号

-- 此效率高于 未加JION的情况
UPDATE order_details JOIN waybill_mail on = t1.订单号 = t2.订单号 
		SET t1.运单号 = t2.运单号 

INSERT INTO order_details(订单号, 运单号) VALUES ("11", "2")
INSERT INTO order_details(订单号, 运单号) SELECT  (订单号, 运单号) FROM temp_new_order 
	WHERE NOT EXISTS (SELECT order_details.订单号 FROM order_details WHERE temp_new_order.订单号 = order_details.订单号)

--  涉及索引 效率选择
big_table in small_table
small_table EIXSTS big_table

[big_table,small_table] NOT EIXSTS [big_table,small_table]


