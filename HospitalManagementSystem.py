'''
This is a program on the project "Hospital Management System"
where the user can:
	1. Add a new patient record
	2. Search or edit patient record
	3. Know the list of patient records
	4. Delete patient records
'''

import time  # For sleep function
import os   # To clear the screen
import re   # To check for patterns
import pyinputplus as pyip  # To validate the input
import pprint
import PatientRecords   # To access contents of the file


def headTitle():    # For the title in every function
    os.system('cls')  # Clearing the screen
    print('\n\n\t\t\t\t    ALKA HOSPITAL\n')
    print('\t\t\t\tJawalakhel, Lalitpur')
    print('\t\t\t\t--------------------')


def mainMenu():  # The main menu function
    headTitle()
    # Asking user for date
    date = input("\n\n\n\n\t\t\t    Enter today's Date(dd/mm/yyyy): ")
    # Declaring the regex pattern
    dateRegexPattern = re.compile('(\d\d)\/(\d\d)\/(\d\d\d\d)')
    # Searching the input for the regex
    dateRegex = dateRegexPattern.search(date)
    # Checking whether date matches the format
    try:
        if date != dateRegex.group(0) or int(dateRegex.group(1)) > 31 or int(dateRegex.group(2)) > 12:
            print('\n\t\t\t    Invalid Input!, Type Again.')
            time.sleep(2)     # Displaying the message for 2 seconds
            os.system('cls')  # Clearing the screen
            mainMenu()
        elif date == dateRegex.group():
            optionMenu()
    except:
        print('\n\t\t\t    Invalid Input!, Type Again.')
        time.sleep(2)     # Displaying the message for 2 seconds
        os.system('cls')  # Clearing the screen
        mainMenu()


def specialistMenu():   # Menu for the list of specialists
    print('\n\t\t\t\t\t\tSpecialists\t\tRoom No.')
    print('\t\t\t\t\t\t-----------\t\t--------')
    print('\n\t\t\t\t\t\t1. General Physician    201, 202')
    print('\t\t\t\t\t\t2. E.N.T\t\t302')
    print('\t\t\t\t\t\t3. Cardiologist\t\t509')
    print('\t\t\t\t\t\t4. Dermatologist\t406')
    print('\t\t\t\t\t\t5. Gastroenterologist\t308')
    print('\t\t\t\t\t\t6. Pediatrician\t\t207')
    print('\t\t\t\t\t\t7. Eye Specialist\t102')
    print('\t\t\t\t\t\t8. Nephrologist\t\t109')
    print('\t\t\t\t\t\t9. General Surgeon\t407, 408')
    print('\t\t\t\t\t\t10. Acupuncturist\t412, 413')


def addContinue():  # To ask user to continue or quit
    # Displaying the end menu
    endChoice = pyip.inputStr(
        '\n\n\t\tEnter (c) to continue or (q) to quit to main menu. ', allowRegexes=[r'[(^c$)|(^q$)]'])
    # Jumping to respective functions
    if endChoice == 'c':
        add_Patient()
    elif endChoice == 'q':
        optionMenu()
    else:
        print('\n\t\t\t\tInvalid number, Type again!')
        time.sleep(2)
        addContinue()


def add_Patient():  # Menu for adding patient record
    # Opening the file
    recordFile = open('PatientRecords.py', 'r+')
    specialistMenu()
    # Reading the contents of the file for Regex
    fileContent = str(recordFile.readlines())
    # Searching the file for matches
    fileRegex = re.findall(pattern='patient[1-9]0? ', string=fileContent)
    # Assigning the patient number
    for i in range(1, 11):
        if 'patient'+str(i)+' ' in fileRegex:
            continue
        else:
            patientNumber = i
        break
    print('Record Patient no: ', patientNumber)
    # Asking the user for input
    patientName = pyip.inputStr('\nName: ', blockRegexes=[r'[^a-zA-Z]'])
    patientAddress = pyip.inputStr('\nAddress: ')
    patientAge = pyip.inputInt('\nAge: ')
    patientSex = pyip.inputStr('\nSex(m/f): ', blockRegexes=[r'[^mf]'])
    patientDisease = input('\nDisease Description(in short): ')
    patientSpecialist = pyip.inputInt('\nReferred Specialist room no. ')
    # Storing the input in a dictionary
    recordDictionary = {'Patient no.': patientNumber,
                        'Name': patientName,
                        'Address': patientAddress,
                        'Age': patientAge,
                        'Sex': patientSex,
                        'Disease Description': patientDisease,
                        'Referred Specialist room no.': patientSpecialist}
    # Writing to the file
    for i in range(1, 11):
        recordFile.write('patient'+str(patientNumber)+' = ' +
                         pprint.pformat(recordDictionary)+'\n')
        break
    print('\n\t\t\t    Added the record successfully!')
    addContinue()
    # Closing the record file
    recordFile.close()


