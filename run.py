from beta.HIRO import HIRO

params = [
    './dataset/data/Training.csv', # training_data
    './dataset/data/Testing.csv', # testing_data
    './dataset/main/Symptom_severity.csv', # serverity_data 
    './dataset/main/symptom_precaution.csv' ,# precaution_data
    './dataset/main/symptom_Description.csv' # description_dat
]

hiro = HIRO(params[0],
    params[1],
    params[2],
    params[3],
    params[4]
)
hiro.prepare()
hiro.introduce(patient_name=input('[patient name] :: '))
    
while True:
    user_problem = input('\n[can you explain your problem] :: ')
    result = hiro.get_user_problem(user_problem)
    # print(result)
    if result[0] == 1:
        print(f'\nsearches related to {result[1][0]} :')
        for item_number , item_name in enumerate(result[1]):
            print(f'{item_number} ) {item_name}')   
        if item_number !=0:
                confidence_input = hiro.get_choice(
                    input(f'select an option from 1 - {item_number} : '),
                   'please enter choice in digits (0-9)!'
                ) 
        else:
            confidence_input = 0
        disease_input = result[1]
        # print(disease_input)
    else:
        print('please enter a valid symptoms')      
    num_days = hiro.get_choice(
        input("\nOkay. From how many days ? : "),
        'please enter number of days in digits (0-9)!'
    )
    # print(num_days)
    # print(hiro.daignose_diseases(result[1]))
    given_symptoms = hiro.recurse(0,1,disease_input[0],result[2])
    # print(given_symptoms)
    print(
        '\nOkay Now I am going to ask you some question,please answer all of them in yes or no'
    )
    symptoms_exp = []
    for symps in given_symptoms:
        choice = input(
            f'\nAre you experiencing any {symps} ? \nEnter your answer in [yes or no] :: ')
        if choice == 'yes':
            symptoms_exp.append(symps)
    
    second_prediction = hiro.second_prediction(symptoms_exp)
    # print(second_prediction)
    patient_condition = hiro.calcCondition(symptoms_exp,num_days)
    # print(patient_condition)