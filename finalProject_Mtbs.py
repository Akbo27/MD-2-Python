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

class SeatUnavailableException(Exception):
    pass

class InvalidShowtimeException(Exception):
    pass

class Movie:
    def __init__(self, title, duration, rating):
        self.title = title
        self.duration = duration
        self.rating = rating
        self.showtimes = []

    def add_showtime(self, showtime):
        self.showtimes.append(showtime)

    def get_showtimes(self):
        return [str(showtime) for showtime in self.showtimes]

    def __str__(self):
        return f"{self.title} ({self.duration} min, {self.rating})"
    
    
class ShowTime:
    def __int__(self, movie, date_time, total_seats=50):
        self.movie = movie
        self.date_time = date_time
        self.total_seats = total_seats
        self.available_seats = total_seats
        self.booked_seats = []

    def book_seat(self, user, seats):
        if self.available_seats < seats:
            raise SeatUnavailableException("There is no enough seats available.")
        self.booked_seats.append(user, seats)
        self.available_seats -= seats
    
    def __str__(self):
        return (
            f"{self.movie.title} : "
            f"{self.date_time.strftime('%Y-%m-%d %H:%M')} - "
            f"{self.available_seats}/{self.total_seats} seats available"
        )


class Booking:
    def __init__(self, user, showtime, seats):
        self.user = user
        self.showtime = showtime
        self.seats = seats
        self.total_price = self.calculate_price()

    def calculate_price(self):
        price_per_seat = 200
        return self.seats * price_per_seat
    
    def __str__(self):
        return (
            f"Booking by {self.user.name} for {self.showtime} - "
            f"{self.seats} seats - Total cost: ${self.total_price}"
        )
    
class User:
    def __init__(self, username, contact_info):
        self.username = username
        self.contact_info = contact_info
        self.bookings = []
    
    def make_booking(self, showtime, seats): 
        booking = Booking(self, showtime, seats)
        self.bookings.append(booking)
        showtime.book_seat(self, seats) 
        return booking  
    
    def __str__(self):  
        return f"User is {self.username}"
    
class Admin(User):
    def__init__(self, name, contact_info):
    super().__init__(name, contact_info)

    def add_movie(self,title, duration, rating):
        return Movie(title, duration, rating)
        
    def add_showtime(self, movie, date_time):
        showtime = ShowTime(movie, date_time)
        movie.add_showtime(showtime)
        return


        





        