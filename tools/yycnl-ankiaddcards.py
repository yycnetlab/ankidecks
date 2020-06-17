# YYC Net Labs - Anki Script
# Written by: Kelvin Tran - May 30th, 2020 (Prefix 933)
# DISCLAIMER: This script is being provided as-is with no guarantee of functionality, availability, or support of any kind.
# NOTE: For debugging, you can disable the bare exceptions (except: ...) - identified in the error message (Format: <method> Bare Exception <#>)
# NOTE: Be sure to modify the variables in the main method (at bottom of script) - instructions in comments in the main method.

import json, sys, argparse


def userInput():  # Collect user input if the importFromFile variable in main() is False
    moreCards = True  # Initialize a variable called "moreCards" and set it to true - used to determine continuation of while loop

    # Initialize arrays to hold the values user inputted for >=1 cards
    originalFront = []
    originalBack = []
    reverseFront = []
    reverseBack = []
    reference = []
    tags = []

    while moreCards:
        # Check that input is not empty (exit the program if condition is satisfied) - use assignment operator
        # (walrus) to assign the input to a variable
        # If not empty - append the established variable to the appropriate list, such that the index
        # is the same as the card index established in the WriteToFile() method

        if (var := input("Please enter the front value of the original card. ")) == "":
            print("Value required.")
            sys.exit()
        originalFront.append(var)

        if (var := input("Please enter the back value of the original card. ")) == "":
            print("Value required.")
            sys.exit()
        originalBack.append(var)

        if (var := input("Please enter the front value of the reversed card. ")) == "":
            print("Value required.")
            sys.exit()
        reverseFront.append(var)

        if (var := input("Please enter the back value of the reversed card. ")) == "":
            print("Value required.")
            sys.exit()
        reverseBack.append(var)

        if (var := input("Please enter your reference. ")) == "":
            print("Value required.")
            sys.exit()
        reference.append(var)

        # Establish temporary tags variable, such that the list can be appended to the tags list established above
        tempTags = []
        # Establish tags index for use with subscripting of list
        tagsIndex = 0

        # Condition to continue with while loop for adding more tags for the card's sublist
        moreTags = True
        while moreTags:
            # Append any tags to the tempTags list
            tempTags.append(input(
                "Please enter the tags that you want to use, one per line. Hit Enter when you've input a tag. When you're done inputting tags, hit Enter once while the line is blank to finalize. "))

            # Implement "enter on a blank line" functionality to exit while loop by setting boolean flag (moreTags) to False
            if tempTags[tagsIndex] == "":
                moreTags = False  # Set flag to break out of loop
                tempTags.remove(
                    '')  # Remove the blank line from the list such that it's not written to the variable/deck file
            elif tempTags[tagsIndex] != "":
                tagsIndex += 1  # Add one to the tag index to allow subscripts to continue operating normally and referencing the correct positions in the list

        tags.append(tempTags)  # Append tempTags list to main list

        # Conditional statement to break out of loop if the user does not type "y" to continue by setting boolean flag to False
        if (input("Type \"y\" to continue. Type nothing and press enter to stop. ")).lower() != "y":
            moreCards = False

    # Return list of all lists as sub-lists of that list for easy reference in later methods
    return [originalFront, originalBack, reverseFront, reverseBack, reference, tags]


def loadInputFile(filename):  # Load input JSON file and parse it as JSON, storing it in variable that is then returned
    try:
        # Open note template file and parse as JSON
        template = json.load(file := open(filename, "r"))

        # Initialize arrays to store data from JSON file
        originalFront = []
        originalBack = []
        reverseFront = []
        reverseBack = []
        reference = []
        tags = []

        for number, note in enumerate(notes := template["notes"]):
            # Append to the arrays initialized above the data from the JSON file with an index in the list matching the index of the card in the file.
            # Exit the program if any of the inputted values are empty.
            if (appendData := notes[number]["front"]) == "":
                print("Value required for front.")
                sys.exit()
            originalFront.append(appendData)

            if (appendData := notes[number]["back"]) == "":
                print("Value required for back.")
                sys.exit()
            originalBack.append(appendData)

            if (appendData := notes[number]["front_reverse"]) == "":
                print("Value required for front_reverse.")
                sys.exit()
            reverseFront.append(appendData)

            if (appendData := notes[number]["back_reverse"]) == "":
                print("Value required for back_reverse.")
                sys.exit()
            reverseBack.append(appendData)

            if (appendData := notes[number]["reference"]) == "":
                print("Value required for reference.")
                sys.exit()
            reference.append(appendData)

            tags.append(appendData := notes[number][
                "tags"])  # Use assignment operator to append the tags array in the JSON file as a list to tags

        # Return an array consisting of sub-arrays from the arrays populated above.
        return [originalFront, originalBack, reverseFront, reverseBack, reference, tags]

    # Handle a decoding error exception - invalid JSON, cannot be parsed
    except json.JSONDecodeError:
        print("Invalid JSON in input file.")
    # Handle an exception if the file is not found
    except FileNotFoundError:
        print("Input file not found. Please try again with another file.")
    # Handle exception if the key is not found in the JSON file.
    except KeyError as e:
        print("The following JSON key wasn't found: ", e)
    # Handle any unexpected errors in an exception by exporting a "pretty-fied" error with the error code present. (loadInputFile, Bare Exception 1)
    except:
        print("loadInputFile Bare Exception 1: Unknown error: ", sys.exc_info()[0])

    # Exit the program if the program has to handle an exception
    sys.exit()


