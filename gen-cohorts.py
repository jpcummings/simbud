#!/usr/bin/env python

import sys, getopt
import pandas as pd
import numpy as np
import math

def analyze_cohort(df, firstsem):
	print('Cohort: '+str(firstsem))
	df = df[(df['first_term']==firstsem) & (df['cohort_type']=='First-Time') & (df['UG_Flag']==1)]
	mean = df.mean().fillna(0)
	sum = df.sum().fillna(0)
	count = df.count().fillna(0)

	
	for i in range(1,12):
		n = count['ug_tuition_trm'+str(i)]
		nres = count['housing_trm'+str(i)]
		tuition = mean['ug_tuition_trm'+str(i)]
		randb = mean['housing_trm'+str(i)] + mean['meals_trm'+str(i)]
		if n!=0:
			fees = sum['course_fees_trm'+str(i)]/n \
				+ sum['traveL_crse_fees_trm'+str(i)]/n \
				+ sum['student_conduct_fines_trm'+str(i)]/n \
				+ sum['SofB_fee_trm'+str(i)]/n \
				+ sum['housing_extra_trm'+str(i)]/n \
				+ sum['housing_misc_trm'+str(i)]/n \
				+ sum['fees_trm'+str(i)]/n \
				+ sum['health_ins_trm'+str(i)]/n \
				+ sum['parking_trm'+str(i)]/n \
				+ sum['misc_fees_trm'+str(i)]/n \
				+ sum['tuit_exchg_trm'+str(i)]/n \
				+ sum['grad_dipl_fee_trm'+str(i)]/n \
				+ sum['fees_w_exp_trm'+str(i)]/n
			aid = sum['unrestricted_iaid_trm'+str(i)]/n \
				+ sum['restricted_iaid_trm'+str(i)]/n
			f_res = float(nres)/float(n)
		else:
			fees = 0.0
			aid = 0.0
			f_res =0.0

#		print('trm'+str(i)+':')
#		print('n:'+str(n) )
#		print('nres:'+str(nres) )
#		print('f_res:'+str(f_res) )
#		print('tuition: '+str(tuition) )
#		print('randb: '+str(randb) )
#		print('fees: '+str(fees) )
#		print('aid: '+str(aid) )

		print( '%3d, %6d, %6d, %5.2f, %5.2f, %5.2f, %5.2f, %.2f'  % (n, firstsem, firstsem, tuition, randb, fees, aid, f_res))

def retention(df, firstsem):
	df = df[(df['first_term']==firstsem) & (df['cohort_type']=='First-Time') & (df['UG_Flag']==1)]
	mean = df.mean().fillna(0)
	sum = df.sum().fillna(0)
	count = df.count().fillna(0)
	
	ret = []
	for i in range(1,11):
		n1 =  count['ug_tuition_trm'+str(i)]
		n2 =  count['ug_tuition_trm'+str(i+1)]
		if n1 != 0:
			ret.append(float(n2)/float(n1))
		else:
			ret.append(0.0)
	print(ret)

def analyze_nsem(df,firstsem,n):
	df = df[(df['first_term']==firstsem) & (df['cohort_type']=='First-Time') & (df['UG_Flag']==1)]
	mean = df.mean().fillna(0)
	sum = df.sum().fillna(0)
	count = df.count().fillna(0)

	i = n
	n = count['ug_tuition_trm'+str(i)]
	nwa = count['sa_wsh_tuition_trm'+str(i)]
	nres = count['housing_trm'+str(i)]
