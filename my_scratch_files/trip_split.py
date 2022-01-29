import os, random
from operator import itemgetter
from collections import Counter

# Open tripdescription file
#check if file exists
#file1_exists = os.path.exists('trip_description.txt')
file1_exists = os.path.exists('trip_description.txt')
if not file1_exists:
   print("execution of trip_split.py was terminated")
   print("trip_description.txt does not exists")
   print("it is neccesary to run flie_splits_v2.py first")
   exit()

file1 = open('trip_description.txt', 'r')
lines = file1.readlines()

# Read information in trip_description.py
trip_info = [[]*5]
for line in lines:
    if not line.startswith("#"):
       line_info = line.split('\t')
       trip_info.append([line_info[0].strip(),line_info[1].strip(),\
       line_info[2].strip(),line_info[3].strip(),line_info[4].strip()])

trip_info = [x for x in trip_info if x] #Remove any empty list elements
#Checking the number of occurences in the trip list
counted = Counter([item for sublist in trip_info for item in sublist])
n_density = [0]*2 #Key, Number of cases with[high density, low density]
n_density[0] = counted.get('low', 'not found!')
n_density[1] = counted.get('high', 'not found!')
n_density_key = ['low','high']
n_light = [0]*2 #Key, Number of cases [day, night]
n_light[0] = counted.get('day', 'not found!')
n_light[1] = counted.get('night', 'not found!')
n_light_key = ['day','night']
n_weather = [0]*2 #Key, Number of cases [bad, fair]
n_weather[0] = counted.get('bad', 'not found!')
n_weather[1] = counted.get('fair', 'not found!')
n_weather_key = ['bad','fair']

#Consolidate the contidions
#n_conditions = n_density + n_light + n_weather

print("Object density info")
print("Number of trips with low object density  = {}".format(n_density[0]))
print("Number of trips with high object density = {}".format(n_density[1]))
print("Light conditions info")
print("Number of trips during day   = {}".format(n_light[0]))
print("Number of trips during night = {}".format(n_light[1]))
print("weather info")
print("Number of trips with bad weather  = {}".format(n_weather[0]))
print("Number of trips with fair weather = {}".format(n_weather[1]))

#Splits
data_splits = {"test":0.10,"validation":0.15,"training":0.75} #Key, [test fraction,validation fraction, training fraction]

#Conditions arrays
#{Order of iteration:{"Name of condition","Variable"}}
def choose_conditions(cond_select):
    data_cond = []
    data_key  = []
    if cond_select == "weather":
       data_cond = n_weather
       data_key  = n_weather_key
    if cond_select == "light":
       data_cond = n_light
       data_key  = n_light_key
    if cond_select == "density":
       data_cond = n_density
       data_key  = n_density_key
    return data_cond, data_key

n_cond = {0:"weather",1:"light",2:"density"} 

splits_order = ["test","validation"] 

test_per_cat  = [0,0,0] #Number of test cases by category, [0]->weather, [1]-> light, [2]->density
val_per_cat   = [0,0,0] #Number of test cases by category, [0]->weather, [1]-> light, [2]->density

for cond in sorted(n_cond):
    print("********** {} **********************".format(n_cond[cond]))
    cond_array, cond_array_key = choose_conditions(n_cond[cond])
    cond_array_sort     = sorted(cond_array)
    cond_array_key_sort = sorted(range(len(cond_array)),key=lambda k: cond_array[k])

    for i_split in splits_order:
        split_fract = data_splits[i_split]
        print(i_split)
    
        for i_trips in range(len(cond_array_sort) - 1):
            n_trips      = cond_array_sort[i_trips]
            trip_id_cond = cond_array_key[ cond_array_key_sort[i_trips] ]
            #print(n_trips)
            n_select = round(split_fract * n_trips)
            print("Number of trips in {} with {} conditions for {} dataset = {}".format(n_cond[cond],trip_id_cond,i_split,n_select))
            if i_split == "test":
               test_per_cat[cond] = n_select
            if i_split == "validation":
               val_per_cat[cond] = n_select
print(test_per_cat) 
print(val_per_cat) 

n_trip_select = [i for i in range(len(trip_info))]
#print(n_trip_select)
n_list_test  = []
n_list_val   = []
n_list_train = []
cond_org = {0:[4,"bad"],1:[3,"night"],2:[2,"high"]}
cond_fair = {0:[4,"fair"],1:[3,"day"],2:[2,"low"]}

#Loop through test and validation splits 
#SECTION #1 of test and validation splits
#SELECT trips with weather=bad, light = night, object density = high
for i_split in splits_order:

    #Loop through weather, light, object density
    for i_cond in sorted(n_cond):

        #number of trips for test/val and for specific condition (e.g. weather, light and object density)
        n_trips = test_per_cat[i_cond] if i_split=="test" else val_per_cat[i_cond]
        for i_random in range(n_trips):
           add_to_list=False
           while not add_to_list:
             random_index = random.randint(0,len(n_trip_select)-1)
             trip_select_index = n_trip_select[random_index]
                
             #Set counters to keep all the bad trip conditions to match the total number of cases \
             #in test_per_cat in val_per_cat
             temp_counter = test_per_cat if i_split=="test" else val_per_cat
             checks = [False]*len(n_cond)
             cond_counter = [False]*len(n_cond)
             #Check conditions
             for i_checks in sorted(n_cond): #Get the main condition: weather=bad, light=night, object density = high
                 temp_check = trip_info[trip_select_index][cond_org[i_checks][0]]
                 checks[i_checks] = True if temp_check == cond_org[i_checks][1] else False #Check main condition
                 #look for the other conditions, it is not allow to grab more trips that the ones already prescibed \
                 #in test_per_cat in val_per_cat
                 temp_counter_check = temp_counter[i_checks] - 1 if checks[i_checks] else temp_counter[i_checks]
                 cond_counter[i_checks] = True if temp_counter_check >= 0 else False
                
             all_true_counter = sum(cond_counter)
             if checks[i_cond] and all_true_counter==3: #Matches trip condition and that all counters are positive
                add_to_list=True
                if i_split == "test":                   
                   #Add trip to split
                   n_list_test.append(trip_info[trip_select_index])
                   #Remove Trip from main trip list = test
                   n_trip_select.pop(random_index)
                   for i_checks in sorted(n_cond):
                       test_per_cat[i_checks] = temp_counter[i_checks] - 1 if checks[i_checks] else temp_counter[i_checks]
                else:                
                   #Add trip to split=Validation
                   n_list_val.append(trip_info[trip_select_index])
                   #Remove Trip from main trip list
                   n_trip_select.pop(random_index)
                   for i_checks in sorted(n_cond):
                       val_per_cat[i_checks] = temp_counter[i_checks] - 1 if checks[i_checks] else temp_counter[i_checks]

                        
