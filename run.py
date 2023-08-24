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
hiro.introduce(patient_name=input('[patient name] :: '))
    
while True:

    user_problem = input('\n[can you explain your problem] :: ')
    result = hiro.get_user_problem(user_problem)
    
    if result[0] == 1:
        print(f'\nsearches related to {result[1][0]} :')
        for item_number , item_name in enumerate(result[1]):
            print(f'{item_number} ) {item_name}')   

        if item_number !=0:
                confidence_input = hiro.get_choice(
                    input(f'select an option from 1 - {item_number} : '),
                   'please enter choice in digits (0-9)!') 

        else:
            confidence_input = 0
        disease_input = result[1]
    else:
        print('please enter a valid symptoms')     
    num_days = hiro.get_choice(input("\nOkay. From how many days ? : "),
                               'please enter number of days in digits (0-9)!')

    given_symptoms = hiro.recurse(0,1,disease_input[0],result[2])

    print(
        '\nOkay Now I am going to ask you some question , please answer all of them in yes or no \n'
        )
    symptoms_exp = []
    for symps in given_symptoms:
        choice = input(f'\nAre you experiencing any {symps} ? \n enter [yes or no] :: ')
        if choice == 'yes':
            symptoms_exp.append(symps)
    second_prediction = hiro.second_prediction(symptoms_exp)
    print(second_prediction)