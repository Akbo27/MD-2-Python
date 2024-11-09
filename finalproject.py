# Key Features
  #For Users
  # select movies, showtimes, and seats.
  # Track availability and prevent double booking.
  # Calculate total costs based on the number of tickets.

  #For Admin
  # add/remove movie and showtime
  # view all the movies and showtimes5


# Main Classes and Attributes
  # Movie: Attributes may include title, duration, rating, showtimes.
  # Showtime: Include movie, date, time, available_seats.
  # Booking: Include user, showtime, seats, total_price.
  # User: Attributes could include username, contact_info, bookings.
  # Admin: An extension of User with additional privileges like adding movies.

# Context Manger - For movie data management
# Decorator - For login 

from datetime import datetime
from functools import wraps

class SeatUnavailableException(Exception):
    pass

class InvalidShowtimeException(Exception):
    pass

def log_action(action: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(f"[LOG] Action: {action} executed.")
            return result
        return wrapper
    return decorator

class ShowTime:
    def __init__(self, movie: 'Movie', date_time: datetime, total_seats: int = 50) -> None:
        self.movie = movie
        self.date_time = date_time
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.booked_seats = []

    def book_seat(self, user: 'User', seats: int) -> None:
        if self.available_seats < seats:
            raise SeatUnavailableException("There are not enough seats available.")
        self.booked_seats.append((user, seats))  
        self.available_seats -= seats 

    def __str__(self) -> str:
        return (
            f"{self.movie.title} : "
            f"{self.date_time.strftime('%Y-%m-%d %H:%M')} - "
            f"{self.available_seats}/{self.total_seats} seats available"
        )

class Movie:
    def __init__(self, title: str, duration: int, rating: str) -> None:
        self.title = title
        self.duration = duration
        self.rating = rating
        self.showtimes = [] 

    def add_showtime(self, showtime: ShowTime) -> None:
        self.showtimes.append(showtime)

    def get_showtimes(self) -> list[str]:
        return [str(showtime) for showtime in self.showtimes]

    def __str__(self) -> str:
        return f"{self.title} ({self.duration} min, {self.rating})"
    
class Booking:
    def __init__(self, user: 'User', showtime: ShowTime, seats: int) -> None:
        self.user = user
        self.showtime = showtime
        self.seats = seats
        self.total_price = self.calculate_price()

    def calculate_price(self) -> float:
        price_per_seat = 200  
        return self.seats * price_per_seat
    
    def __str__(self) -> str:
        return (
            f"Booking by {self.user.username} for {self.showtime} - "
            f"{self.seats} seats - Total cost: ${self.total_price}"
        )

class User:
    def __init__(self, username: str, contact_info: str) -> None:
        self.username = username
        self.contact_info = contact_info
        self.bookings = [] 
    
    def make_booking(self, showtime: ShowTime, seats: int) -> Booking:
        booking = Booking(self, showtime, seats)
        self.bookings.append(booking)
        showtime.book_seat(self, seats)
        return booking  
    
    def __str__(self) -> str:  
        return f"User: {self.username}"

class Admin(User):
    def __init__(self, username: str, contact_info: str) -> None:
        super().__init__(username, contact_info)

    @log_action("Add Movie")
    def add_movie(self, title: str, duration: int, rating: str) -> Movie:
        return Movie(title, duration, rating)

    @log_action("Add Showtime")
    def add_showtime(self, movie: Movie, date_time: datetime) -> ShowTime:
        showtime = ShowTime(movie, date_time)
        movie.add_showtime(showtime)
        return showtime

    @log_action("Remove Showtime")
    def remove_showtime(self, movie: Movie, showtime: ShowTime) -> None:
        if showtime in movie.showtimes:
            movie.showtimes.remove(showtime)
        else:
            raise InvalidShowtimeException("Showtime not found for the specified movie.")
        
class MovieDataFileHandler:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def __enter__(self):
        try:
            with open(self.filename, 'r') as file:
                self.data = file.readlines()
        except FileNotFoundError:
            self.data = []  # Default data if no file found
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.filename, 'w') as file:
            file.writelines(self.data)

def load_movies_from_file(filename: str):
    movie_list = []
    user_list = []
    
    with MovieDataFileHandler(filename) as file_handler:
        data = file_handler.data
        for line in data:
            if line.startswith("Movie:"):
                parts = line.strip().split(',')  
                title = parts[1].split(":")[1].strip()
                duration = int(parts[2].split(":")[1].strip())
                rating = parts[3].split(":")[1].strip()
                movie_list.append(Movie(title, duration, rating))
            elif line.startswith("User:"):
                parts = line.strip().split(',')
                username = parts[1].split(":")[1].strip()
                contact_info = parts[2].split(":")[1].strip()
                user_list.append(User(username, contact_info))
    
    return movie_list, user_list

