DROP TRIGGER
IF EXISTS test;

CREATE TRIGGER test BEFORE UPDATE ON order_details FOR EACH ROW
BEGIN

IF @disable_triggers IS NULL
AND old.运单号 IS NOT NULL
AND new.运单号 != old.运单号 THEN
	INSERT waybill_conflict (
		订单号,
		运单号_local,
		商品名_local,
		规格_local,
		单位_local,
		数量_local,
		收件人姓名_local,
		收件人地址_local,
		收件人电话_local,
		备注_local
	)
VALUES
	(
		old.订单号,
		old.运单号,
		old.商品名,
		old.规格,
		old.单位,
		old.数量,
		old.收件人姓名,
		old.收件人地址,
		old.收件人电话,
		old.备注
	);

UPDATE waybill_conflict t1,
 waybill_mail t2
SET t1.运单号 = t2.运单号,
 t1.商品名 = t2.商品名,
 t1.规格 = t2.规格,
 t1.单位 = t2.单位,
 t1.数量 = t2.数量,
 t1.收件人姓名 = t2.收件人姓名,
 t1.收件人地址 = t2.收件人地址,
 t1.收件人电话 = t2.收件人电话,
 t1.备注 = t2.备注
WHERE
	t1.订单号 = t2.订单号;


SET new.运单号 = old.运单号;


END
IF;


END