def loadOutputFile(file):
    try:
        outputJSON = json.load(open(file, "r"))  # Open file and parse as JSON
        return outputJSON
    except json.JSONDecodeError:  # Handle invalid JSON exception
        print("Invalid JSON in output file.")
    except FileNotFoundError:  # Handle exception if file isn't found
        print("Output file not found. Please try again with another file.")
    except:  # Handle all other exceptions (include error info) (loadOutputFile Bare Exception 1:)
        print("loadOutputFile Bare Exception 1: Unknown error: ", sys.exc_info()[0])

    sys.exit()  # Exit the program if the try block fails to return a value (if an exception is handled)


def FindNMUUID(json):  # Find Note Model UUID in output JSON file
    try:
        uuid = json["note_models"][0]["crowdanki_uuid"]  # Search note models object for uuid to include on all notes
        return uuid
    except json.JSONDecodeError:  # Handle exceptions for JSON errors
        print("Invalid JSON in output file.")
    except KeyError as e:  # Handle error if JSON object can't be found
        print("The following JSON key wasn't found: ", e)
    except:  # Bare exception to catch all other errors (FindNMUUID Bare Exception 1)
        print("FindNMUUID Bare Exception 1: Unknown error: ", sys.exc_info()[0])

    sys.exit()  # Exit program if exception was handled


def GenerateUniqueGUID(json, prefix, num):  # Generate unique GUID for the card based on the GUID of the previous card
    index = 0  # Use as index for subscripting - incremented every iteration of the for loop
    foundPrefix = False  # Mark as true if GUID with prefix is found (if user with prefix has contributed a card), if False - create first GUID, if True - increment last GUID
    highestWithPrefix = 0  # Use as integer to store highest GUID with the prefix
    try:
        for iterations, value in enumerate(notes := json[
                "notes"]):  # For loop that enumerates list notes (json["notes"]), separate iterations from value (variables may be used in the future)
            if notes[index]["guid"][0:3] == str(prefix):
                foundPrefix = True  # If the first three characters of the GUID match the prefix argument, mark the boolean Flag foundPrefix True
                if (candidate := int(notes[index][
                                         "guid"])) > highestWithPrefix:  # if the candidate GUID is higher than the current highest, replace the highest
                    highestWithPrefix = candidate
            index += 1  # Increment index to maintain accurate subscripting
    except KeyError as e:  # Handle exception if notes doesn't exist in the file
        print("The following JSON key wasn't found: ", e)
        sys.exit()
    except:  # Bare except to catch other issues (GenerateUniqueGUID Bare Exception 1)
        print("GenerateUniqueGUID Bare Exception 1: Unexpected error: ", sys.exc_info()[0])
        sys.exit()

    # Establish cardIndex variable as integer
    cardIndex = 0

    # Initialize forwardGUID and reverseGUID variables as lists to contain GUIDs - index matches with cardIndex in the WriteToFile() module
    forwardGUID = []
    reverseGUID = []

    lastGUID = highestWithPrefix  # Assign highestWithPrefix value to lastGUID

    while cardIndex < num:  # Incremented, while loop continues as long as this variable stays below the number of items - not >=, since len is 1 more than the index of the last item in the list
        if not foundPrefix:
            forwardGUID.append(
                str(prefix) + "0900001")  # If GUID with prefix doesn't exist, create the first one for forwards card
            reverseGUID.append(int(forwardGUID[cardIndex]) + 1)  # Reverse card is forwardsGUID + 1
        elif foundPrefix:
            try:
                forwardGUID.append(int(
                    lastGUID) + 1)  # If GUID with prefix can be found, take the highest GUID and add 1 for forwards GUID
                reverseGUID.append(
                    forwardGUID[cardIndex] + 1)  # Add one to the forwardsGUID for the reverseGUID - create GUID pair
            except ValueError:  # Handle exception if GUID cannot be converted to integer - invalid GUID value in the JSON data
                print("Invalid value for GUID. Failure to convert to integer. ERROR: ValueError")
                sys.exit()
            except:  # Bare exception to catch other issues (GenerateUniqueGUID Bare Exception 2)
                print("GenerateUniqueGUID Bare Exception 2: Unexpected error: ", sys.exc_info()[0])
                sys.exit()
        lastGUID = reverseGUID[
            cardIndex]  # Account for multiple cards - change lastGUID to be the new highest (reverseGUID)
        cardIndex += 1  # Increment cardIndex - must be last action so as to not interfere with other subscript actions - align with item index in lists

    return [forwardGUID, reverseGUID]  # Return a list of forwardGUID and reverseGUID as sub-lists


