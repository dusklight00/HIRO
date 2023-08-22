from beta.HIRO import HIRO

datasets = [
    './dataset/data/Training.csv', # training_data
    './dataset/data/Testing.csv', # testing_data
    './dataset/main/Symptom_severity.csv', # serverity_data 
    './dataset/main/symptom_precaution.csv' ,# precaution_data
    './dataset/main/symptom_Description.csv' # description_dat
]

hiro = HIRO(
    datasets[0],
    datasets[1],
    datasets[2],
    datasets[3],
    datasets[4]
)
hiro.prepare()

if __name__=='__main__':
    
    while True:
        patient_name = input('[patient name] :: ')
        hiro.introduce(patient_name)
        
        user_problem = input('\n[can you explain your problem] :: ')
        result = hiro.get_user_problem(user_problem)
        
        if result[0] == 1:
            print(f'\nsearches related to {result[1][0]} :')
            for item_number , item_name in enumerate(result[1]):
                print(f'{item_number} ) {item_name}')
                
            if item_number !=0:
                try:
                    confidence_input = int(input(f'select an option from 1 - {item_number} : '))
                except Exception:
                    print("\nplease enter a valid input for choice")
            else:
                confidence_input = 0 
                
            disease_input = result[1]
            break
        
        else:
            print('please enter a valid symptoms')
        
            