def save_movies_to_file(filename: str, movie_list: list[Movie], user_list: list[User]):
    with MovieDataFileHandler(filename) as file_handler:
        file_handler.data = []
        # Saving movies
        for movie in movie_list:
            file_handler.data.append(f"Movie: {movie.title}, Duration: {movie.duration}, Rating: {movie.rating}\n")
        # Saving users
        for user in user_list:
            file_handler.data.append(f"User: {user.username}, Contact: {user.contact_info}\n")

def display_menu():
    print("\n------------------------------")
    print("\n--- Welcome to Bobo Cinema ---")
    print("\n------------------------------")
    print("1. Log in as User")
    print("2. Log in as Admin")
    print("3. Exit")
    choice = input("Select an option: ")
    return choice

def user_menu(user: User, movie_list: list[Movie]):
    while True:
        print("\n-----------------")
        print("\n--- User Menu ---")
        print("\n-----------------")
        print("1. View Available Movies and Showtimes")
        print("2. Make a Booking")
        print("3. View Bookings")
        print("4. Exit to Main Menu")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            print("\n--- Available Movies ---")
            for movie in movie_list:
                print(movie)
            print("\n--- Available Showtimes ---")
            for movie in movie_list:
                for showtime in movie.showtimes:
                    print(showtime)
        
        elif choice == '2':
            movie_name = input("Enter movie title to book: ")
            movie = next((m for m in movie_list if m.title.lower() == movie_name.lower()), None)
            if movie:
                print("\nAvailable showtimes for", movie.title)
                for showtime in movie.showtimes:
                    print(showtime)
                showtime_str = input("Enter the showtime you want to book (format: YYYY-MM-DD HH:MM): ")
                showtime = next((s for s in movie.showtimes if s.date_time.strftime('%Y-%m-%d %H:%M') == showtime_str), None)
                if showtime:
                    seats = int(input("Enter number of seats to book: "))
                    try:
                        booking = user.make_booking(showtime, seats)
                        print("\nBooking Successful:")
                        print(booking)
                    except SeatUnavailableException as e:
                        print(f"Error: {e}")
                else:
                    print("Invalid showtime selected.")
            else:
                print("Movie not found.")

        elif choice == '3':
            if not user.bookings:
                print("No bookings made yet.")
            else:
                print("\nYour Bookings:")
                for booking in user.bookings:
                    print(booking)
        
        elif choice == '4':
            break

def admin_menu(admin: Admin, movie_list: list[Movie]):
    while True:
        print("\n-----------------")
        print("\n--- Admin Menu ---")
        print("\n-----------------")
        print("1. Add Movie")
        print("2. Add Showtime to Movie")
        print("3. Remove Showtime from Movie")
        print("4. View All Movies and Showtimes")
        print("5. Exit to Main Menu")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            title = input("Enter movie title: ")
            duration = int(input("Enter movie duration (minutes): "))
            rating = input("Enter movie rating: ")
            movie = admin.add_movie(title, duration, rating)
            movie_list.append(movie)
            print(f"Movie '{movie.title}' added successfully.")
        
        elif choice == '2':
            title = input("Enter movie title: ")
            movie = next((m for m in movie_list if m.title.lower() == title.lower()), None)
            if movie:
                date_time_str = input("Enter showtime (format: YYYY-MM-DD HH:MM): ")
                date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
                showtime = admin.add_showtime(movie, date_time)
                print(f"Showtime for '{movie.title}' added: {showtime}")
            else:
                print("Movie not found.")
        
        elif choice == '3':
            title = input("Enter movie title: ")
            movie = next((m for m in movie_list if m.title.lower() == title.lower()), None)
            if movie:
                showtime_str = input("Enter showtime to remove (format: YYYY-MM-DD HH:MM): ")
                showtime = next((s for s in movie.showtimes if s.date_time.strftime('%Y-%m-%d %H:%M') == showtime_str), None)
                if showtime:
                    admin.remove_showtime(movie, showtime)
                    print(f"Showtime removed from '{movie.title}': {showtime}")
                else:
                    print("Showtime not found.")
            else:
                print("Movie not found.")
        
        elif choice == '4':
            print("\n--- All Movies and Showtimes ---")
            for movie in movie_list:
                print(movie)
                for showtime in movie.showtimes:
                    print(showtime)
        
        elif choice == '5':
            break

def main():
    filename = 'movie_data.txt'
    movie_list, user_list = load_movies_from_file(filename)
    
    while True:
        choice = display_menu()
        
        if choice == '1':
            username = input("Enter your username: ")
            contact_info = input("Enter your contact info: ")
            user = User(username, contact_info)
            user_menu(user, movie_list)
        
        elif choice == '2':
            username = input("Enter your admin username: ")
            contact_info = input("Enter your admin contact info: ")
            admin = Admin(username, contact_info)
            admin_menu(admin, movie_list)
        
        elif choice == '3':
            save_movies_to_file(filename, movie_list, user_list)
            print("Data saved successfully. Exiting the program.")
            break

main()