#	tuition = mean['ug_tuition_trm'+str(i)]
	tuition = (sum['ug_tuition_trm'+str(i)] \
			+ sum['sa_wsh_tuition_trm'+str(i)])/(n+nwa)
	randb = mean['housing_trm'+str(i)] + mean['meals_trm'+str(i)]
	if n!=0:
		fees = (sum['course_fees_trm'+str(i)] \
			+ sum['traveL_crse_fees_trm'+str(i)] \
			+ sum['student_conduct_fines_trm'+str(i)] \
			+ sum['SofB_fee_trm'+str(i)]/n \
			+ sum['housing_extra_trm'+str(i)] \
			+ sum['housing_misc_trm'+str(i)] \
			+ sum['fees_trm'+str(i)] \
			+ sum['health_ins_trm'+str(i)] \
			+ sum['parking_trm'+str(i)] \
			+ sum['misc_fees_trm'+str(i)] \
			+ sum['tuit_exchg_trm'+str(i)] \
			+ sum['grad_dipl_fee_trm'+str(i)] \
			+ sum['fees_w_exp_trm'+str(i)])/n
		aid = (sum['unrestricted_iaid_trm'+str(i)] \
			+ sum['restricted_iaid_trm'+str(i)])/n
		f_res = float(nres)/float(n)
	else:
		fees = 0.0
		aid = 0.0
		f_res =0.0

	print( '%3d, %6d, %6d, %5.2f, %5.2f, %5.2f, %5.2f, %.2f'  % (n, firstsem, firstsem, tuition, randb, fees, aid, f_res))

def analyze_nsem_gr(df,firstsem,n):
	df = df[(df['gr_first_term']==firstsem) & (df['GR_Flag']==1)]
	mean = df.mean().fillna(0)
	sum = df.sum().fillna(0)
	count = df.count().fillna(0)

	i = n
	n = count['GR_tuition_MSA_trm'+str(i)]
	nmba = count['GR_tuition_MBA_CERT_trm'+str(i)]
	nres = count['housing_gr_trm'+str(i)]
	tuition = (sum['GR_tuition_MSA_trm'+str(i)] \
			+ sum['GR_tuition_MBA_CERT_trm'+str(i)])/(n+nmba)
	randb = mean['housing_gr_trm'+str(i)] + mean['meals_gr_trm'+str(i)]
	if n!=0:
		fees = (sum['fees_gr_trm'+str(i)] \
			+ sum['health_ins_gr_trm'+str(i)] \
			+ sum['parking_gr_trm'+str(i)] \
			+ sum['misc_fees_gr_trm'+str(i)] \
			+ sum['grad_dipl_fee_gr_trm'+str(i)] \
			+ sum['fees_w_exp_gr_trm'+str(i)])/n
		aid = (sum['unrestricted_iaid_gr_trm'+str(i)])/n
		f_res = float(nres)/float(n)
	else:
		fees = 0.0
		aid = 0.0
		f_res =0.0

	print( 'grad%s, %3d, %6d, %6d, %5.2f, %5.2f, %5.2f, %5.2f, %.2f'  % (year(firstsem,4), n+nmba, firstsem, firstsem, tuition, randb, fees, aid, f_res))

def year(semester,isem):
	year = semester/100
	sem = semester%100
	deltayear = (isem+1)/2
	return year+deltayear

def anal_nsem(df,firstsem,i):
	df = df[(df['first_term']==firstsem) & (df['cohort_type']=='First-Time') & (df['UG_Flag']==1)]
	mean = df.mean().fillna(0)
	sum = df.sum().fillna(0)
	count = df.count().fillna(0)

	n = count['ug_tuition_trm'+str(i)]
	nwa = count['sa_wsh_tuition_trm'+str(i)]
	nres = count['housing_trm'+str(i)]
	tuition = (sum['ug_tuition_trm'+str(i)] \
			+ sum['sa_wsh_tuition_trm'+str(i)])/(n+nwa)
	room = mean['housing_trm'+str(i)] 
	board = mean['meals_trm'+str(i)]
	randb = mean['housing_trm'+str(i)] + mean['meals_trm'+str(i)]  # assume 1:1 correspendence
	if n!=0:
		fees = (sum['course_fees_trm'+str(i)] \
			+ sum['traveL_crse_fees_trm'+str(i)] \
			+ sum['student_conduct_fines_trm'+str(i)] \
			+ sum['SofB_fee_trm'+str(i)]/n \
			+ sum['housing_extra_trm'+str(i)] \
			+ sum['housing_misc_trm'+str(i)] \
			+ sum['fees_trm'+str(i)] \
			+ sum['health_ins_trm'+str(i)] \
			+ sum['parking_trm'+str(i)] \
			+ sum['misc_fees_trm'+str(i)] \
			+ sum['tuit_exchg_trm'+str(i)] \
			+ sum['grad_dipl_fee_trm'+str(i)] \
			+ sum['fees_w_exp_trm'+str(i)])/n
		aid = (sum['unrestricted_iaid_trm'+str(i)] \
			+ sum['restricted_iaid_trm'+str(i)])/n
		f_res = float(nres)/float(n)
	else:
		fees = 0.0
		aid = 0.0
		f_res =0.0

	print('first semester: '+str(firstsem) + '  semester: '+str(i))
	print('year: '+str(year(firstsem,i)))
