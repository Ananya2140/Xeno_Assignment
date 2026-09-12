select count(*) as target_base
from communication_log cl
join campaign c 
on cl.communication_id = c.id
where cl.merchant_id = 501
  and cl.communication_type = '2'
  and cl.delivery_status = 900
  and cl.sent_time >= '2026-10-01 00:00:00'
  and cl.sent_time < '2026-11-01 00:00:00';