def WriteToFile(jsondata, file, elementtype, data, fields, flags, guid, nmuuid,
                numcards):  # Based on various arguments, write to deck file
    # Create new variable "backup" consisting of jsonData's contents in case of failure
    backup = jsondata

    # Create backup file with the original file name of the deck + ".backup.json" and dump a pretty version of the original JSON data - truncate file if it already exists and overwrite
    with open((backupName := file + ".backup.json"), "w") as backupFile:
        json.dump(backup, backupFile, indent=2)

    index = 0  # Use as counter in while loop below

    while index < (
            numcards):  # Increment index - while index is below the number of cards as provided in method argument, append data
        # FORWARD CARD - append first using all values as provided in arguments - as dictionary to represent JSON object fields[0] and fields[1] are front and back
        # For forward and reverse cards - fields[4] - reference, flags[5] - tags / guid[0] - forward GUID, guid[1] - reverse GUID (third item in fields list refers to the OTHER card's GUID)
        jsondata["notes"].append(writeDataForward := {'__type__': elementtype, 'data': data,
                                                      'fields': [fields[0][index], fields[1][index],
                                                                 str(guid[1][index]), fields[4][index]], 'flags': flags,
                                                      'guid': str(guid[0][index]), 'note_model_uuid': nmuuid,
                                                      'tags': fields[5][index]})
        # REVERSE CARD - append second using all values as provided in arguments - as dictionary to represent JSON object - fields[2] and fields[3] are front_reverse and back_reverse
        jsondata["notes"].append(writeDataReverse := {'__type__': elementtype, 'data': data,
                                                      'fields': [fields[2][index], fields[3][index],
                                                                 str(guid[0][index]), fields[4][index]], 'flags': flags,
                                                      'guid': str(guid[1][index]), 'note_model_uuid': nmuuid,
                                                      'tags': fields[5][index]})
        index += 1

    with open(file, "w") as stream:  # Open file in writing mode (truncate file if it exists)
        json.dump(jsondata, stream,
                  indent=2)  # Dump the new jsonData (with new cards appended) with an indent value of 2 to align with original indent design - pretty output
        print("JSON data has been successfully exported to the file " + str(
            file) + ". A backup file has been created in the same folder with the name of " + str(
            backupName) + " to protect against program failures.")  # Confirmation message


def main(args):
    prefix = None  # Replace the prefix with your own prefix as an integer (default: None)

    # Conditional statement to quit program if prefix is not set correctly
    if prefix is None:
        print("Prefix cannot be none. Please set the prefix to a valid integer.")
        sys.exit()

    deckJSON = None  # Replace the file name with the FULL file name (including file extensions) of the deck JSON file. Absolute or relative paths allowed. (default: None)

    if deckJSON is None:
        print("deckJSON cannot be none. Please set the deckJSON variable to the file name of the deck JSON file.")
        sys.exit()  # Exit the program if deckJSON is set to the default value of None

    SetFlags = False  # If there are flags, set the variable True: (default: False)

    CustomFlags = 0  # If there are flags, enter them in the variable (default: 0)

    data = ""  # If there is any data for the data field, please enter it between the quotes. (default: "", blank string)

    type = "Note"  # If there is a custom type, please change the value of the variable below. (Default: Note)

    importFromFile = False  # If you are importing from a JSON file, mark the following field True (default: False, interactive mode)
    # for debug purposes ONLY, set to "debug" as string to bypass the conditional statement block.

    if importFromFile:  # Users of interactive mode don't need to provide arguments; only initialize argparse if the user has set the flag for importFromFile to True
        parser = argparse.ArgumentParser()  # Initialize argparse argument parser
        parser.add_argument("-f", help="Input JSON file")  # Add -f argument to allow user to provide file
        args = parser.parse_args()  # Parse user arguments into args variable for later reference

    if importFromFile:
        if args.f is not None:
            importJSON = args.f  # Note that if the JSON file is provided with the -f flag, it will take precedence over manual definition.
        else:
            importJSON = ""  # Replace the file name with the file name of the imported JSON file. Absolute or relative paths work. (Default: none)

        values = loadInputFile(importJSON)  # Call function to parse the value of the importJSON file as JSON

    elif not importFromFile:
        values = userInput()  # Call userInput function to collect user input
    elif importFromFile.lower() == "debug":  # Don't collect user input or collect from file if debug is enabled.
        pass
    else:
        print("Invalid keyword for importFromFile variable. It should be a boolean True/False.")
        sys.exit()  # Exit program if importFromFile variable set incorrectly.

    # Parse JSON in output file
    outputJSON = loadOutputFile(deckJSON)

    # Find the Note Model UUID to add onto all notes by calling a function to search the deck JSON file for it
    uuid = FindNMUUID(outputJSON)

    # Check for number of cards
    numCards = len(values[0])

    # Generate Unique GUID
    guids = GenerateUniqueGUID(outputJSON, prefix, numCards)

    # Call function to write all gathered data to deck file
    WriteToFile(outputJSON, deckJSON, type, data, values, CustomFlags, guids, uuid, numCards)


def ExecuteMain():
    # Execute the main method if the script is not being imported as an external module
    if __name__ == "__main__":
        main(None)


# Call method to execute main method on condition that the script is NOT being imported
ExecuteMain()