entries_test = len(n_list_test)
entries_val  = len(n_list_val)           

#SECTION #2 of test and validation splits
#SELECT trips with weather=fair, light = day, object density = low
#Loop through test and validation splits 
for i_split in splits_order: ###Note: I need to update the split order
    
    #Number of trips left per split
    n_trips = round(len(trip_info)*data_splits[i_split]) - entries_test if i_split=="test" else round(len(trip_info)*data_splits[i_split]) - entries_val                
    
    #Loop through weather, light, object density            
    for i_random in range(n_trips):
        add_to_list=False
        while not add_to_list:
          random_index = random.randint(0,len(n_trip_select)-1)
          trip_select_index = n_trip_select[random_index]                
          #All fair conditions must be true                             
          checks = [False]*len(n_cond)            
          for i_checks in sorted(n_cond):
             #Get the conditions of randomly selected trip
             temp_check = trip_info[trip_select_index][cond_fair[i_checks][0]]
             checks[i_checks] = True if temp_check == cond_fair[i_checks][1] else False

          #If all the conditions are true then add them in their respective array
          all_true_counter = sum(checks)
          if all_true_counter==3: #Matches all trip conditions
             add_to_list=True
             if i_split == "test":                   
                #Add trip to split
                n_list_test.append(trip_info[trip_select_index])
                #Remove Trip from main trip list
                n_trip_select.pop(random_index)
             else:                
                #Add trip to split
                n_list_val.append(trip_info[trip_select_index])
                #Remove Trip from main trip list
                n_trip_select.pop(random_index)

#All the left trips are transferred to training array
for i_select in range(len(n_trip_select)):
    trip_select_index = n_trip_select[i_select]
    n_list_train.append(trip_info[trip_select_index])    
                    
#print("Number of trips in test_per_cat")
#print(test_per_cat)
print("Number of trips in test split is = {}".format(len(n_list_test)))
#print(n_list_test)
print("\n")
#print("Number of trips in val_per_cat")
#print(val_per_cat)
print("Number of trips in validation split is = {}".format(len(n_list_val)))
#print(n_list_val)
print("\n")
print("Number of trips in training split is = {}".format(len(n_list_train)))
#print(n_list_train)

print("********* TEST *****************")
#Checking the number of occurences in test
counted = Counter([item for sublist in n_list_test for item in sublist])
n_density[1] = counted.get('high', 'not found!')
n_light[1] = counted.get('night', 'not found!')
n_weather[0] = counted.get('bad', 'not found!')
print("Object density info")
print("Number of trips with high object density = {}".format(n_density[1]))
print("Light conditions info")
print("Number of trips during night = {}".format(n_light[1]))
print("weather info")
print("Number of trips with bad weather  = {}".format(n_weather[0]))

print("********* VALIDATION *****************")
#Checking the number of occurences in test
counted = Counter([item for sublist in n_list_val for item in sublist])
n_density[1] = counted.get('high', 'not found!')
n_light[1] = counted.get('night', 'not found!')
n_weather[0] = counted.get('bad', 'not found!')
print("Object density info")
print("Number of trips with high object density = {}".format(n_density[1]))
print("Light conditions info")
print("Number of trips during night = {}".format(n_light[1]))
print("weather info")
print("Number of trips with bad weather  = {}".format(n_weather[0]))

print("********* TRAINING *****************")
#Checking the number of occurences in test
counted = Counter([item for sublist in n_list_train for item in sublist])
n_density[1] = counted.get('high', 'not found!')
n_light[1] = counted.get('night', 'not found!')
n_weather[0] = counted.get('bad', 'not found!')
print("Object density info")
print("Number of trips with high object density = {}".format(n_density[1]))
print("Light conditions info")
print("Number of trips during night = {}".format(n_light[1]))
print("weather info")
print("Number of trips with bad weather  = {}".format(n_weather[0]))

#write the trip splits to a file
def split_array(split_id):
    if split_id == 0:
        return_array = n_list_test
    if split_id == 1:
        return_array = n_list_val
    if split_id == 2:
        return_array = n_list_train
    return return_array
    
file_write={0:"test_split.txt",1:"validation_split.txt",2:"training_split.txt"}
for i_file in file_write:
    filename = file_write[i_file]
    f = open("%s" %filename,"w")    
    trip_data = [] #Clear array
    trip_data = split_array(i_file)
    f.write("#**Total number of trips %d**\n" %len(trip_data))
    f.write("#**trip number**\t**file_name**\n")
    trip_counter = 0
    for i_trip in trip_data:
        f.write("%d\t%s\n" %(trip_counter,i_trip[1]))
        trip_counter +=1
    f.close()
        
    
    