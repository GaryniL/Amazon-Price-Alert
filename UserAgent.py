import random

class UserAgent:
	agent = {}

	def random(self):
		self.get_platform()
		self.get_os()
		self.get_browser()

		if self.agent['browser'] == 'Chrome':
			webkit = str(random.randint(500, 599))
			version = "%s.0%s.%s"%(str(random.randint(0, 24)), str(random.randint(0, 1500)), str(random.randint(0, 999)))

			return "Mozilla/5.0 (%s) AppleWebKit/%s.0 (KHTML, live Gecko) Chrome/%s Safari/%s"%(self.agent['os'], webkit, version, webkit)
		elif self.agent['browser'] == 'Firefox':
			year = str(random.randint(2000, 2015))
			month = str(random.randint(1, 12)).zfill(2)
			day = str(random.randint(1, 28)).zfill(2)
			gecko = "%s%s%s"%(year, month, day)
			version = "%s.0"%(str(random.randint(1, 15)))

			return "Mozillia/5.0 (%s; rv:%s) Gecko/%s Firefox/%s"%(self.agent['os'], version, gecko, version)
		elif self.agent['browser'] == 'IE':
			version = "%s.0"%(str(random.randint(1, 10)))
			engine = "%s.0"%(str(random.randint(1, 5)))
			option = random.choice([True, False])
			if option:
				token = "%s;"%(random.choice(['.NET CLR', 'SV1', 'Tablet PC', 'Win64; IA64', 'Win64; x64', 'WOW64']))
			else:
				token = ''

			return "Mozilla/5.0 (compatible; MSIE %s; %s; %sTrident/%s)"%(version, self.agent['os'], token, engine)

	def get_os(self):
		if self.agent['platform'] == 'Machintosh':
			self.agent['os'] = random.choice(['68K', 'PPC'])
		elif self.agent['platform'] == 'Windows':
			self.agent['os'] = random.choice(['Win3.11', 'WinNT3.51', 'WinNT4.0', 'Windows NT 5.0', 'Windows NT 5.1', 'Windows NT 5.2', 'Windows NT 6.0', 'Windows NT 6.1', 'Windows NT 6.2', 'Win95', 'Win98', 'Win 9x 4.90', 'WindowsCE'])
		elif self.agent['platform'] == 'X11':
			self.agent['os'] = random.choice(['Linux i686', 'Linux x86_64'])

	def get_browser(self):
		self.agent['browser'] = random.choice(['Chrome', 'Firefox', 'IE'])

	def get_platform(self):
		self.agent['platform'] = random.choice(['Machintosh', 'Windows', 'X11'])