#	print('n: %3d nwa %3d nres %3d' % (n,nwa,nres))
	print('tuition: %5.2f aid: %5.2f  fees %5.2f room: %5.2f board: %5.2f' % (tuition, aid, fees, room, board))

def anal_part_time(df):
	for i in range(1,12):
		if df[][] < 12 :
			nptsem +=11
		elif df[][] >= 12 :
			nftsem += 1
		else:
			nsem +=1
	print
	
def psummary(df):
	dz = df.fillna(0)
	f_res = 0

	for i in range(1,12) :
		dz['tuition'] = dz['ug_tuition_trm'+str(i)] 
#				+ dz['sa_wsh_tuition_trm'+str(i)]
		dz['tot_fees'] = dz['course_fees_trm'+str(i)] \
			+ dz['traveL_crse_fees_trm'+str(i)] \
			+ dz['student_conduct_fines_trm'+str(i)] \
			+ dz['SofB_fee_trm'+str(i)] \
			+ dz['housing_extra_trm'+str(i)] \
			+ dz['housing_misc_trm'+str(i)] \
			+ dz['fees_trm'+str(i)] \
			+ dz['health_ins_trm'+str(i)] \
			+ dz['parking_trm'+str(i)] \
			+ dz['misc_fees_trm'+str(i)] \
			+ dz['tuit_exchg_trm'+str(i)] \
			+ dz['grad_dipl_fee_trm'+str(i)] \
			+ dz['fees_w_exp_trm'+str(i)]
		dz['randb'] = df['housing_trm'+str(i)] + df['meals_trm'+str(i)]  # assume 1:1 correspendence
		dz['tot_aid'] = dz['unrestricted_iaid_trm'+str(i)] \
			+ dz['restricted_iaid_trm'+str(i)]

		dd=dz.replace(0,np.nan)
		count = dd.count().fillna(0)
		mean = dd.mean().fillna(0)
	
		n = count['ug_tuition_trm'+str(i)]
		nwa = count['sa_wsh_tuition_trm'+str(i)]
		nres = count['housing_trm'+str(i)]
		tuition = mean['tuition']
		fees = mean['tot_fees']
		room = mean['housing_trm'+str(i)] 
		board = mean['meals_trm'+str(i)]
		randb = mean['randb']
		aid =  mean['tot_aid']
		if n != 0 :
			f_res = float(nres)/float(n)
		else:
			f_res = 0.0
	
		print('%5d %5d %5.2f %5.2f %5.2f %5.2f %5.2f' % (i, n, tuition, fees, randb, aid, f_res))

def pgradsummary(df):
	dz = df.fillna(0)
	f_res = 0

	for i in range(1,3) :
		dz['tuition'] = dz['GR_tuition_MSA_trm'+str(i)] \
				+ dz['GR_tuition_MBA_CERT_trm'+str(i)]
		dz['tot_fees'] = dz['fees_gr_trm'+str(i)] \
			+ dz['parking_gr_trm'+str(i)] \
			+ dz['misc_fees_gr_trm'+str(i)] \
			+ dz['grad_dipl_fee_gr_trm'+str(i)]
