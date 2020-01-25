#!/usr/bin/env python

import sys, getopt
import numpy as np
import pandas as pd
import copy

class Cohort:
	def __init__(self, name, nstud, startsem, currsem, tuition, randb, sfees, aid, f_res,ret,grad):
		self._name = name
		self._nstud = int(nstud)
		self._startsem = int(startsem)
		self._currsem = int(currsem)
		self._randb = randb
		self._sfees = sfees
		self._aid = aid
		self._f_res = f_res 
		self._retention = ret
		self._grad = int(grad)
		self._tui_yr = {  # check that these are not off by 1 - year is END of academic year
			2017:34611,	# 17305.5
			2018:35735,	# 17876.5
			2019:36975,	# 18487.5
			2020: 38355,	# 19177.5
			2021: 39497,	# 19748.5
			2022: 40673,	# 20336.5
			2023: 41893,	# 20946.5
			2024: 43194	# 21597.0
		}
		self._gr_tui_yr = {  # check that these are not off by 1 - year is END of academic year
			2017:16068,	
			2018:15147,
			2019:15191,
			2020: 17869,
			2021: 17869,
			2022: 17869,
			2023: 17869,
			2024: 17869
		}
		self.set_tuition()


	def __repr__(self):
		print("%s, %d, %d, %d, %6.2f, %6.2f, %6.2f, %6.2f %6.2f" % (self._name,self._nstud,self._startsem,self._currsem,self._tuition,self._randb, self._sfees, self._aid, self._f_res))
#		s = "%s:\n\tnstud: %s\n\tstartsem: %s\n\tcurrsem: %s\n\ttuition: %s\n\trandb: %s\n\tfees: %s\n\taid: %s\n\tf_res: %s\n" % (self._name,self._nstud,self._startsem,self._currsem,self._tuition,self._randb, self._sfees, self._aid, self._f_res)
		s = ""
		return s

	def print_c(self):
		print("%d %s, %d, %d, %d, %6.2f, %6.2f, %6.2f, %6.2f %6.2f" % (self.isemester(), self._name,self._nstud,self._startsem,self._currsem,self._tuition,self._randb, self._sfees, self._aid, self._f_res))
		# print('isemester: '+str(c.isemester()))


#	def use_real_tuition(self):
#		self._realtuition = True
#		self._tuition = self._tui_yr[self.year()]/2.0

	def set_tuition(self):
		if self._grad == 1:
			self._tuition = self._gr_tui_yr[self.year()]
		else:
			self._tuition = self._tui_yr[self.year()]/2.0

	def add_transfers(self,ntrans):
		self._nstud+=ntrans

	def tui(self):
		return self._nstud*(self._tuition)

	def fees(self):
		return self._nstud*(self._sfees)

	def financial_aid(self):
		return self._nstud*self._aid

	def tui_fees(self):
		return self.tui()+self.fees()

	def rev(self):
		return self.tui_fees()+self.randb()

	def randb(self):
		return self._nstud*(self._randb)*self._f_res

	def isemester(self):
		syear = self._startsem/100
		ssem = self._startsem%100
		cyear = self._currsem/100
		csem = self._currsem%100
		return (csem-ssem)/10 + 2*(cyear-syear)

	def iyear(self):
		syear = self._startsem/100
		cyear = self._currsem/100
		return (cyear-syear)

	def year(self):
		return self._currsem/100

	def age(self):
		cyear = self._currsem/100
		csem = self._currsem%100
		if csem == 30:
			#add 10 to semester
			csem += 10
#			print(cyear*100+csem)
			self._currsem = cyear*100+csem
		elif csem == 40:
			#add 1 to year and set csem to 30
			cyear += 1
			csem = 30
#			print(cyear*100+csem)
			self._currsem = cyear*100+csem
		else:
			print('bad semester in .age()')

		#update values
		
		self._nstud = self._retention[self.isemester()-1]*self._nstud  # QQ: need to add in transfers
		self._randb = 1.0275*self._randb # QQ: how to model r&b increases?
		# self._sfees = sfees # QQ: how to model fee increases?
		# self._aid = aid # QQ: is aid truly flat?
		# self._f_res = f_res  # QQ: does fraction of residents change?
		
		return self




def read_cohorts(d, semester):
	cc = []		
	for i, r in d.iterrows():
		if (d['stype'][i] != 'comment') and (d['semester'][i] == semester) :
			ret =[d['r2'][i],d['r3'][i],d['r4'][i],d['r5'][i],d['r6'][i],d['r7'][i],d['r8'][i],d['r9'][i],d['r10'][i],d['r11'][i],d['r12'][i]]
			cc.append(Cohort(d['name'][i],d['nstud'][i],d['startsem'][i],d['semester'][i],d['tuition'][i],d['randb'][i],d['fees'][i],d['aid'][i],d['f_res'][i], ret, d['grad'][i]  ))
	return cc


