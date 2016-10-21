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
print 'ap_time_matrix:', len(ap_time_matrix), ap_time_matrix[-10:]

print max(max(row) for row in ap_time_matrix)

from sklearn.neighbors import NearestNeighbors
kn_model = NearestNeighbors(algorithm='auto').fit(ap_time_matrix)

neighbors = kn_model.kneighbors(ap_time_matrix, 5, return_distance=False)
wifi_ap_list = sorted(raw_data.keys())
time_list = sorted(raw_data[wifi_ap_list[0]].keys())

# 部分Ap邻居数据，可见确实距离很近。
def avg_rows(rows):
	avg_row = list(rows[0])  # 一定要加list，否则会被改动，Debug到凌晨3点。
	for row in rows[1:]:
		for i, val in enumerate(row):
			avg_row[i] += val
	return [round(val/len(rows), 1) for val in avg_row]

print 'Wifi neighbors'
for row in neighbors[-10:]:
	print [wifi_ap_list[x] for x in row]

print 'wifi neighbors score vectors'
for row in neighbors[-10:]:
	for x in row:
		pass
		print [round(x, 1) for x in ap_time_matrix[x]]
	print avg_rows([ap_time_matrix[x] for x in row])
	print ''

# 输出最终预测数据.
out_data = []
for neighbor_idx_row in neighbors:
	out_row = avg_rows([ap_time_matrix[x] for x in neighbor_idx_row])
	# print row_by_time
	out_data.append(out_row)

print 'out_data, m=%s, n=%s' % (len(out_data), len(out_data[0]))


fout = open('./airport_gz_passenger_predict.csv', 'w')
fout.write('passengerCount,WIFIAPTag,slice10min\n')
for i, wifi_row in enumerate(out_data):
	wifi_ap_tag = wifi_ap_list[i]
	for j, score in enumerate(wifi_row):
		time = time_list[j]
		fout.write('%s,%s,%s\n' % (round(score, 1), wifi_ap_tag, time))
fout.close()