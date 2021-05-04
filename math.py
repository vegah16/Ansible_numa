import sys

def percent(num1, num2):
    return (num1 / num2)
# Take input from the user
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

with open('/home/rof/Ansible_numa/results/percentage.txt', 'w') as f:
    print("The packetdrop percentage is", percent(num1, num2)*100, file=f)