
def complex_calculations(a, b):
    try:
        
        division = a / b
        print(f"Division result: {division}")

        
        power = a ** b
        print(f"Power result (a^b): {power}")

      
        if a < 0:
            raise ValueError("Square root of negative number not allowed")
        sqrt_val = a ** 0.5
        print(f"Square root of {a}: {sqrt_val}")

    except ZeroDivisionError:
        print("Error: Division by zero is not allowed!")
    except OverflowError:
        print("Error: Calculation result is too large!")
    except ValueError as ve:
        print(f"Value Error: {ve}")
    except TypeError:
        print("Error: Invalid data type, please enter numbers only!")
    except Exception as e:
        print(f"Unexpected Error: {e}")


complex_calculations(10, 2)     
complex_calculations(5, 0)      
complex_calculations(-9, 2)    
complex_calculations("abc", 3)  