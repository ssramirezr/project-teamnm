
def calcular_first(producciones):
    # Initialize the dictionary of FIRST sets
    first = {}
    for no_terminal in producciones:
        # Initialize the dictionary of FIRST sets for each non-terminal symbol with an empty set
        first[no_terminal] = set()
    # Iterate over the productions to find the terminals
    for no_terminal, reglas in producciones.items():
        for regla in reglas:
            for simbolo in regla:
                # Terminals are lowercase letters
                if simbolo.islower():  
                    # Add the terminal to the FIRST set of the non-terminal symbol
                    if simbolo not in first:
                        first[simbolo] = {simbolo}

    # Flag to check if there were changes in the FIRST sets
    hubo_cambios = True
    while hubo_cambios:
        hubo_cambios = False
        # Iterate over the productions to calculate the FIRST sets
        for no_terminal, reglas in producciones.items():
            # Iterate over the rules of each non-terminal symbol
            for regla in reglas:
                i = 0
                # Iterate over the symbols of each rule
                while i < len(regla):
                    # Get the symbol
                    simbolo = regla[i]
                    # If it finds a lowercase letter, it is a terminal
                    if simbolo.islower():  
                        # Add the terminal to the FIRST set of the non-terminal symbol
                        if simbolo not in first[no_terminal]:
                            first[no_terminal].add(simbolo)
                            # Set the flag to True to indicate that there were changes in the FIRST set
                            hubo_cambios = True
                        # Break the loop since the only possible FIRST for this rule is found
                        break  
                    # If it is an uppercase letter, it is a non-terminal
                    else:  
                        # Save the size of the FIRST set before adding new elements
                        tamano_antes = len(first[no_terminal])
                        # Add the FIRST set of the non-terminal symbol to the FIRST set of the current non-terminal symbol without the empty string
                        first[no_terminal] |= first[simbolo] - {'e'}
                        # If the empty string is not in the FIRST set of the non-terminal symbol, it breaks the loop
                        if 'e' not in first[simbolo]:
                            break
                        i += 1
                    # If the loop reaches the end of the rule, it adds the empty string to the FIRST set of the non-terminal symbol
                    if i == len(regla):
                        first[no_terminal].add('e')
                    # If the size of the FIRST set before adding new elements is different from the size after adding new elements, it sets the flag to True
                    if tamano_antes != len(first[no_terminal]):
                        hubo_cambios = True

    # Return the dictionary of FIRST sets
    return first

def calcular_follow(producciones, first):

    # Initialize the dictionary of FOLLOW sets with an empty set for each non-terminal symbol
    follow = {no_terminal: set() for no_terminal in producciones}
    # Get the start symbol which is the first non-terminal symbol
    start_symbol = list(producciones.keys())[0]
    # Add the end of input symbol to the FOLLOW set of the start symbol, where $ represents the end of input
    follow[start_symbol].add('$')

    # Flag to check if there were changes in the FOLLOW sets
    hubo_cambios = True
    while hubo_cambios:
        hubo_cambios = False

        # Iterate over the productions to calculate the FOLLOW sets
        for no_terminal, reglas in producciones.items():
            # Iterate over the rules of each non-terminal symbol
            for regla in reglas:
                # Iterate over the symbols of each rule
                for i in range(len(regla)):
                    # Get the symbol
                    simbolo = regla[i]
                    # We are just interested in non-terminal symbols
                    if simbolo.isupper():
                        # Initialize the next set
                        siguiente_conjunto = set()
                        j = i + 1
                        # Iterate over the symbols after the current symbol
                        while j < len(regla):
                            # Get the next symbol
                            siguiente_simbolo = regla[j]
                            # We get the FIRST set of the next symbol without the empty string
                            siguiente_conjunto |= first[siguiente_simbolo] - {'e'}
                            # If the empty string is not in the FIRST set of the next symbol, it breaks the loop
                            if 'e' not in first[siguiente_simbolo]:
                                break
                            j += 1
                        else:
                            # If the loop reaches the end of the rule, it adds the FOLLOW set of the non-terminal symbol
                            siguiente_conjunto |= follow[no_terminal]
                        
                        # Save the size of the FOLLOW set before adding new elements
                        tamano_antes = len(follow[simbolo])
                        # Add the next set to the FOLLOW set of the current non-terminal symbol
                        follow[simbolo] |= siguiente_conjunto
                        # If the size of the FOLLOW set before adding new elements is different from the size after adding new elements, it sets the flag to True
                        if tamano_antes != len(follow[simbolo]):
                            hubo_cambios = True

    return follow

def leer_producciones():
    # Read the number of grammars
    n_gramaticas = int(input())
    for _ in range(n_gramaticas):
        # Read the number of non-terminals symbols
        n_no_terminales = int(input())
        #Initialize the dictionary of productions
        producciones = {}
        for _ in range(n_no_terminales):
            # Read the productions for each non-terminal symbol and store them in the dictionary
            entrada = input().split()
            no_terminal = entrada[0]
            reglas = entrada[1:]
            producciones[no_terminal] = reglas
        # Calculate the FIRST and FOLLOW sets
        first = calcular_first(producciones)
        follow = calcular_follow(producciones, first)

        # Print the FIRST and FOLLOW sets
        for no_terminal in first:
            print(f"First ({no_terminal}) = {first[no_terminal]}")
        for no_terminal in follow:
            print(f"Follow ({no_terminal}) = {follow[no_terminal]}")

# Calls the function to run the code
leer_producciones()