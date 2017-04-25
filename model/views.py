#coding:utf-8

from django.shortcuts import render, HttpResponse

import redis
import json
import pymssql
import re
# Create your views here.
def connent():
    conn = pymssql.connect(host="172.16.5.16", user='sa', password='sa', database='ProductCommant', charset='utf8')
    cursor = conn.cursor()
    sql = '''select * from ZFXXMODELCAL'''
    cursor.execute(sql)
    result = cursor.fetchall()
    result.sort(key=lambda x: (x[2], x[0]))

    return result

def zfmc(request):
	return render(request, 'zfmc.html')

def zfmcshow1(request):
	result = connent()

	DATA = {}
	title = '秘书判断（负面召回率）优化对比'
	DATA = {
		'text': title,
		'legend': ['政府_秘书判断','政府_改进秘书判断','医疗_秘书判断','医疗_改进秘书判断',],
	};

	time_list = []
	list_fz_yiliao = list()
	list_fz = list()
	n_list_fz_yiliao = list()
	n_list_fz = list()
	for each in result:
		# if each[0] == 'fc823138-cf5c-4d1d-ba99-4c2b06b78b36':
		# 	continue
		# if each[0] == '30c057e3-3d70-4b8c-bbcc-384d764c8914':
		# 	continue
		time = each[4]
		time = re.search("(\d{2}\.\d{2})$", time)
		if time:
			time = time.group(1)
			time = time.replace(".", u"月") + u"日"
		else:
			continue
		time_list.append(time)

		data = each[-1]
		data_type = each[6]

		if u'医疗' in data_type:
			fz_yiliao = re.search(u'秘书判断负面召回率：(0.\d+)', data)
			if fz_yiliao:
				fz_yiliao = fz_yiliao.group(1)
			zzq_yiliao = re.search(u"秘书判断整体准确率：(0.\d+)", data)
			if zzq_yiliao:
				zzq_yiliao = zzq_yiliao.group(1)
			zz_yiliao = re.search(u"秘书判断整体召回率：(0.\d+)", data)
			if zz_yiliao:
				zz_yiliao = zz_yiliao.group(1)
			f1_yiliao = re.search(u"F1:(0.\d+) 改进秘书判断", data)
			if f1_yiliao:
				f1_yiliao = f1_yiliao.group(1)

			n_fz_yiliao = re.search(u"改进判断负面召回率：(0.\d+)", data)
			if n_fz_yiliao:
				n_fz_yiliao = n_fz_yiliao.group(1)
			n_zzq_yiliao = re.search(u"改进判断整体准确率：(0.\d+)", data)
			if n_zzq_yiliao:
				n_zzq_yiliao = n_zzq_yiliao.group(1)
			n_zz_yiliao = re.search(u"改进判断整体召回率：(0.\d+)", data)
			if n_zz_yiliao:
				n_zz_yiliao = n_zz_yiliao.group(1)
			n_f1_yiliao = re.search(u"F1:(0.\d+) 准确率", data)
			if n_f1_yiliao:
				n_f1_yiliao = n_f1_yiliao.group(1)

			# 医疗——负面召回率
			tmp_fz_yiliao = [time, fz_yiliao]
			list_fz_yiliao.append(tmp_fz_yiliao)
			# 改进医疗——负面召回率
			n_tmp_fz_yiliao = [time, n_fz_yiliao]
			n_list_fz_yiliao.append(n_tmp_fz_yiliao)

		if u'汇总' in data_type:
			fz = re.search(u"秘书判断负面召回率：(0.\d+)", data)
			if fz:
				fz = fz.group(1)
			zzq = re.search(u"秘书判断整体准确率：(0.\d+)", data)
			if zzq:
				zzq = zzq.group(1)
			zz = re.search(u"秘书判断整体召回率：(0.\d+)", data)
			if zz:
				zz = zz.group(1)
			f1 = re.search(u"F1:(0.\d+) 改进秘书判断", data)
			if f1:
				f1 = f1.group(1)

			n_fz = re.search(u"改进判断负面召回率：(0.\d+)", data)
			if n_fz:
				n_fz = n_fz.group(1)
			n_zzq = re.search(u"改进判断整体准确率：(0.\d+)", data)
			if n_zzq:
				n_zzq = n_zzq.group(1)
			n_zz = re.search(u"改进判断整体召回率：(0.\d+)", data)
			if n_zz:
				n_zz = n_zz.group(1)
			n_f1 = re.search(u"F1:(0.\d+) 准确率", data)
			if n_f1:
				n_f1 = n_f1.group(1)

			# 汇总——负面召回率
			tmp_fz = [time, fz]
			list_fz.append(tmp_fz)
			# 改进汇总——负面召回率
			n_tmp_fz = [time, n_fz]
			n_list_fz.append(n_tmp_fz)

	# 负面召回率
	content = list()
	for i in range(len(list_fz_yiliao)):
		for j in range(len(list_fz)):
			if list_fz_yiliao[i][0] == list_fz[j][0]:
				content_1 = [list_fz[j][0], list_fz[j][1], list_fz_yiliao[i][1]]
				content_1 = [n for n in content_1]
				content.append(content_1)
	content.sort(key=lambda x: (x[0], x[0]))
	# print content

	# 改进负面召回率
	n_content = list()
	for i in range(len(n_list_fz_yiliao)):
		for j in range(len(n_list_fz)):
			if n_list_fz_yiliao[i][0] == n_list_fz[j][0]:
				n_content_1 = [n_list_fz[j][0], n_list_fz[j][1], n_list_fz_yiliao[i][1]]
				n_content_1 = [n for n in n_content_1]
				n_content.append(n_content_1)
	n_content.sort(key=lambda x: (x[0], x[0]))
	# print n_content

	time_list = list()
	old_f_recall_list_all = list()
	new_f_recall_list_all = list()
	old_f_recall_list_yiliao = list()
	new_f_recall_list_yiliao = list()

	for a in content:
		time_list.append(a[0])
		old_f_recall_list_all.append(a[1])
		old_f_recall_list_yiliao.append(a[2])
	for b in n_content:
		new_f_recall_list_all.append(b[1])
		new_f_recall_list_yiliao.append(b[2])

	time_list.insert(0, '标准（无预警）')
	old_f_recall_list_all.insert(0, 0.7096154)
	new_f_recall_list_all.insert(0, 0.8788462)
	old_f_recall_list_yiliao.insert(0, 0.325301)
	new_f_recall_list_yiliao.insert(0,0.493976)


	DATA['time'] = time_list
	# 汇总
	DATA['old_f_recall_list_all'] = old_f_recall_list_all
	DATA['new_f_recall_list_all'] = new_f_recall_list_all
    # 医疗
	DATA['old_f_recall_list_yiliao'] = old_f_recall_list_yiliao
	DATA['new_f_recall_list_yiliao'] = new_f_recall_list_yiliao


	return render(request, 'zfmcshow.html', {'DATA': json.dumps(DATA)})

