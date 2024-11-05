
每个月第一天的2：00，创建新的History记录
id:日期+月份+cargo_id，如202411C0001
year: 当年年份
month：当月月份
cargo_name, model: SELECT cargo_name, model FROM inventory WHERE cargo_id = %s
starting_price: 当前单价
starting_count: 当前数量
starting_total_price:当前总价(starting_price * starting_count)

每个月最后一天的23:00
closing_count: 当前数量
closing_price:当前单价
closing_total_price: 当前总价
