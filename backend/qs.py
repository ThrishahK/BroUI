from app.database import SessionLocal
from app.models.question import Question

def populate_questions():
    db = SessionLocal()
    
    
    questions_data = [
  {
    "id": "E01",
    "title": "The Vibe Check (Sum)",
    "description": "Write a program that takes two integers as input and prints their sum.",
    "input_format": "Two integers on separate lines.",
    "output_format": "A single integer representing the sum.",
    "sample_input": "10\n20",
    "sample_output": "30",
    "difficulty": "easy",
    "points": 2
  },
  {
    "id": "E02",
    "title": "Odd or Even Vibe?",
    "description": "Check if a given number is even or odd.",
    "input_format": "Single integer.",
    "output_format": "Print \"Even\" or \"Odd\".",
    "sample_input": "7",
    "sample_output": "Odd",
    "difficulty": "easy",
    "points": 2
  },
  {
    "id": "E03",
    "title": "Who is the Biggest Bro?",
    "description": "Given two distinct integers, print the larger one.",
    "input_format": "Two integers on separate lines.",
    "output_format": "The larger integer.",
    "sample_input": "50\n12",
    "sample_output": "50",
    "difficulty": "easy",
    "points": 2
  },
  {
    "id": "E04",
    "title": "Simple Countdown",
    "description": "Print numbers from N down to 1.",
    "input_format": "Single integer N.",
    "output_format": "Numbers separated by space.",
    "sample_input": "5",
    "sample_output": "5 4 3 2 1",
    "difficulty": "easy",
    "points": 2
  },
  {
    "id": "E05",
    "title": "Echo Chamber",
    "description": "Print the given string three times separated by spaces.",
    "input_format": "Single string.",
    "output_format": "String repeated three times.",
    "sample_input": "Bro",
    "sample_output": "Bro Bro Bro",
    "difficulty": "easy",
    "points": 2
  },
  {
    "id": "E06",
    "title": "Positive Vibes Only",
    "description": "Convert a negative number to positive.",
    "input_format": "Single integer.",
    "output_format": "Positive integer.",
    "sample_input": "-42",
    "sample_output": "42",
    "difficulty": "easy",
    "points": 2
  },
  {
    "id": "E07",
    "title": "String Length",
    "description": "Calculate the length of a string.",
    "input_format": "Single string.",
    "output_format": "Integer length.",
    "sample_input": "BroCode",
    "sample_output": "7",
    "difficulty": "easy",
    "points": 2
  },
  {
    "id": "E08",
    "title": "Celsius to Fahrenheit",
    "description": "Convert Celsius to Fahrenheit using (C * 9/5) + 32.",
    "input_format": "Integer Celsius value.",
    "output_format": "Integer Fahrenheit value.",
    "sample_input": "25",
    "sample_output": "77",
    "difficulty": "easy",
    "points": 2
  },
  {
    "id": "E09",
    "title": "First Character",
    "description": "Print the first character of a string.",
    "input_format": "Single string.",
    "output_format": "First character.",
    "sample_input": "Pizza",
    "sample_output": "P",
    "difficulty": "easy",
    "points": 2
  },
  {
    "id": "E10",
    "title": "Cube It",
    "description": "Calculate the cube of a number.",
    "input_format": "Single integer.",
    "output_format": "Cubed value.",
    "sample_input": "3",
    "sample_output": "27",
    "difficulty": "easy",
    "points": 2
  },
  {
    "id": "M01",
    "title": "Reverse the Hype",
    "description": "Reverse a given string.",
    "input_format": "Single string.",
    "output_format": "Reversed string.",
    "sample_input": "Hello",
    "sample_output": "olleH",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": "M02",
    "title": "Factorial Fun",
    "description": "Calculate factorial of a non-negative integer.",
    "input_format": "Single integer N.",
    "output_format": "Factorial of N.",
    "sample_input": "5",
    "sample_output": "120",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": "M03",
    "title": "FizzBuzz Classic",
    "description": "Print numbers from 1 to N with FizzBuzz rules.",
    "input_format": "Single integer N.",
    "output_format": "Space separated values.",
    "sample_input": "5",
    "sample_output": "1 2 Fizz 4 Buzz",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": "M04",
    "title": "Array Max",
    "description": "Find the maximum number in an array.",
    "input_format": "First line N, second line N integers.",
    "output_format": "Maximum integer.",
    "sample_input": "5\n10 20 5 100 2",
    "sample_output": "100",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": "M05",
    "title": "Palindrome Checker",
    "description": "Check if a string is a palindrome.",
    "input_format": "Single string.",
    "output_format": "\"True\" or \"False\".",
    "sample_input": "racecar",
    "sample_output": "True",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": "M06",
    "title": "Sum of Digits",
    "description": "Calculate sum of digits of an integer.",
    "input_format": "Single integer.",
    "output_format": "Sum of digits.",
    "sample_input": "123",
    "sample_output": "6",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": "M07",
    "title": "Count Vowels",
    "description": "Count vowels in a string.",
    "input_format": "Single string.",
    "output_format": "Integer count.",
    "sample_input": "BroCode",
    "sample_output": "3",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": "M08",
    "title": "Linear Search",
    "description": "Find index of target element in an array.",
    "input_format": "Target, N, then N integers.",
    "output_format": "Index or -1.",
    "sample_input": "5\n4\n10 20 5 30",
    "sample_output": "2",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": "M09",
    "title": "Power Up",
    "description": "Calculate base raised to exponent.",
    "input_format": "Base and exponent on separate lines.",
    "output_format": "Result.",
    "sample_input": "2\n3",
    "sample_output": "8",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": "M10",
    "title": "Remove Duplicates",
    "description": "Remove duplicate characters from a string.",
    "input_format": "Single string.",
    "output_format": "String without duplicates.",
    "sample_input": "banana",
    "sample_output": "ban",
    "difficulty": "medium",
    "points": 3
  },
  {
    "id": "H01",
    "title": "Prime Time",
    "description": "Check if a number is prime.",
    "input_format": "Single integer.",
    "output_format": "\"Prime\" or \"Not Prime\".",
    "sample_input": "17",
    "sample_output": "Prime",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": "H02",
    "title": "Fibonacci Nth",
    "description": "Find the Nth Fibonacci number.",
    "input_format": "Single integer N.",
    "output_format": "Nth Fibonacci number.",
    "sample_input": "5",
    "sample_output": "3",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": "H03",
    "title": "Sort It Out",
    "description": "Sort an array in ascending order.",
    "input_format": "N then N integers.",
    "output_format": "Sorted integers.",
    "sample_input": "4\n3 1 4 2",
    "sample_output": "1 2 3 4",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": "H04",
    "title": "Anagram Check",
    "description": "Check if two strings are anagrams.",
    "input_format": "Two strings on separate lines.",
    "output_format": "\"Yes\" or \"No\".",
    "sample_input": "listen\nsilent",
    "sample_output": "Yes",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": "H05",
    "title": "Matrix Diagonal Sum",
    "description": "Calculate sum of main diagonal of a matrix.",
    "input_format": "N then N rows of N integers.",
    "output_format": "Diagonal sum.",
    "sample_input": "2\n1 2\n3 4",
    "sample_output": "5",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": "H06",
    "title": "Second Largest",
    "description": "Find the second largest number in an array.",
    "input_format": "N then N integers.",
    "output_format": "Second largest number.",
    "sample_input": "4\n10 20 40 30",
    "sample_output": "30",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": "H07",
    "title": "Word Count",
    "description": "Count number of words in a sentence.",
    "input_format": "Sentence string.",
    "output_format": "Word count.",
    "sample_input": "Bro Code is lit",
    "sample_output": "4",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": "H08",
    "title": "Pattern Printing",
    "description": "Print a right-angled triangle pattern.",
    "input_format": "Single integer N.",
    "output_format": "Pattern of stars.",
    "sample_input": "3",
    "sample_output": "*\n**\n***",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": "H09",
    "title": "Missing Number",
    "description": "Find the missing number in the array.",
    "input_format": "N then N numbers.",
    "output_format": "Missing number.",
    "sample_input": "3\n3 0 1",
    "sample_output": "2",
    "difficulty": "hard",
    "points": 5
  },
  {
    "id": "H10",
    "title": "Bracket Balancer",
    "description": "Check if brackets are balanced.",
    "input_format": "Bracket string.",
    "output_format": "\"Balanced\" or \"Unbalanced\".",
    "sample_input": "(())()",
    "sample_output": "Balanced",
    "difficulty": "hard",
    "points": 5
  }
]


    for q_data in questions_data:
        # Check if question already exists by question_id
        exists = db.query(Question).filter(Question.question_id == q_data["id"]).first()
        if not exists:
            # Map the data to match the Question model fields
            new_q = Question(
                question_id=q_data["id"],
                title=q_data.get("title", ""),
                description=q_data.get("description", ""),
                sample_input=q_data.get("sample_input"),
                sample_output=q_data.get("sample_output"),
                difficulty=q_data.get("difficulty", "medium"),
                points=q_data.get("points", 10),
                is_active=True
            )
            db.add(new_q)
    
    db.commit()
    db.close()
    print("✅ Successfully populated questions")

if __name__ == "__main__":
    populate_questions()