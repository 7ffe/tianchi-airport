# coding: utf8
# 样例表头：'user_id,item_id,behavior_type,user_geohash,item_category,time\r\n'
# behavior_type: 1,2,3,4
import datetime
fin = open('./train_user.csv', 'r')
# lines = fin.readlines(1024*1024*100)
lines = fin.readlines()
print 'lines: ', len(lines)
print 'line 0:', lines[0].strip()
print 'line 1:', lines[1].strip()

# 处理表头.
field_to_idx = {}
idx_to_field = {}
for idx, field in enumerate(lines[0].strip().split(',')):
    field_to_idx[field] = idx
    idx_to_field[idx] = field

print field_to_idx
print idx_to_field

# 按一定结构组织数据.
data_1 = {}
today_date = datetime.datetime.utcnow().date()
for line in lines[1:]:
    entry = line.strip().split(',')
    user_id = entry[field_to_idx['user_id']]
    item_id = entry[field_to_idx['item_id']]
    behavior_type = int(entry[field_to_idx['behavior_type']])
    user_geohash = entry[field_to_idx['user_geohash']]
    item_category = entry[field_to_idx['item_category']]
    time = entry[field_to_idx['time']]
    time_dt = datetime.datetime.strptime(time, '%Y-%m-%d %H')
    time_date = time_dt.date()
    time_norm_day = int((time_date - today_date).days) + 365*10
    if time_norm_day in data_1:
    	data_1[time_norm_day].add((user_id, item_id, behavior_type))
    else:
    	data_1[time_norm_day] = set([(user_id, item_id, behavior_type)])

# 进一步处理，目的是统计某个概率.
data_2 = {}
for event_day in sorted(data_1.keys()):
	for triple in data_1[event_day]:
		if triple[2] == 1: # View event.
			user_id, item_id, behavior_type = triple
			for day_span in range(0, 15):
				if day_span not in data_2:
					data_2[day_span] = {'views':0, 'buys': 0} 
				data_2[day_span]['views'] += 1
				target_day = event_day + day_span
				if target_day in data_1 and (user_id, item_id, 4) in data_1[target_day]:
					data_2[day_span]['buys'] += 1
# import pdb; pdb.set_trace()

stats = {}
stats['day_span_buys_in_views'] = {}
for day_span in range(0, 15):
	buys = data_2.get(day_span, {}).get('buys', 0)
	views = data_2.get(day_span, {}).get('views', 1)
	print day_span, buys, views, '%.4f' % (1.0*buys/views)
	stats['day_span_buys_in_views'][day_span] = 1.0*buys/views
	
print sorted(data_1.keys())
print stats
final_day = max(data_1.keys()) + 1
max_day = max(data_1.keys())

ret_data = set()
for triple in data_1[event_day]:
	user_id, item_id, behavior_type = triple
	if behavior_type != 4:
		ret_data.add((user_id, item_id))

fout = open('./tianchi_mobile_recommendation_predict.csv', 'w')
fout.write('user_id,item_id\n')
for user_id, item_id in sorted(list(ret_data)):
	fout.write('%s,%s\n' % (user_id, item_id))
fout.close()

