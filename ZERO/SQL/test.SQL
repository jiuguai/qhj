-- 处理订单信息


DROP PROCEDURE
IF EXISTS proc_export_order;


CREATE PROCEDURE proc_export_order (in interval_hour int)

BEGIN

DROP TABLE
IF EXISTS temp_new_order;
--  生成一个可发送的新的数据
CREATE TABLE temp_new_order AS SELECT
  export_order.*
FROM
      export_order  join order_details on 
    export_order.订单号 = order_details.订单号
AND export_order.导出订单时间 = order_details.导出订单时间

union

select * from export_order where 订单号 not in (select 订单号 from order_details);

-- 可发送的老数据
DROP TABLE
IF EXISTS `temp_old_order`;

CREATE TABLE temp_old_order AS SELECT
  *
FROM
      export_order
    
WHERE
  订单号 NOT IN (
    SELECT
      订单号
    FROM
      temp_new_order
  ) and 导出订单时间 < DATE_SUB(now(),INTERVAL interval_hour HOUR);

END




# 插入新增加的订单
DROP PROCEDURE
IF EXISTS proc_insert_new_order;

CREATE PROCEDURE proc_insert_new_order ()
BEGIN
  INSERT order_details (
    商品ID,
    商品名,
    订单号,
    下单用户,
    下单时间,
    售价,
    实付金额,
    收件人电话,
    收件人地址,
    供应商ID,
    导出订单时间,
    供应商
  ) SELECT
    商品ID,
    商品名,
    订单号,
    下单用户,
    STR_TO_DATE(
      下单时间,
      '%Y年%m月%d日%H:%i:%s'
    ),
    售价,
    实收金额,
    收件人电话,
    收件人地址,
    供应商ID,
    导出订单时间,
    供应商
  FROM
    temp_new_order

  WHERE
    temp_new_order.订单号 not in (select 订单号 from order_details);
  END