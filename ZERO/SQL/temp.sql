


INSERT INTO test(订单号, 运单号, 商品ID, 商品名, 下单用户, 下单时间, 售价, 收件人电话, 收件人地址,供应商ID)
SELECT 订单号,
       NULL 运单号,
            商品ID,
            商品名,
            下单用户,
            STR_TO_DATE(下单时间,'%Y年%m月%d日%H:%i:%s') ,
            售价,
            收件人电话,
            收件人地址,
            供应商ID
FROM order_temp a
WHERE a.订单号 NOT IN
    (SELECT 订单号
     FROM test);




