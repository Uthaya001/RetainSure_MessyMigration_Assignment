Project Story – From Legacy to Clean Code
This project began as a messy, legacy Flask application—the kind where all the logic was crammed into one file, routes were tangled, and security was an afterthought. It technically worked, but maintaining or scaling it was a nightmare.

I took this as a challenge to refactor the entire codebase into a clean, modular, and production-ready User Management API, using everything I’ve learned about software engineering best practices.

💥 Challenges I Faced
🔥 Spaghetti Code: The original app had everything in one script (app.py)—routes, logic, and even pseudo-database operations.
🛠️ Solution: I split the code into proper layers—routes, services, models, and utilities.

🔐 Security Issues: Passwords were stored in plain text (yes, really!).
🛠️ Solution: Integrated password hashing using Werkzeug and strict input validation.

📦 No Testing: There were zero tests. No way to confidently make changes.
🛠️ Solution: Wrote unit tests using pytest to cover all critical endpoints.

🧪 Data Management: The original version didn’t even use a real database—just a global list in memory.
🛠️ Solution: Built a simple in-memory model structure with proper CRUD operations that can easily be swapped with a real database.

🚫 Bad Error Handling: All errors led to generic messages or app crashes.
🛠️ Solution: Implemented meaningful error responses and clean exception handling.

💔 Broken Validation: Inputs weren’t sanitized or validated, making the app vulnerable to injections or unexpected crashes.
🛠️ Solution: Built a custom validation utility to check names, emails, and passwords strictly but gracefully.

🌱 What I Learned
How to refactor legacy code without breaking functionality

How to implement clean architecture principles in real projects

Writing better, testable and maintainable backend code

The importance of error handling, input validation, and separation of concerns

Building APIs that are secure, not just functional

🙌 Why This Matters
This wasn’t just a technical exercise—it was a personal journey in code quality, discipline, and engineering mindset. I learned how to think like a backend engineer, not just a coder.

This project has made me more confident in taking messy problems and turning them into clean, scalable solutions—and that’s what software development is all about.
