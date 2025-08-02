#23905993.py
#STUDENT ID :23905993
#AUTHOR(name): PUNIT NITIN PATIL


#The program to find the t test calculation , minoskwi distance for the specific country
#The program also find the absolute profit change and assign rank based on the number of employees and the absolute profit change
def main(csvfile):
    
    country_data,category_data = file_reader(csvfile)
    
    t_results = t_calculator(country_data)
    mino_dist=minoskwi_distance(country_data)
    
    t_mino=t_mino_dis_calcultor(t_results , mino_dist)
    
    category_data=percentage(category_data)
    category_data=rank_add(category_data)
    
    result_dict=numemplo_profit_rank(category_data)
    
    return t_mino,result_dict

def file_reader(csvfile):
    # Initializing the  empty dictionaries to store data and check the unique Organisations ID 
    country_data = {}
    category_data = {}
    unique_ids = set()

    try:
        # Opening the CSV file for reading
        with open(csvfile, 'r') as file:
            # Reading the header line and split it into a list of column names
            header = file.readline().strip().split(',')

            # Iterate over each line in the CSV file
            for line in file:
                values = line.strip().split(',')
                row = {}

                # Creating a dictionary for the current row by pairing the column names with values
                for i in range(len(header)):
                    value = values[i].strip()
                    if value == '':
                        value = None
                    row[header[i].strip()] = value

                # Extract country data and categoy for making them the key in a dictionary from the row
                country = row.get('country')
                category = row.get('category')
                org_id = row.get('organisation id')

                # Checking if there are any duplicate organisation id 
                if org_id not in unique_ids:
                    unique_ids.add(org_id)

                    # making the dictionary with key as country
                    if country:
                        country = country.lower()
                        if country in country_data:
                            country_data[country].append(row)
                        else:
                            country_data[country] = [row]

                    # making the dictionary with key as category
                    if category:
                        category = category.lower()
                        if category in category_data:
                            category_data[category].append(row)
                        else:
                            category_data[category] = [row]

        # Returning the dictionaries which contain country as key and category as key in other dictionary
        return country_data, category_data
    except IOError:
        #Handing exception if the file is not in the particular directory
        print(f"The file you are trying to access is not in the file directory")
        return {}, {}
  


def t_calculator(country_data):
    # Initializing an empty dictionary for storing the result of t_test
    t_test_results = {}

    try:
        # Iterate over each country and the  data in contains
        for country, rows in country_data.items():
            profits_2020 = []
            profits_2021 = []

            # Extracting median salary, and number of employees data from rows
            for entry in rows:
                median_salary = entry.get('median Salary')
                num_employees = entry.get('number of employees')

                # Checking  if the median salary and number of employees are greater than 0 and not negative 
                if median_salary is not None and num_employees is not None and float(median_salary) > 0 and int(num_employees) > 0:
                    profit2020 = int(entry.get('profits in 2020(million)'))
                    profit2021 = int(entry.get('profits in 2021(million)'))
                    profits_2020.append(profit2020)
                    profits_2021.append(profit2021)

            
            if len(profits_2020) > 1 and len(profits_2021) > 1:
                # Calculate means and sample sizes
                mean_2020 = sum(profits_2020) / len(profits_2020)
                mean_2021 = sum(profits_2021) / len(profits_2021)
                n1 = len(profits_2020)
                n2 = len(profits_2021)

                # Calculating sample standard deviations
                std_dev_2020 = 0
                std_dev_2021 = 0

                for profit in profits_2020:
                    std_dev_2020 += (profit - mean_2020) ** 2

                for profit in profits_2021:
                    std_dev_2021 += (profit - mean_2021) ** 2

                std_dev_2020 = (std_dev_2020 / (n1 - 1)) ** 0.5
                std_dev_2021 = (std_dev_2021 / (n2 - 1)) ** 0.5

                # Calculating the t_test
                denominator = ((std_dev_2020 ** 2) / n1 + (std_dev_2021 ** 2) / n2) ** 0.5
                t_statistic = (mean_2020 - mean_2021) / denominator

                # Storing the t_test
                t_test_results[country] = round(t_statistic, 4)

        # Returning the t_test results
        return t_test_results
    except :
       
        print(f"The file might contain some invalid data")
        return {}
 
# Function that calcultes minoskwi distance
def minoskwi_distance(country_data):
    mino_dist = {}

    try:
        for country, rows in country_data.items():
            total = 0
            for entry in rows:
                mediasal = int(entry['median Salary'])
                noempl = int(entry['number of employees'])
                total += abs(mediasal - noempl) ** 3

            mino_dist[country] = round(total ** (1/3), 4)

        return mino_dist
    except:
        
        print(f"The file might contain some invalid data")
        return {}

# Function which combines the t_test and minoswki distance into a single dicitonary
def t_mino_dis_calcultor(t_test_results, mino_dist):
    t_mino = {}

    try:
        for key, value in t_test_results.items():
            if key in mino_dist:
                t_mino[key] = [value, mino_dist[key]]
            else:
                t_mino[key] = value

        for key, value in mino_dist.items():
            if key in t_test_results:
                if key not in t_mino:
                    t_mino[key] = value

        return t_mino
    except:
        
        print(f"The file might contain some invalid data")
        return {}
 
 
#Function which adds absolute percentage into the every small dicitonary in the category data dictionary
def percentage(category_data):
    try:
        for key, value in category_data.items():
            for trigger in value:
                if 'profits in 2020(million)' in trigger and 'profits in 2021(million)' in trigger:
                    profit2020 = int(trigger.get('profits in 2020(million)', 0))
                    profit2021 = int(trigger.get('profits in 2021(million)', 0))
                    absolute = abs(profit2020 - profit2021)

                    if profit2020 != 0:
                        percent = (absolute / profit2020) * 100
                        percent = round(percent, 4)
                        trigger['percentage data'] = percent

        return category_data
    except :
        
        print(f"The file might contain some invalid data ")
        return category_data


# Function which adds rank based on percentage and the number of employees
def rank_add(category_data):
    try:
        for category, data_list in category_data.items():
            sorted_data = sorted(data_list, key=lambda x: (-int(x.get('number of employees', 0)), -int(x.get('percentage data', 0))))

            rank = 1
            for entry in sorted_data:
                entry['rank'] = rank
                rank += 1

            category_data[category] = sorted_data

        return category_data
    except:
        
        print(f"The file might contain some invalid data")
        return category_data
 

# Function which brings the number of employees , profit percentage and rank into a single dictionary
def numemplo_profit_rank(category_data):
    result_dict = {}

    try:
        for category, data_list in category_data.items():
            cat_dict = {}

            for entry in data_list:
                ID = entry.get('organisation id')
                num_employees = int(entry.get('number of employees', 0))
                prof_percent = entry.get('percentage data', 0)
                rank = int(entry.get('rank', 0))

                # Creating a list with relevant data and storing it in a dictionary with the organization ID as the key
                data_list = [num_employees, prof_percent, rank]
                cat_dict[ID] = data_list

            # Storing the category-specific dictionary in the result dictionary
            result_dict[category] = cat_dict

        return result_dict
    except:
        
        print(f"The file might contain some invalid data")
        return result_dict
 






          










            












    
    



            

        
    
        

        
    


        
        
        
    

    











