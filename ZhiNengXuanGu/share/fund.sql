create table stock_fund_history(
 id  serial not null,
 name varchar(20),
 symbol varchar(20),
 ctime VARCHAR(20),
 organ  VARCHAR(20),
 organNum int,
 stackNum "numeric"(12,2),
 stackMoney "numeric"(12,2),
 rateTotalStack "numeric"(5,2),
 rateCirculateStack "numeric"(5,2)

)