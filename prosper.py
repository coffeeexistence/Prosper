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
			'optional_costs' : {},
			'mo_income_sans_taxes' : 0
		}
		self.name = name

		database=shelve.open('./db/main.db', writeback=True)

		if str(name) in database:
			profile_db=database[str(name)]
			print("Using previously stored data of " + str(name) + " from database.")
		else:
			print("New profile, adding entry to database")
			database[str(name)]=self.profile_db

		database.close()

	def pre_spending_limit():
		monthly_income=self.profile_db['mo_income_sans_taxes']
		return (2 * (math.pow (4.5, math.log10 (2*monthly_income) ) ) )
	
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


profile=input("Enter profile name to get started: ")

user=financial_profile(profile)

print(user.profile_db)



