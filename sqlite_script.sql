# 各个表headers的样子.
zhe-mactekiMacBook-Air:raw_data zhe-mac$ head -1 gate.csv
BGATE_ID,BGATE_AREA
zhe-mactekiMacBook-Air:raw_data zhe-mac$ head -1 depart.csv 
passenger_ID2,flight_ID,flight_time,checkin_time
zhe-mactekiMacBook-Air:raw_data zhe-mac$ head -1 security.csv 
passenger_ID,security_time,flight_ID
zhe-mactekiMacBook-Air:raw_data zhe-mac$ head -1 flight.csv 
flight_ID,scheduled_flt_time,actual_flt_time,BGATE_ID
zhe-mactekiMacBook-Air:raw_data zhe-mac$ head -1 wifi.csv 
WIFIAPTag,passengerCount,timeStamp

# 创建databases,注意要用无头的csv.
create table gate(bgate_id text, bgate_area text);
.import gate.csv gate

create table depart(passenger_id_2 text, flight_id text, flight_time text, checkin_time text);
.import depart.csv depart

create table security(passenger_id text, security_time text, flight_id text);
.import security.csv security

create table flight(flight_id text, scheduled_flight_time text, actual_flight_time text, bgate_id text);
.import flight.csv flight

create table wifi(wifi_ap_tag text, passenger_count real, time text);
.import wifi.csv wifi

# 统计各个area中ap的流量分布.
select t1.bgate_area, t1.wifi_ap_tag, passenger_count, passenger_count/passenger_area_sum
from (
	select substr(wifi_ap_tag, 1, 2) as bgate_area, wifi_ap_tag, passenger_count 
	from (select upper(wifi_ap_tag) as wifi_ap_tag, sum(passenger_count) as passenger_count from wifi group by 1)
) as t1 join (
	select substr(upper(wifi_ap_tag), 1, 2) as bgate_area, sum(passenger_count) as passenger_area_sum from wifi group by 1
) as t2 using(bgate_area)
where t1.bgate_area == 'E1';

# 生成Baseline.
select round(sum(passenger_count)/3,1) as passengerCount, upper(wifi_ap_tag) as WIFIAPTag,
	'2016-09-14-' || substr(time, 12, 4) as slice10min   
from wifi
where substr(time, 6, 5) in ('09-11', '09-12', '09-13') and
      substr(time, 12, 5) >= '15-00' and substr(time, 12, 5) < '18-00'
group by 2,3
limit 10;