def add_cohorts(cc,d,semester):
	# we should add a test here to make sure we are starting in the fall
	# loop over data frame and find cohorts starting in *semester*
	for i, r in d.iterrows():
		if d['startsem'][i] == semester :
			ret =[d['r2'][i],d['r3'][i],d['r4'][i],d['r5'][i],d['r6'][i],d['r7'][i],d['r8'][i],d['r9'][i],d['r10'][i],d['r11'][i],d['r12'][i]]
			cc.append(Cohort(d['name'][i],d['nstud'][i],d['startsem'][i],d['semester'][i],d['tuition'][i],d['randb'][i],d['fees'][i],d['aid'][i],d['f_res'][i], ret, d['grad'][i]  ))
	return cc

def reset_tuition(cc):
	for c in cc:
		c.set_tuition()

def tot_tui(cc):
	# loop over cohorts and add tuition and fees
	tot_tui = 0
	for c in cc:
		tot_tui+= c.tui()
	return tot_tui

def tot_fees(cc):
	# loop over cohorts and add tuition and fees
	tot_fees = 0
	for c in cc:
		tot_fees+= c.fees()
	return tot_fees

def tot_tui_fees(cc):
	# loop over cohorts and add tuition and fees
	tot_tui_fees = 0
	for c in cc:
		tot_tui_fees+= c.tui_fees()
	return tot_tui_fees

def tot_rev(cc):
	# loop over cohorts and add revenues
	tot_stud_rev = 0
	for c in cc:
		tot_stud_rev+= c.rev()
	return tot_stud_rev

def tot_aid(cc):
	# loop over cohorts and add aid
	tot_stud_aid = 0
	for c in cc:
		tot_stud_aid+= c.financial_aid()
	return tot_stud_aid

def tot_randb(cc):
	# loop over cohorts and add aid
	tot_randb = 0
	for c in cc:
		tot_randb+= c.randb()
	return tot_randb

def print_cohorts(cc):
	cc.sort(key= lambda x: (x._startsem, -x._currsem))
	for c in cc:
		c.print_c()
		
def print_budget(cc):
	print('tuition:\t% 11.2f' % (tot_tui(cc)))
	print('stud. aid:\t% 11.2f' % (tot_aid(cc)))
	print('net trev.:\t% 11.2f'% (tot_tui(cc)-tot_aid(cc)))
	print('fees:   \t% 11.2f'% (tot_fees(cc)))
	print('randb:  \t% 11.2f' % (tot_randb(cc)))
	print('net rev.:\t% 11.2f' % (tot_tui(cc)-tot_aid(cc)+tot_fees(cc)+tot_randb(cc) ))


printcohorts = False

def print_report(f,s,y):
	global printcohorts
	print('\n')
#	print('fall:')
#	print_cohorts(f)
#	print('spring:')
#	print_cohorts(s)
#	print('fall:')
#	print_budget(f)
#	print('spring:')
#	print_budget(s)
#	print('year:')
	if printcohorts == True :
		print_cohorts(f)
		print_cohorts(s)
	print_budget(y)
	print('dis. rate:\t'+str(tot_aid(y)/tot_tui_fees(y)))

def gen_spring(fall, spring,df):
	for c in fall:
		cc = copy.deepcopy(c)
		cc.age()
		spring.append(cc)
		csem = cc._currsem
	add_cohorts(spring,df,csem)
		
	
def gen_nextfall(spring, df):
	# find the current year
	nextfall = []
	oyear = spring[0].year()
	deltayear = 1
	for c in spring:
		if c.isemester() <= 10 : # dont advance 12th semester (isemester == 11)
			cc = copy.deepcopy(c)
			cc.age()
			nextfall.append(cc)
	# add next freshman class - ex 202130
	csemester = (oyear + deltayear)*100 + 30
	add_cohorts(nextfall,df,csemester)
	reset_tuition(nextfall)
	return(nextfall)	




def main(argv):
	global printcohorts
	inputfile = 'current.xlsx'
	outputfile = ''


	try:
		opts, args = getopt.getopt(argv,"hci:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'simbud.py -c -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'simbud.py -c -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-c"):
			print('setting printcohorts')
			printcohorts = True
			print(printcohorts)
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg

	df = pd.read_excel("data/"+inputfile)
	fall1 = read_cohorts(df, 202030)


#do the first year

	spring1 = []
	gen_spring(fall1, spring1,df)
	year1 = fall1 + spring1
	print_report(fall1,spring1,year1)


# do the next year

	fall2 = []
	spring2 = []
	fall2 = gen_nextfall(spring1,df)
	gen_spring(fall2, spring2,df)
	year2 = fall2 + spring2
	print_report(fall2,spring2,year2)


# do the next next year

	fall3 = []
	spring3 = []
	fall3 = gen_nextfall(spring2,df)
	gen_spring(fall3, spring3,df)
	year3 = fall3 + spring3
	print_report(fall3,spring3,year3)





if __name__ == "__main__":
	main(sys.argv[1:])

