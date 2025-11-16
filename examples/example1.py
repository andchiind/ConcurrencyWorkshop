import time

def example1():
    '''This example does not let our current program progress'''
    def foo():
        i = 0
        while True:
            print(f"Hello world - count {i}")
            i +=1 
            time.sleep(1)

    foo() # Run counter iterator

    # Get feedback from the user
    print("Hello user, we have now started doing that work you asked us to do")
    print("Please leave a review below")
    response = input()
    print(f"Thank you for the response: {response}")