#			+ dz['health_ins_gr_trm'+str(i)] \
#			+ dz['fees_w_exp_gr_trm'+str(i)]
#			+ dz['housing_extra_gr_trm'+str(i)] \
#			+ dz['housing_misc_gr_trm'+str(i)] \
#			+ dz['SofB_fee_gr_trm'+str(i)] \
#			+ dz['course_fees_gr_trm'+str(i)] 			
		dz['randb'] = df['housing_gr_trm'+str(i)] + df['meals_gr_trm'+str(i)]  # assume 1:1 correspendence
		dz['tot_aid'] = dz['unrestricted_iaid_gr_trm'+str(i)] \
			+ dz['restricted_iaid_gr_trm'+str(i)]

		dd=dz.replace(0,np.nan)
		count = dd.count().fillna(0)
		mean = dd.mean().fillna(0)
	
		nmsa = count['GR_tuition_MSA_trm'+str(i)]
		nmba = count['GR_tuition_MBA_CERT_trm'+str(i)]
		n = nmba + nmsa
		nres = count['housing_gr_trm'+str(i)]
		tuition = mean['tuition']
		fees = mean['tot_fees']
		room = mean['housing_gr_trm'+str(i)] 
		board = mean['meals_gr_trm'+str(i)]
		randb = mean['randb']
		aid =  mean['tot_aid']
		if n != 0 :
			f_res = float(nres)/float(n)
		else:
			f_res = 0.0
	
		print('%5d %5d %5.2f %5.2f %5.2f %5.2f %5.2f' % (i, n, tuition, fees, randb, aid, f_res))

def get_total_aid(df,semester):
	dd = df[(df['first_term']<=semester) & (df['UG_Flag']==1)]
	aid=0.0
	for i, r in dd.iterrows(): # unrestricted_iaid_trm?
		y1 =  int(semester/100)
		y2 =  int(r['first_term']/100)
		y =  y1 - y2
		s1 = int(semester%100)
		s2 = int(r['first_term']%100)
		s = s1-s2
		trm = y*2+s/10 +1
#		print('%d %d %d %d %d' % (semester, r['first_term'], y,s,trm))
		if (trm <=11):
			if math.isnan(r['unrestricted_iaid_trm'+str(trm)]) == False:
				aid += (r['unrestricted_iaid_trm'+str(trm)])
			if math.isnan(r['restricted_iaid_trm'+str(trm)]) == False:
				aid += (r['restricted_iaid_trm'+str(trm)])

	return aid
	


def main(argv):
	inputfile = "student_data_for_financial_modeling.xlsx"
	cohort = 'First-Time'
	ug_flag = 1
	gr_flag = 0
	athlete = 0

	try:
		opts, args = getopt.getopt(argv,"hgtai:c:",["ifile="])
	except getopt.GetoptError:
		print 'gen-cohorts.py -g -t -a -c (Fall|Spring|First-Time|Transfer) -i <inputfile> '
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'gen-cohorts.py -g -t -a -c (Fall|Spring|First-Time|Transfer) -i <inputfile> '
			sys.exit()
		elif opt in ("-t"):
			cohort = 'Transfer'
		elif opt in ("-c"):
			cohort = arg
		elif opt in ("-a"):
			athlete = 1
		elif opt in ("-g"):
			ug_flag = 0
			gr_flag = 1
		elif opt in ("-i", "--ifile"):
			inputfile = arg

	fterm = args[0]
	df = pd.read_excel(inputfile)

	if ug_flag==1 :
		d = df[ df['first_term']==int(fterm) ]
		d = d[ d['cohort_type']== cohort ]
		d = d[ d['UG_Flag']==1 ]
		if athlete == 1:
			d = d[ d['athlete_roster_trm1'] == 1 ]
		psummary(d)
	else:
		print("grad studets")
		d = df[ df['gr_first_term']==int(fterm) ]
		d = d[ d['term_type_GR']== cohort ]
		d = d[ d['GR_Flag']==1 ]
		if athlete == 1:
			d = d[ d['athlete_roster_trm1'] == 1 ]
		pgradsummary(d)
	
	
if __name__ == "__main__":
	main(sys.argv[1:])

