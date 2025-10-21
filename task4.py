#error handling decorator and cmd parsing for assistant bot
def input_error(func):
    """
    Decorator to handle KeyError, ValueError,IndexError exceptions
    in command functions, returning specific error messages to the user.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            if str(e) == "Name cannot be purely numeric.": #when name input in all digits
                return "[ValueError] Name cannot be purely numeric. Make sure to enter a valid name first."
            
            return "[ValueError] Give me name and phone please, or name and new phone number." #when invalid value
        except IndexError:
            return "[IndexError] Enter user name, or give me name and new phone number please." #when missing args
        except KeyError:
            return "[KeyError] Contact not found." #when contact is not in dict
        except Exception as e:
            return f"[Exception] An unexpected error occurred: {e}" #other unexpected errors

    return inner

def parse_input(user_input):
    """
    Parses input string into a command and its arguments.
    Converts command to lowercase, whitespace is removed.
    """
    parts = user_input.split()
    if not parts:
        return "", [] #no command, no arguments

   #1st word - command,others - arguments
    cmd, *args = parts
    cmd = cmd.strip().lower()
    return cmd, args

# Cmd handlers with error decorator
@input_error
def add_contact(args, contacts):
    """
    adds new contact to contacts dict. expects name (1st) and phone (2nd) in args.
    """
    if len(args) < 2:
        raise IndexError #not enough args    
    name, phone = args

    if name.isdigit():
        raise ValueError("Name cannot be purely numeric.") #additional value error check from me (noticed while testing)    
    
    if len(args) != 2: #expecting name and phone (2 args)
        raise IndexError 

    contacts[name.lower()] = phone #add/update contact, converts to lowercase
    return "Contact added."

@input_error
def change_contact(args, contacts):
    """
    Changes the phone number for the specified and existing contact.
    Expects [name, new_phone].
    """
    name, new_phone = args
    name_key = name.lower() #add or update contact, сonvert name to lowercase before storing

    if name_key not in contacts: #non-existing contact
        raise KeyError
    
    contacts[name_key] = new_phone
    return "Contact updated."

@input_error
def show_phone(args, contacts):
    """
    Shows the phone no. of a contact name. Expects [name].
    """
    name = args[0]
    name_key = name.lower()  #convert lookup name to lowercase

    if name_key not in contacts: #non-existing contact
        raise KeyError
    
    return contacts[name_key]

def show_all(contacts):
    """
    Prints all saved contacts and their phone numbers.
    """
    if not contacts:
        return "No contacts saved."
    
    output = "All contacts:\n"
    #iters thru original names and phones
    for name, phone in contacts.items():
        output += f"{name}: {phone}\n"
        
    return output.strip()

def main():
    """
    Assistant bot main loop, waits for user input.
    """
    contacts = {}
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        #exit cmds
        if command in ["close", "exit"]:
            print("Good bye!")
            break

        #cmd mapping and exec
        elif command == "hello":
            print("How can I help you?")
            
        elif command == "add":
            #decorator handles errors from add_contact
            print(add_contact(args, contacts))
            
        elif command == "change":
            #decorator handles errors from change_contact
            print(change_contact(args, contacts))
            
        elif command == "phone":
            #decorator handles errors from show_phone
            print(show_phone(args, contacts))
            
        elif command == "all":
            print(show_all(contacts))
            
        elif command: #invalid cmds handling, only print if command is not empty
            print("Invalid command.")

if __name__ == "__main__":
    main()
