-- 处理订单信息
DROP PROCEDURE
IF EXISTS proc_export_order;

CREATE PROCEDURE proc_export_order (IN interval_hour INT)
BEGIN
  DROP TABLE
IF EXISTS temp_new_order;

--  生成一个可发送的新的数据
CREATE TABLE temp_new_order AS SELECT
  export_order.*
FROM
  export_order
JOIN order_details ON export_order.订单号 = order_details.订单号
AND export_order.导出订单时间 = order_details.导出订单时间
UNION
  SELECT
    *
  FROM
    export_order
  WHERE
    NOT EXISTS (
      SELECT
        订单号
      FROM
        order_details
      WHERE
        order_details.订单号 = export_order.订单号
    );

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
  )
AND 导出订单时间 < DATE_SUB(
  now(),
  INTERVAL interval_hour HOUR
);


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
  用户名,
  用户等级,
  下单时间,
  售价,
  规格,
  单位,
  数量,
  实付金额,
  收件人姓名,
  收件人电话,
  收件人地址,
  发货商,
  发货商ID,
  供应商ID,
  供应商,
  导出订单时间,
  备注
) SELECT
  商品ID,
  商品名,
  订单号,
  用户名,
  用户等级,
  下单时间,
  售价,
  规格,
  单位,
  数量,
  实付金额,
  收件人姓名,
  收件人电话,
  收件人地址,
  发货商,
  发货商ID,
  供应商ID,
  供应商,
  导出订单时间,
  备注
FROM
  temp_new_order
WHERE
  NOT EXISTS (
    SELECT
      订单号
    FROM
      order_details
    WHERE
      order_details.订单号 = temp_new_order.订单号
  );

  END


drop procedure if exists proc_update_address;

CREATE PROCEDURE proc_update_address ()
BEGIN
  UPDATE order_details t1
JOIN update_address t2 ON t1.订单号 = t2.订单号
SET t1.国家 = t2.国家,
 t1.城市 = t2.城市,
 t1.县区 = t2.县区,
 t1.街道 = t2.街道,
 t1.lng = t2.lng,
 t1.lat = t2.lat;
END;