def addRecord():    # Menu for options to add records
    headTitle()
    print('\n\n\n\n\t\t\t    Select one of the following:\n')
    # Displaying the options for new record
    print('\t\t\t    1. O.P.D service')
    print('\t\t\t    2. Emergency service')
    print('\t\t\t    3. Return to main menu.\n')
    # Taking in the choice out of these two
    newPatientChoice = pyip.inputInt('\t\t\t    ')
    # Checking the choice
    if newPatientChoice == 1:
        headTitle()
        print('\n\n\t\t\t    ADDING NEW O.P.D PATIENT RECORD')
        print('\t\t\t    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        add_Patient()
    elif newPatientChoice == 2:
        headTitle()
        print('\n\n\t\t\tADDING NEW EMERGENCY PATIENT RECORD')
        print('\t\t\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        add_Patient()
    elif newPatientChoice == 3:
        optionMenu()
    else:
        print('\t\t\t    Invalid Input!, Try again!')
        time.sleep(2)   # Displaying the message for 2 seconds
        addRecord()


def searchContinue():   # To ask user to continue or quit
    # Displaying the end menu
    endChoice = pyip.inputStr(
        '\n\n\t\tEnter (c) to continue or (q) to quit to main menu. ', allowRegexes=[r'[(^c$)|(^q$)]'])
    # Jumping to respective functions
    if endChoice == 'c':
        searcheditRecord()
    elif endChoice == 'q':
        optionMenu()
    else:
        print('\n\t\t\t\tInvalid number, Type again!')
        time.sleep(2)
        searchContinue()


def search_Patient():   # To search records
    headTitle()
    print('\n\n\t\t\t      SEARCHING PATIENT RECORD')
    print('\t\t\t      ~~~~~~~~~~~~~~~~~~~~~~~~')
    # Opening the file
    recordFile = open('PatientRecords.py', 'r+')
    # Reading the contents of the file for Regex
    fileContent = str(recordFile.readlines())
    # Taking in the patient number
    patientNum = pyip.inputInt(
        '\n\n\n\t\t\tEnter the patient no. to search: ', max=10)
    # Searching the file for matches
    fileRegex = re.findall(pattern='patient[1-9]0? ', string=fileContent)
    try:
        # Displaying the patient records
        if 'patient'+str(patientNum)+' ' in fileRegex:
            PatientRecords.display_Record(patientNum)
        else:
            print('\n\t\t\t\tInvalid number, Type again!')
            time.sleep(2)
            search_Patient()
    except:
        print('\n\t\t\t\tInvalid number, Type again!')
        time.sleep(2)
        search_Patient()
    # Closing the file
    recordFile.close()
    searchContinue()


def editContinue():  # To ask user to continue or quit
    # Displaying the end menu
    endChoice = pyip.inputStr(
        '\n\n\t\tEnter (c) to continue or (q) to quit to main menu. ', allowRegexes=[r'[(^c$)|(^q$)]'])
    # Jumping to respective functions
    if endChoice == 'c':
        searcheditRecord()
    elif endChoice == 'q':
        optionMenu()
    else:
        print('\n\t\t\t\tInvalid number, Type again!')
        time.sleep(2)
        editContinue()


def editMenu(num):
    headTitle()
    print('\n\n\t\t\t\tEDITING PATIENT RECORD')
    print('\t\t\t\t~~~~~~~~~~~~~~~~~~~~~~')
    # Displaying the menu
    print('\n\n\n\t\t\t    Choose one from the following:\n')
    print('\t\t\t    1. Edit Name')
    print('\t\t\t    2. Edit Address')
    print('\t\t\t    3. Edit Age')
    print('\t\t\t    4. Edit Sex')
    print('\t\t\t    5. Edit Disease Description')
    print('\t\t\t    6. Edit Referred Specialist\n')
    # Taking the input
    editChoice = pyip.inputInt('\t\t\t    ', greaterThan=0, lessThan=7)
    # Editing the record
    if editChoice == 1:
        change = pyip.inputStr(
            '\n\t\t\t    Enter the new Name: ', blockRegexes=[r'[^a-zA-Z]'])
        PatientRecords.edit_Record(num, editChoice, change)
    elif editChoice == 2:
        change = pyip.inputStr(
            '\n\t\t\t    Enter the new Address: ')
        PatientRecords.edit_Record(num, editChoice, change)
    elif editChoice == 3:
        change = pyip.inputInt(
            '\n\t\t\t    Enter the new Age: ')
        PatientRecords.edit_Record(num, editChoice, change)
    elif editChoice == 4:
        change = pyip.inputStr(
            '\n\t\t\t    Enter the new Sex: ', blockRegexes=[r'[^mf]'])
        PatientRecords.edit_Record(num, editChoice, change)
    elif editChoice == 5:
        change = pyip.inputStr(
            '\n\t\t\t    Enter the new Disease Description: ')
        PatientRecords.edit_Record(num, editChoice, change)
    elif editChoice == 6:
        change = pyip.inputInt(
            '\n\t\t\t    Enter the new Referred Specialist: ')
        PatientRecords.edit_Record(num, editChoice, change)


def edit_Patient():  # To edit records
    headTitle()
    print('\n\n\t\t\t\tEDITING PATIENT RECORD')
    print('\t\t\t\t~~~~~~~~~~~~~~~~~~~~~~')
    # Opening the file
    recordFile = open('PatientRecords.py', 'r+')
    # Reading the contents of the file for Regex
    fileContent = str(recordFile.readlines())
    # Searching the file for matches
    fileRegex = re.findall(pattern='patient[1-9]0? ', string=fileContent)
    # Taking in the patient number
    patientNum = pyip.inputInt(
        '\n\n\n\t\t\tEnter the patient no. to edit: ', max=10)
    # Editing the record
    if 'patient'+str(patientNum)+' ' in fileRegex:
        editMenu(patientNum)
        print('\n\t\t\t    Record successfully edited!')
        editContinue()
    elif 'patient'+str(patientNum) not in fileRegex:
        print('\n\t\t\t    Invalid number, Type again!')
        time.sleep(1)
        edit_Patient()
    # Closing the file
    recordFile.close()


def searcheditRecord():  # Menu for options to search or edit records
    headTitle()
    print('\n\n\n\n\t\t\t    Select one of the following:\n')
    # Displaying the options for searching or editing
    print('\t\t\t    1. Search the records')
    print('\t\t\t    2. Edit the records')
    print('\t\t\t    3. Return to main menu.\n')
    # Taking the input for choice
    seChoice = pyip.inputInt('\t\t\t    ')
    if seChoice == 1:
        search_Patient()
    elif seChoice == 2:
        edit_Patient()
    elif seChoice == 3:
        optionMenu()
    else:
        print('\n\t\t\t\tInvalid number, Type again!')
        time.sleep(2)
        searcheditRecord()


def displayContinue():  # To ask user to continue or quit
    # Displaying the end menu
    endChoice = pyip.inputStr(
        '\n\n\t\tEnter (c) to continue or (q) to quit to main menu. ', allowRegexes=[r'[(^c$)|(^q$)]'])
    # Jumping to respective functions
    if endChoice == 'c':
        displayRecord()
    elif endChoice == 'q':
        optionMenu()
    else:
        print('\n\t\t\t\tInvalid number, Type again!')
        time.sleep(2)
        displayContinue()


def displayRecord():    # To display all the records
    headTitle()
    # Opening the file
    recordFile = open('PatientRecords.py', 'r+')
    # Reading the contents of the file for Regex
    fileContent = str(recordFile.readlines())
    # Searching the file for matches
    fileRegex = re.findall(pattern='patient', string=fileContent)
    # Displaying the records
    if 'patient' not in fileRegex:
        print('\n\n\t\t\t\tNo records available!')
    else:
        PatientRecords.display_All()
    # Closing the file
    recordFile.close()
    displayContinue()


def deleteContinue():   # To ask user to continue or quit
    # Displaying the end menu
    endChoice = pyip.inputStr(
        '\n\n\t\tEnter (c) to continue or (q) to quit to main menu. ', allowRegexes=[r'[(^c$)|(^q$)]'])
    # Jumping to respective functions
    if endChoice == 'c':
        deleteRecord()
    elif endChoice == 'q':
        optionMenu()
    else:
        print('\n\t\t\t\tInvalid number, Type again!')
        time.sleep(2)
        deleteContinue()


def delete_Patient():  # Menu for deleting a single record
    headTitle()
    # Opening the file
    recordFile = open('PatientRecords.py', 'r+')
    # Reading the contents of the file for Regex
    fileContent = str(recordFile.readlines())
    # Searching the file for matches
    fileRegex = re.findall(pattern='patient[1-9]\d?0?', string=fileContent)
    print('\n\n\t\t\t      DELETING A PATIENT RECORD')
    print('\t\t\t      ~~~~~~~~~~~~~~~~~~~~~~~~~')
    # Taking in the choice
    patientNum = pyip.inputInt(
        '\n\n\t\t\tEnter the patient number to delete: ', max=100)
    if 'patient'+str(patientNum) in fileRegex:
        PatientRecords.delete_Record(patientNum)
        print('\n\t\t\t     Record successfully deleted!')
        deleteContinue()
    else:
        print('\n\t\t\t\tInvalid number, Type again!')
        time.sleep(2)
        delete_Patient()
    # Closing the file
    recordFile.close()


def deleteRecord():  # Menu for options to delete records
    headTitle()
    print('\n\n\n\n\t\t\t    Select one of the following:\n')
    # Displaying the options for deleting records
    print('\t\t\t    1. Delete a single record')
    print('\t\t\t    2. Delete all the records')
    print('\t\t\t    3. Return to main menu\n')
    # Taking in the input
    deletionChoice = pyip.inputInt('\t\t\t    ')
    # Opening the file
    recordFile = open('PatientRecords.py', 'r+')
    # Reading the contents of the file for Regex
    fileContent = str(recordFile.readlines())
    # Searching the file for matches
    fileRegex = re.findall(pattern='patient[1-9]0? ', string=fileContent)
    # Deleting the key
    if deletionChoice == 1:
        delete_Patient()
    elif deletionChoice == 2:
        PatientRecords.delete_Record()
        print('\n\n\t\t\tDeleted all the records successfully!')
        deleteContinue()
    elif deletionChoice == 3:
        optionMenu()
    else:
        print('\n\t\t\t\tInvalid number, Type again!')
        time.sleep(2)
        deleteRecord()
    # Closing the file
    recordFile.close()


def optionMenu():  # The options in the main menu
    headTitle()
    print('\n\n\n\n\t\t\t    Enter the corresponding no.\n')
    # Displaying the choices
    print('\t\t\t    1. Add new Patient record')
    print('\t\t\t    2. Search or edit record')
    print("\t\t\t    3. Know the Patient's record")
    print('\t\t\t    4. Delete the record')
    print('\t\t\t    5. Exit from the program\n')
    # Taking in the choice from user
    optionChoice = pyip.inputInt('\t\t\t    ')
    # Checking the optionChoice
    if optionChoice == 1:
        addRecord()
    elif optionChoice == 2:
        searcheditRecord()
    elif optionChoice == 3:
        displayRecord()
    elif optionChoice == 4:
        deleteRecord()
    elif optionChoice == 5:
        os.system('cls')    # Clearing the screen
        os.system('exit')   # Existing the program
    else:
        print('\t\t\t    Invalid Input!, Try again!')
        time.sleep(2)   # Displaying the message for 2 seconds
        optionMenu()


# Start of program
optionMenu()
