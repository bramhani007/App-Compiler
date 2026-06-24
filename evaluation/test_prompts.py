# A list of test prompts: real and edge cases
prompts = [
    # Realistic
    "Build a task management app with user login, projects, tasks, due dates, and team assignments.",
    "Create an e-commerce platform with product listings, shopping cart, checkout, and order history.",
    "Build a blog platform with articles, comments, user profiles, and admin panel.",
    "Create a fitness tracker with workout logging, progress charts, and meal plans.",
    "Build a hotel booking system with room search, reservations, payments, and reviews.",
    "Create a learning management system with courses, lessons, quizzes, and certificates.",
    "Build a project management tool with Kanban boards, Gantt charts, and time tracking.",
    "Create a customer support ticketing system with ticket creation, assignment, and knowledge base.",
    "Build a social media app with posts, likes, comments, and friend requests.",
    "Create an inventory management system with stock tracking, suppliers, and purchase orders.",
    # Edge cases
    "Make a social network.",  # vague
    "Build a dashboard for sales but also it should be an e-commerce and maybe a blog.",  # conflicting
    "I need an app for my business.",  # incomplete
    "Create a login system with OAuth2 and passwordless but also support username/password.",  # conflicting
    "Build a calendar app that syncs with Google and Outlook but only offline.",  # contradictory
    "Make a simple to-do list.",  # minimal
    "Build an app like Uber but for food.",  # analogy
    "Create a website where people can trade Pokémon cards securely.",  # niche
    "I want an app that does everything my last app did but better.",  # no reference
    "Build an AI-powered personal assistant that can do anything."  # unrealistic
]