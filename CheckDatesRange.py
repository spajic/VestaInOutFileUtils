# Скрипт предназначен для определения интервалов дат, для которых в заданной папке есть выгрузки ОПЭТИ
# Файлы с выгрузками ОПЭТИ должны иметь вид yymmdd_+_DEN_dd.zip
import os
import datetime
import re
import unittest

class TestOPETI(unittest.TestCase):

  def test_YearFromOpetiString(self):
  	opeti_string = '150725'
  	self.assertEqual(year_from_opeti_string(opeti_string), 2015)

  def test_MonthFromOpetiString(self):
  	opeti_string = '150725'
  	self.assertEqual(month_from_opeti_string(opeti_string), 7)

  def test_DayFromOpetiString(self):
  	opeti_string = '150725'
  	self.assertEqual(day_from_opeti_string(opeti_string), 25)

  def test_DateFromOpetiString(self):
	opeti_string = '150725'
	opeti_date = datetime.date(2015, 7, 25)
	self.assertEqual(date_from_opeti_string(opeti_string), opeti_date)

  def test_GenerateDatesRange(self):
  	first_date = datetime.date(2015, 7, 25)
  	last_date = datetime.date(2015, 7, 28)
  	date_range = [
  		datetime.date(2015, 7, 25), 
  		datetime.date(2015, 7, 26),
  		datetime.date(2015, 7, 27),
  		datetime.date(2015, 7, 28)
  	]
  	self.assertEqual(generate_dates_range(first_date, last_date), date_range)

  def test_MatchOpetiSyntax(self): # Syntax: yymmdd_+_DEN_dd.zip
  	ok_opeti_string_1 = '150227_+_DEN_27.zip'
  	ok_opeti_string_2 = '150320_+_DEN_20.zip'
  	ok_opeti_string_3 = '150105_+_DEN_05.zip'
  	not_opeti_string_1 = 'readme.txt'
  	not_opeti_string_2 = '150105_+_DEN_05'
  	not_opeti_string_3 = '150105_+_DEN_05.rar'
  	self.assertEqual(match_opeti_syntax(ok_opeti_string_1), True)
  	self.assertEqual(match_opeti_syntax(ok_opeti_string_2), True)
  	self.assertEqual(match_opeti_syntax(ok_opeti_string_3), True)
  	self.assertEqual(match_opeti_syntax(not_opeti_string_1), False)
  	self.assertEqual(match_opeti_syntax(not_opeti_string_2), False)
  	self.assertEqual(match_opeti_syntax(not_opeti_string_3), False)
  
def match_opeti_syntax(file_name): # Syntax: yymmdd_+_DEN_dd.zip
	return ( re.match('^\d{6}_\+_DEN_\d\d\.zip$', file_name) != None )

def year_from_opeti_string(opeti_string): # opeti_string вида вида yymmdd
	return int(opeti_string[0:2]) + 2000

def month_from_opeti_string(opeti_string): # opeti_string вида вида yymmdd
	return int(opeti_string[2:4])

def day_from_opeti_string(opeti_string): # opeti_string вида вида yymmdd
	return int(opeti_string[4:6])

def date_from_opeti_string(opeti_string): # opeti_string вида вида yymmdd
	return datetime.date(
		year_from_opeti_string(opeti_string), 
		month_from_opeti_string(opeti_string), 
		day_from_opeti_string(opeti_string)
	)
def generate_dates_range(first_date, last_date):
	dates_range = [
		first_date + datetime.timedelta(days = i) for i in range((last_date - first_date).days+1)]
  	return dates_range	

# Запускаем unit-тесты
suite = unittest.TestLoader().loadTestsFromTestCase(TestOPETI)
unittest.TextTestRunner(verbosity=2).run(suite)

opeti_path = u'C:\\work\\python\\VestaInOutFilesUtils\\OPETI_EXAMPLE'
#opeti_path = u"C:\\BitTorrent Sync\\Rackstation\\Газ\\ПИТЕР 2015\\Выгрузки ОПЭТИ\\2015"

# Оставляем только файлы вида yymmdd_+_DEN_dd.zip и берём первые 6 символов yymmdd
file_names =  [f[:6] for f in os.listdir(opeti_path) if match_opeti_syntax(f)] 
present_dates = [date_from_opeti_string(f) for f in file_names]
present_dates.sort()
first_date = present_dates[0]
last_date = present_dates[-1]
all_dates = generate_dates_range(first_date, last_date)
absent_dates = list(set(all_dates) - set(present_dates))
absent_dates.sort()

print('First Date is: ' + str(first_date))
print('Last Date is: ' + str(last_date))
print('Absent dates: ')
for d in absent_dates:
	print(d)