def zfmcshow2(request):
	result = connent()

	DATA = {}
	title = '秘书判断优化对比（医疗结果）'
	DATA = {
		'text': title,
		'legend': ['原_整体准确率','原_整体召回率','原_F1','改进_整体准确率','改进_整体召回率','改进_F1',],
	};

	time_list = []
	list_zzq_yiliao = list()
	n_list_zzq_yiliao = list()
	list_zz_yiliao = list()
	n_list_zz_yiliao = list()
	list_f1_yiliao = list()
	n_list_f1_yiliao = list()
	for each in result:
		time = each[4]
		time = re.search("(\d{2}\.\d{2})$", time)
		if time:
			time = time.group(1)
			time = time.replace(".", u"月") + u"日"
		else:
			continue
		time_list.append(time)

		data = each[-1]
		data_type = each[6]

		if u'医疗' in data_type:
			fz_yiliao = re.search(u'秘书判断负面召回率：(0.\d+)', data)
			if fz_yiliao:
				fz_yiliao = fz_yiliao.group(1)
			zzq_yiliao = re.search(u"秘书判断整体准确率：(0.\d+)", data)
			if zzq_yiliao:
				zzq_yiliao = zzq_yiliao.group(1)
			zz_yiliao = re.search(u"秘书判断整体召回率：(0.\d+)", data)
			if zz_yiliao:
				zz_yiliao = zz_yiliao.group(1)
			f1_yiliao = re.search(u"F1:(.*?)[\n*]\u6539\u8fdb\u79d8\u4e66", data)
			if not f1_yiliao:
				f1_yiliao = re.search(u"F1:(.*?)\n\n\u6539\u8fdb\u79d8\u4e66", data)
			if not f1_yiliao:
				f1_yiliao = re.search(u"F1:(.*?)\n\u6539\u8fdb\u79d8\u4e66", data)
			if f1_yiliao:
				f1_yiliao = f1_yiliao.group(1)

			n_fz_yiliao = re.search(u"改进判断负面召回率：(0.\d+)", data)
			if n_fz_yiliao:
				n_fz_yiliao = n_fz_yiliao.group(1)
			n_zzq_yiliao = re.search(u"改进判断整体准确率：(0.\d+)", data)
			if n_zzq_yiliao:
				n_zzq_yiliao = n_zzq_yiliao.group(1)
			n_zz_yiliao = re.search(u"改进判断整体召回率：(0.\d+)", data)
			if n_zz_yiliao:
				n_zz_yiliao = n_zz_yiliao.group(1)
			n_f1_yiliao = re.search(u'''F1:(.*?)\n\n\u51c6\u786e''', data)
			if not n_f1_yiliao:
				n_f1_yiliao = re.search(u'''F1:(.*?)\n\u51c6\u786e''', data)
			if not n_f1_yiliao:
				n_f1_yiliao = re.search(u'''F1:(.*?)[\n*]\u51c6\u786e''', data)
			if n_f1_yiliao:
				n_f1_yiliao = n_f1_yiliao.group(1)

			# 医疗——整体准确率
			tmp_zzq_yiliao = [time, zzq_yiliao]
			list_zzq_yiliao.append(tmp_zzq_yiliao)
			# 改进医疗——整体准确率
			n_tmp_zzq_yiliao = [time, n_zzq_yiliao]
			n_list_zzq_yiliao.append(n_tmp_zzq_yiliao)
			# 医疗——整体召回率
			tmp_zz_yiliao = [time, zz_yiliao]
			list_zz_yiliao.append(tmp_zz_yiliao)
			# 改进医疗——整体召回率
			n_tmp_zz_yiliao = [time, n_zz_yiliao]
			n_list_zz_yiliao.append(n_tmp_zz_yiliao)
			# 医疗——F1
			tmp_f1_yiliao = [time, f1_yiliao]
			list_f1_yiliao.append(tmp_f1_yiliao)
			# 改进医疗——F1
			n_tmp_f1_yiliao = [time, n_f1_yiliao]
			n_list_f1_yiliao.append(n_tmp_f1_yiliao)

	# 整体准确率
	content = list()
	for i in range(len(list_zzq_yiliao)):
		for j in range(len(n_list_zzq_yiliao)):
			if list_zzq_yiliao[i][0] == n_list_zzq_yiliao[j][0]:
				content_1 = [list_zzq_yiliao[j][0], list_zzq_yiliao[j][1], n_list_zzq_yiliao[i][1]]
				content_1 = [n for n in content_1]
				content.append(content_1)
	content.sort(key=lambda x: (x[0], x[0]))
	# print content

	time_list = list()
	zzq_list = list()
	n_zzq_list = list()
	for a in content:
		time_list.append(a[0])
		zzq_list.append(a[1])
		n_zzq_list.append(a[2])

	# 整体召回率
	content2 = list()
	for i in range(len(list_zz_yiliao)):
		for j in range(len(n_list_zz_yiliao)):
			if list_zz_yiliao[i][0] == n_list_zz_yiliao[j][0]:
				content_1 = [list_zz_yiliao[j][0], list_zz_yiliao[j][1], n_list_zz_yiliao[i][1]]
				content_1 = [n for n in content_1]
				content2.append(content_1)
	content2.sort(key=lambda x: (x[0], x[0]))
	# print content2

	zz_list = list()
	n_zz_list = list()
	for b in content2:
		zz_list.append(b[1])
		n_zz_list.append(b[2])

	# f1
	content3 = list()
	for i in range(len(list_f1_yiliao)):
		for j in range(len(n_list_f1_yiliao)):
			if list_f1_yiliao[i][0] == n_list_f1_yiliao[j][0]:
				content_1 = [list_f1_yiliao[j][0], list_f1_yiliao[j][1], n_list_f1_yiliao[i][1]]
				content_1 = [n for n in content_1]
				content3.append(content_1)
	content3.sort(key=lambda x: (x[0], x[0]))
	# print content3

	f1_list = list()
	n_f1_list = list()
	for c in content3:
		f1_list.append(c[1])
		n_f1_list.append(c[2])

	time_list.insert(0, '标准（无预警）')
	zzq_list.insert(0, 0.8)
	n_zzq_list.insert(0, 0.75431)
	zz_list.insert(0, 0.382023)
	n_zz_list.insert(0,0.50578)
	f1_list.insert(0, 0.51711)
	n_f1_list.insert(0,0.605536)


	DATA['time'] = time_list

	DATA['zzq_list'] = zzq_list
	DATA['n_zzq_list'] = n_zzq_list
	#
	DATA['zz_list'] = zz_list
	DATA['n_zz_list'] = n_zz_list
    #
	DATA['f1_list'] = f1_list
	DATA['n_f1_list'] = n_f1_list

	return render(request, 'zfmcshow2.html', {'DATA': json.dumps(DATA)})

