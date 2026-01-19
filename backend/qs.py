from app.database import SessionLocal
from app.models.question import Question

def populate_questions():
    db = SessionLocal()
    
    
    questions_data = [
        {
            "id": 1,
            "title": "The Vibe Check (Sum)",
            "description": "Write a program that takes two integers as input and prints their sum. Input Format: Two integers on separate lines.",
            "sample_input": "10\n20",
            "sample_output": "30",
            "difficulty": "easy",
            "points": 2
        },
        {
            "id": 2,
            "title": "Odd or Even Vibe?",
            "description": "Check if a given number is even or odd. Print 'Even' if even, 'Odd' if odd. Input Format: Single integer.",
            "sample_input": "7",
            "sample_output": "Odd",
            "difficulty": "easy",
            "points": 2
        },
        {
            "id": 3,
            "title": "Who is the Biggest Bro?",
            "description": "Given two distinct integers, print the larger one. Input Format: Two integers on separate lines.",
            "sample_input": "50\n12",
            "sample_output": "50",
            "difficulty": "easy",
            "points": 2
        },
        {
            "id": 4,
            "title": "Simple Countdown",
            "description": "Read an integer N. Print numbers from N down to 1 separated by spaces.",
            "sample_input": "5",
            "sample_output": "5 4 3 2 1",
            "difficulty": "easy",
            "points": 2
        },
        {
            "id": 5,
            "title": "Echo Chamber",
            "description": "Take a string input and print it repeated 3 times with spaces in between.",
            "sample_input": "Bro",
            "sample_output": "Bro Bro Bro",
            "difficulty": "easy",
            "points": 2
        },
        {
            "id": 6,
            "title": "Positive Vibes Only",
            "description": "Read an integer. If it's negative, convert it to positive. If positive, keep it as is.",
            "sample_input": "-42",
            "sample_output": "42",
            "difficulty": "easy",
            "points": 2
        },
        {
            "id": 7,
            "title": "String Length",
            "description": "Calculate the length of a given string.",
            "sample_input": "BroCode",
            "sample_output": "7",
            "difficulty": "easy",
            "points": 2
        },
        {
            "id": 8,
            "title": "Celsius to Fahrenheit",
            "description": "Convert temperature from Celsius to Fahrenheit. Formula: (c*9/5)+32. Output rounded to nearest integer.",
            "sample_input": "25",
            "sample_output": "77",
            "difficulty": "easy",
            "points": 2
        },
        {
            "id": 9,
            "title": "First Character",
            "description": "Print the first character of the given string.",
            "sample_input": "Pizza",
            "sample_output": "P",
            "difficulty": "easy",
            "points": 2
        },
        {
            "id": 10,
            "title": "Cube It",
            "description": "Calculate the cube of a number (N * N * N).",
            "sample_input": "3",
            "sample_output": "27",
            "difficulty": "easy",
            "points": 2
        },
         {
    "id": 11,
    "title": "Reverse the Hype",
    "description": "Reverse a given string.",
    "sample_input": "Hello",
    "sample_output": "olleH",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": 12,
    "title": "Factorial Fun",
    "description": "Calculate the factorial of a non-negative integer N.",
    "sample_input": "5",
    "sample_output": "120",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": 13,
    "title": "FizzBuzz Classic",
    "description": "Print numbers from 1 to N, replacing multiples of 3 with 'Fizz', 5 with 'Buzz', and both with 'FizzBuzz'.",
    "sample_input": "5",
    "sample_output": "1 2 Fizz 4 Buzz",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": 14,
    "title": "Array Max",
    "description": "Find the maximum value in an array of integers.",
    "sample_input": "5\n10 20 5 100 2",
    "sample_output": "100",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": 15,
    "title": "Palindrome Checker",
    "description": "Check whether a given string is a palindrome.",
    "sample_input": "racecar",
    "sample_output": "True",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": 16,
    "title": "Sum of Digits",
    "description": "Calculate the sum of digits of an integer.",
    "sample_input": "123",
    "sample_output": "6",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": 17,
    "title": "Count Vowels",
    "description": "Count the number of vowels in a string (case-insensitive).",
    "sample_input": "BroCode",
    "sample_output": "3",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": 18,
    "title": "Linear Search",
    "description": "Find the index of a target element in an array using linear search.",
    "sample_input": "5\n4\n10 20 5 30",
    "sample_output": "2",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": 19,
    "title": "Power Up",
    "description": "Calculate Base raised to the power of Exponent.",
    "sample_input": "2\n3",
    "sample_output": "8",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": 20,
    "title": "Remove Duplicates",
    "description": "Remove duplicate characters from a string while keeping the first occurrence.",
    "sample_input": "banana",
    "sample_output": "ban",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": 21,
    "title": "Prime Time",
    "description": "Check whether a given number is prime.",
    "sample_input": "17",
    "sample_output": "Prime",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": 22,
    "title": "Fibonacci Nth",
    "description": "Find the Nth number in the Fibonacci sequence where N=1 corresponds to 0.",
    "sample_input": "5",
    "sample_output": "3",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": 23,
    "title": "Sort It Out (Bubble Sort)",
    "description": "Sort an array of integers in ascending order using bubble sort logic.",
    "sample_input": "4\n3 1 4 2",
    "sample_output": "1 2 3 4",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": 24,
    "title": "Anagram Check",
    "description": "Check whether two strings are anagrams of each other.",
    "sample_input": "listen\nsilent",
    "sample_output": "Yes",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": 25,
    "title": "Matrix Diagonal Sum",
    "description": "Calculate the sum of the main diagonal of a square matrix.",
    "sample_input": "2\n1 2\n3 4",
    "sample_output": "5",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": 26,
    "title": "Second Largest",
    "description": "Find the second largest number in an array.",
    "sample_input": "4\n10 20 40 30",
    "sample_output": "30",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": 27,
    "title": "Word Count",
    "description": "Count the number of words in a given sentence.",
    "sample_input": "Bro Code is lit",
    "sample_output": "4",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": 28,
    "title": "Pattern Printing",
    "description": "Print a right-angled triangle pattern using '*' of height N.",
    "sample_input": "3",
    "sample_output": "*\n**\n***",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": 29,
    "title": "Missing Number",
    "description": "Find the missing number from an array containing numbers from 0 to N.",
    "sample_input": "3\n3 0 1",
    "sample_output": "2",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": 30,
    "title": "Bracket Balancer",
    "description": "Check whether a sequence of round brackets is balanced.",
    "sample_input": "(())()",
    "sample_output": "Balanced",
    "difficulty": "hard",
    "points": 5
  }
    ]

    for q_data in questions_data:
       
        exists = db.query(Question).filter(Question.id == q_data["id"]).first()
        if not exists:
            new_q = Question(**q_data)
            db.add(new_q)
    
    db.commit()
    db.close()
    print("✅ Successfully populated questions")

if __name__ == "__main__":
    populate_questions()