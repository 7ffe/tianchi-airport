# coding: utf8
# 样例表头：'user_id,item_id,behavior_type,user_geohash,item_category,time\r\n'
# behavior_type: 1,2,3,4
import datetime
fin = open('./data_round2/kn_raw.csv', 'r')
# lines = fin.readlines(1024*1024*100)
lines = fin.readlines()
print 'lines: ', len(lines)
print 'line 0:', lines[0].strip()
print 'line 1:', lines[1].strip()

raw_data = {}
for line in lines[1:]:
	parts = line.strip().split(',')
	wifi_ap_tag = parts[0]
	time = parts[1]
	score = float(parts[2])
	ap_dict = raw_data.get(wifi_ap_tag, {})
	ap_dict[time] = score
	raw_data[wifi_ap_tag] = ap_dict

ap_time_matrix = []
for wifi_ap_tag in sorted(raw_data.keys()):
	row = []
	for each_time in sorted(raw_data[wifi_ap_tag].keys()):
		row.append(raw_data[wifi_ap_tag][each_time])
	ap_time_matrix.append(row)
print 'ap_time_matrix:', len(ap_time_matrix), ap_time_matrix[:3]

from sklearn.neighbors import NearestNeighbors
kn_model = NearestNeighbors(algorithm='auto').fit(ap_time_matrix)

neighbors = kn_model.kneighbors(ap_time_matrix, 5, return_distance=False)
wifi_ap_list = sorted(raw_data.keys())
time_list = sorted(raw_data[wifi_ap_list[0]].keys())

# 部分Ap邻居数据，可见确实距离很近。
print neighbors[500:510]

def avg_rows(rows):
	avg_row = rows[0]
	for row in rows[1:]:
		for i, val in enumerate(row):
			avg_row[i] += val
	return [round(val/len(rows), 1) for val in avg_row]

for row in neighbors[500:510]:
	for x in row:
		print [round(x, 1) for x in ap_time_matrix[x]]
	print avg_rows([ap_time_matrix[x] for x in row])
	print ''

for row in neighbors[500:510]:
	print [wifi_ap_list[x] for x in row]


print wifi_ap_list
print time_list
# 输出最终预测数据.
out_data = []
for neighbor_idx_row in neighbors:
	row_by_time = avg_rows([ap_time_matrix[x] for x in neighbor_idx_row])
	out_data.append(row_by_time)

print 'out_data, m=%s, n=%s' % (len(out_data), len(out_data[0]))


fout = open('./airport_gz_passenger_predict.csv', 'w')
fout.write('passengerCount,WIFIAPTag,slice10min\n')
for i, wifi_row in enumerate(out_data):
	wifi_ap_tag = wifi_ap_list[i]
	for j, score in enumerate(wifi_row):
		time = time_list[j]
		score = wifi_row[j]
		fout.write('%s,%s,%s\n' % (round(score, 1), wifi_ap_tag, time))
fout.close()

'''


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
'''