def zfmcshow3(request):
	result = connent()

	DATA = {}
	title = '秘书判断优化对比（政府结果）'
	DATA = {
		'text': title,
		'legend': ['原_整体准确率', '原_整体召回率', '原_F1', '改进_整体准确率', '改进_整体召回率', '改进_F1', ],
	};

	time_list = []
	list_zzq = list()
	n_list_zzq = list()
	list_zz = list()
	n_list_zz = list()
	list_f1 = list()
	n_list_f1 = list()
	for each in result:
		time = each[4]
		time = re.search("(\d{2}\.\d{2})$", time)
		if time:
			time = time.group(1)
			time = time.replace(".", u"月") + u"日"
		else:
			continue
		time_list.append(time)

		data = each[-1]
		data_type = each[6]

		if u'汇总' in data_type:
			fz = re.search(u"秘书判断负面召回率：(0.\d+)", data)
			if fz:
				fz = fz.group(1)
			zzq = re.search(u"秘书判断整体准确率：(0.\d+)", data)
			if zzq:
				zzq = zzq.group(1)
			zz = re.search(u"秘书判断整体召回率：(0.\d+)", data)
			if zz:
				zz = zz.group(1)
			f1 = re.search(u"F1:(.*?)[\n*]\u6539\u8fdb\u79d8\u4e66", data)
			if not f1:
				f1 = re.search(u"F1:(.*?)\n\n\u6539\u8fdb\u79d8\u4e66", data)
			if not f1:
				f1 = re.search(u"F1:(.*?)\n\u6539\u6539\u8fdb\u79d8\u4e66", data)
			if f1:
				f1 = f1.group(1)

			n_fz = re.search(u"改进判断负面召回率：(0.\d+)", data)
			if n_fz:
				n_fz = n_fz.group(1)
			n_zzq = re.search(u"改进判断整体准确率：(0.\d+)", data)
			if n_zzq:
				n_zzq = n_zzq.group(1)
			n_zz = re.search(u"改进判断整体召回率：(0.\d+)", data)
			if n_zz:
				n_zz = n_zz.group(1)
			n_f1 = re.search(u"F1:(.*?)[\n*]\u51c6\u786e", data)
			if not n_f1:
				n_f1 = re.search(u'''F1:(.*?)\n\u51c6\u786e''', data)
			if not n_f1:
				n_f1 = re.search(u'''F1:(.*?)\n\n\u51c6\u786e''', data)
			if n_f1:
				n_f1 = n_f1.group(1)

			# 医疗——整体准确率
			tmp_zzq_yiliao = [time, zzq]
			list_zzq.append(tmp_zzq_yiliao)
			# 改进医疗——整体准确率
			n_tmp_zzq_yiliao = [time, n_zzq]
			n_list_zzq.append(n_tmp_zzq_yiliao)
			# 医疗——整体召回率
			tmp_zz_yiliao = [time, zz]
			list_zz.append(tmp_zz_yiliao)
			# 改进医疗——整体召回率
			n_tmp_zz_yiliao = [time, n_zz]
			n_list_zz.append(n_tmp_zz_yiliao)
			# 医疗——F1
			tmp_f1_yiliao = [time, f1]
			list_f1.append(tmp_f1_yiliao)
			# 改进医疗——F1
			n_tmp_f1_yiliao = [time, n_f1]
			n_list_f1.append(n_tmp_f1_yiliao)

	# 整体准确率
	content = list()
	for i in range(len(list_zzq)):
		for j in range(len(n_list_zzq)):
			if list_zzq[i][0] == n_list_zzq[j][0]:
				content_1 = [list_zzq[j][0], list_zzq[j][1], n_list_zzq[i][1]]
				content_1 = [n for n in content_1]
				content.append(content_1)
	content.sort(key=lambda x: (x[0], x[0]))
	# print content

	time_list = list()
	zzq_list = list()
	n_zzq_list = list()
	for a in content:
		time_list.append(a[0])
		zzq_list.append(a[1])
		n_zzq_list.append(a[2])

	# 整体召回率
	content2 = list()
	for i in range(len(list_zz)):
		for j in range(len(n_list_zz)):
			if list_zz[i][0] == n_list_zz[j][0]:
				content_1 = [list_zz[j][0], list_zz[j][1], n_list_zz[i][1]]
				content_1 = [n for n in content_1]
				content2.append(content_1)
	content2.sort(key=lambda x: (x[0], x[0]))
	# print content2

	zz_list = list()
	n_zz_list = list()
	for b in content2:
		zz_list.append(b[1])
		n_zz_list.append(b[2])

	# f1
	content3 = list()
	for i in range(len(list_f1)):
		for j in range(len(n_list_f1)):
			if list_f1[i][0] == n_list_f1[j][0]:
				content_1 = [list_f1[j][0], list_f1[j][1], n_list_f1[i][1]]
				content_1 = [n for n in content_1]
				content3.append(content_1)
	content3.sort(key=lambda x: (x[0], x[0]))
	# print content3

	f1_list = list()
	n_f1_list = list()
	for c in content3:
		f1_list.append(c[1])
		n_f1_list.append(c[2])

	time_list.insert(0, '标准（无预警）')
	zzq_list.insert(0, 0.857538)
	n_zzq_list.insert(0, 0.84014)
	zz_list.insert(0, 0.6695464)
	n_zz_list.insert(0,0.8071749)
	f1_list.insert(0, 0.7519709)
	n_f1_list.insert(0,0.8233276)


	DATA['time'] = time_list

	DATA['zzq_list'] = zzq_list
	DATA['n_zzq_list'] = n_zzq_list
	#
	DATA['zz_list'] = zz_list
	DATA['n_zz_list'] = n_zz_list
	#
	DATA['f1_list'] = f1_list
	DATA['n_f1_list'] = n_f1_list

	return render(request, 'zfmcshow2.html', {'DATA': json.dumps(DATA)})


if __name__ == '__main__':
	zfmcshow3()