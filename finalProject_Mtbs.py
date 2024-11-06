# Key Features
  # Allow users to select movies, showtimes, and seats.
  # Track availability and prevent double booking.
  # Calculate total costs based on the number of tickets and any discounts.

# Main Classes and Attributes
  # Movie: Attributes may include title, duration, rating, showtimes.
  # Showtime: Include movie, date, time, available_seats.
  # Booking: Include user, showtime, seats, total_price.
  # User: Attributes could include username, contact_info, bookings.
  # Admin: An extension of User with additional privileges like adding movies.

import json
from datetime import datetime

# Custom Exceptions
class SeatUnavailableException(Exception):
    pass

class InvalidShowtimeException(Exception):
    pass


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

class ShowTime:
    def __init__(self, movie: Movie, date_time: datetime, total_seats: int = 50) -> None:
        self.movie = movie
        self.date_time = date_time
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.booked_seats = []  

    def book_seat(self, user: User, seats: int) -> None:

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

class Booking:
    def __init__(self, user: User, showtime: ShowTime, seats: int) -> None:
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

    def add_movie(self, title: str, duration: int, rating: str) -> Movie:
        return Movie(title, duration, rating)

    def add_showtime(self, movie: Movie, date_time: datetime) -> ShowTime:
        showtime = ShowTime(movie, date_time)
        movie.add_showtime(showtime)
        return showtime

    def remove_showtime(self, movie: Movie, showtime: ShowTime) -> None:
        if showtime in movie.showtimes:
            movie.showtimes.remove(showtime)
        else:
            raise InvalidShowtimeException("Showtime not found for the specified movie.")
        
def main() -> None:
    admin = Admin("admin_user", "admin@example.com")
    movie = admin.add_movie("Inception", 148, "PG-13")
    
    showtime1 = admin.add_showtime(movie, datetime(2023, 11, 15, 19, 30))
    showtime2 = admin.add_showtime(movie, datetime(2023, 11, 15, 21, 30))

    print("Available Showtimes for 'Inception':")
    for showtime in movie.get_showtimes():
        print(showtime)

    user = User("johndoe", "johndoe@example.com")
    booking = user.make_booking(showtime1, 3)

    print("\nBooking Details:")
    print(booking)

    print("\nUpdated Showtimes after booking:")
    for showtime in movie.get_showtimes():
        print(showtime)
    
    admin.remove_showtime(movie, showtime2)
    
    print("\nShowtimes after removing one:")
    for showtime in movie.get_showtimes():
        print(showtime)


if __name__ == "__main__":
    main()
