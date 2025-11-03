import pygame
import sys
import random
from datetime import datetime, timedelta

# Initialize Pygame
pygame.init()

# Get current time
now = datetime.now()
base_time = now.replace(minute=0, second=0, microsecond=0)
offsets = [1, 3, 6]

def show_ticket_window(movie, date_time, theater, seat):
    # Extract just the time portion (remove the "Time X:" prefix)
    # If the date_time contains "Time X:", we'll extract just the actual time part
    if ":" in date_time and len(date_time.split(":", 1)) > 1:
        actual_time = date_time.split(":", 1)[1].strip()
    else:
        actual_time = date_time
    
    # Create a new window for the ticket
    win_width, win_height = 500, 241
    ticket_win = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("Your Movie Ticket")

    font = pygame.font.SysFont(None, 36)

    lines = [
        f"Movie: {movie}",
        f"Time: {actual_time}",
        f"Theater: {theater}",
        f"Seat: {seat}"
    ]

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ticket_win.fill((255, 255, 255))
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (0, 0, 0))
            ticket_win.blit(text_surface, (50, 50 + i * 40))
        
        pygame.display.update()
        clock.tick(30)

def otp_window(otp):
    """Open a Pygame window to display OTP."""
    # Create a new window for OTP
    win_width, win_height = 400, 255
    otp_win = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("OTP Verification")
    
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)
    
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        otp_win.fill((255, 255, 255))
        
        # Display OTP
        text_surface = font.render(f"Your OTP: {otp}", True, (0, 0, 0))
        otp_win.blit(text_surface, (100, 70))
        
        pygame.display.update()
        clock.tick(30)
        
    pygame.quit()

# --- Helper functions ---
def ticket(price):
    mapping = {
        '1': 'Please, pay your ticket: Rp 75,000',
        '2': 'Please, pay your ticket: Rp 150,000',
        '3': 'Please, pay your ticket: Rp 300,000'
    }
    return mapping.get(price, 'Error')

def show_times():
    times = []
    for i, h in enumerate(offsets, start=1):
        future_time = base_time + timedelta(hours=h)
        date_time = f"Time {i}: {future_time.strftime('%Y-%m-%d %H:%M')}"
        print(date_time)
        times.append(date_time)
    return times

def get_valid_input(prompt, length, input_type="digits"):
    """Get valid input with specific length and type requirements"""
    while True:
        user_input = input(prompt)
        
        # Check if input is the correct length
        if len(user_input) != length:
            print(f"Error: Must be exactly {length} characters")
            continue
            
        # Check if input contains only digits
        if input_type == "digits" and not user_input.isdigit():
            print("Error: Must contain only numbers")
            continue
            
        return user_input

def payment_flow(movie, date_time):
    price = input('Input your category ticket movie: \n1. Regular 2. Premium 3. VIP: ')
    seat_msg = ticket(price)
    if seat_msg == 'Error':
        print('Error')
        return

    print('Your', movie, 'seat already booked!')
    print(seat_msg)
    
    # Get card number with validation (must be 16 digits)
    card = get_valid_input('Please enter your card number (16 digits): ', 16, "digits")
    
    # Get CVV with validation (must be 3 digits)
    code = get_valid_input('Please enter your CVC/CVV (3 digits): ', 3, "digits")

    otp = random.randint(100000, 999999)
    
    # Show OTP in a Pygame window
    print("An OTP window will appear. Check it for your verification code.\nFor security reasons, please close the window before entering the OTP")
    otp_window(otp)

    # Ask OTP in main flow
    otp_enter = input('Please enter the OTP from the window: ')

    if otp_enter.isdigit() and int(otp_enter) == otp:
        print('Payment success!')
        theater = random.randint(1, 5)
        if price == '1':
            seat = random.randint(61, 200)
        elif price == '2':
            seat = random.randint(11, 60)
        elif price == '3':
            seat = random.randint(1, 10)
        print("Your ticket window will appear shortly.")
        show_ticket_window(movie, date_time, theater, seat)
    else:
        print('Error: Wrong OTP')

# --- Main flow ---
print('Movie Ticket')

# Define all available movies
all_movies = {
    '1': 'Shadows of Tomorrow',
    '2': 'The Glass Crown',
    '3': 'Echoes in the Static',
    '4': 'Whispering Hollow',
    '5': 'Crimson Horizon',
    '6': 'The Last Lantern',
    '7': 'Neon Mirage',
    '8': 'Frostfire',
    '9': 'Beneath the Iron Sky'
}

# Randomly select 3 unique movies from all available movies
movie_keys = list(all_movies.keys())
random.shuffle(movie_keys)
selected_movie_keys = movie_keys[:3]

# Create a new mapping with sequential numbers (1, 2, 3)
movies = {}
for i, key in enumerate(selected_movie_keys, 1):
    movies[str(i)] = all_movies[key]

# Display the selected movies
print("Today's featured movies:")
for key, movie_name in movies.items():
    print(f"{key}. {movie_name}")

movie_choice = input('Choose movie to watch (1/2/3): ')

if movie_choice in movies:
    title = movies[movie_choice]
    times = show_times()
    c_date_time = input('Choose time to watch (1/2/3): ')
    if c_date_time in ['1', '2', '3']:
        date_time = times[int(c_date_time) - 1]
        payment_flow(title, date_time)
    else:
        print('Error: Invalid time choice')
else:
    print('Error: Invalid movie choice')

# Clean up at the very end
pygame.quit()