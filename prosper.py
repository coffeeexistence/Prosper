import math
import locale
import shelve

locale.setlocale( locale.LC_ALL, '' )

def getArg(arg_arr, arg_name):
	return arg_arr[arg_arr.index(arg_name)+1]


def isArg(arg_arr, arg_name):
	try:
		arg_arr.index(arg_name)
	
	except ValueError:
		return False
	else:
		return True

def convert_input_to_array(input):
	str_cache=""
	return_arr=[]
	for x in input:
		if x == " ":
			return_arr.append(str_cache)
			str_cache=""
		else:
			str_cache+=x
	return_arr.append(str_cache)

	return return_arr

def cash(amount):
	return locale.currency( amount, grouping=True )

 
class financial_profile:
	

	def __init__(self, name):
		self.profile_db={
			'mandatory_costs' : {},
			'nonessential_costs' : {}, #Make sure to put in an array of 2 integers for nonessential, index 0 for value, 1 for priority
			'net_income' : 1
		}
		self.name = name

		database=shelve.open('./db/main.db', writeback=True)

		if str(name) in database:
			self.profile_db=database[str(name)]
			print("Using previously stored data of " + str(name) + " from database.")
		else:
			print("New profile, adding entry to database")
			database[str(name)]=self.profile_db

		database.close()

	def save(self):
		database=shelve.open('./db/main.db', writeback=True)
		database[str(self.name)]=self.profile_db
		database.close()


	def update_income(self, income):
		self.profile_db['net_income']=income
		print("Net income updated to "+str(income))

	def total_expenses(self):
		return self.nonessential_expenses()+self.mandatory_expenses()

	def mandatory_expenses(self):
		return_value=0
		for key, value in self.profile_db['mandatory_costs'].items():
			return_value+=value
		return return_value

	def nonessential_expenses(self):
		return_value=0
		for key, value in self.profile_db['nonessential_costs'].items():
			return_value+=value[0]
		return return_value

	def pre_spending_limit(self):
		monthly_income=self.profile_db['net_income']
		return (2 * (math.pow(4.5, math.log10(2*monthly_income) ) ) )
	
	def spending_limit(self):
		return self.pre_spending_limit()+self.total_expenses()

	def add_mandatory(self):
		print("please enter name of cost followed by a space, then the cost \nWhen finished, type 'done'\n")
		count=0
		while True:
			cost_input=input("")
			input_arr = convert_input_to_array(cost_input)
			if input_arr[0]=="done":
				print("Successfully added "+str(count)+" items!")
				break
			elif len(input_arr)==2:
				count+=1;
				self.profile_db['mandatory_costs'][input_arr[0]]=int(input_arr[1])

	def add_nonessential(self):
		print("Make entries in the following format: name - cost - importance(from 1 to 10) \nWhen finished, type 'done'\n")
		count=0
		while True:
			cost_input=input("")
			input_arr = convert_input_to_array(cost_input)
			if input_arr[0]=="done":
				print("Successfully added "+str(count)+" items!")
				break
			elif len(input_arr)==5:
				count+=1;
				self.profile_db['nonessential_costs'][input_arr[0]]=[input_arr[2],input_arr[4]]




profile=input("Enter profile name to get started: ")

user=financial_profile(profile)

print(user.profile_db)


user_input=""

while True:
	user_input=input("Enter command: $")

	if user_input == "add mandatory":
		user.add_mandatory()
	elif user_input == "add nonessential":
		user.add_nonessential()	
	elif "update net income" in user_input: 
		input_arr=convert_input_to_array(user_input)
		user.update_income(int(input_arr[3]))
	elif "show spending limit" in user_input: 
		print(cash(user.spending_limit()))
	elif "exit" in user_input: 
		cmd = input("Would you like to save?(Y/n):")
		if cmd.upper() == "Y":
			user.save()
			print("User's profile has been saved!")
		break
	elif "help" in user_input: 
		print("Prosper commands:_________________________")
		print('  "update net income"')
		print('  "add mandatory"')
		print('  "add nonessential"')
		print('  "show spending limit"')
		print('  "exit"')

	else:
		print('Invalid command ¯\_(ツ)_/¯ \nType "help" for well.. help')

		









