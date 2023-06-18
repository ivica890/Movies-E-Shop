import json

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from hw5.MovieForm import MovieForm
from hw5.models import Film, Seat, Order


def film_list(request):
    films = Film.objects.all()
    return render(request, 'film_list.html', {'films': films})


def seat_list(request, film_id):
    film = Film.objects.get(pk=film_id)
    seats = Seat.objects.filter(film=film)
    return render(request, 'seat_list.html', {'film': film, 'seats': seats})


def save_seat(request):
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats[]')

        # Update the is_available field for the selected seats
        Seat.objects.filter(seat_number__in=selected_seats).update(is_available=False)

        # Perform any other actions after saving the selected seats

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def remove_seat(request):
    if request.method == 'POST':
        seat_id = request.POST.get('seatId')
        # Perform database update to remove the deselected seat with the provided seat_id
        # Replace the following lines with your actual database update logic
        seat = Seat.objects.get(pk=seat_id)
        seat.is_selected = False
        seat.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def shopping_cart(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shopping_cart.html', {'orders': orders})


@login_required
def confirmation(request):
    # Process payment and create the Order instance

    # Send email confirmation to the user
    # user = request.user
    # subject = 'Order Confirmation'
    # message = 'Thank you for your order. We have received your payment.'
    # from_email = 'your-email@example.com'  # Replace with your email address
    # to_email = [user.email]
    #
    # send_mail(subject, message, from_email, to_email)

    return render(request, 'confirmation.html')


def get_film_info(request):
    film_id = request.GET.get('film_id')

    try:
        film = get_object_or_404(Film, id=film_id)
    except ValueError:
        return JsonResponse({'error': 'Invalid film ID.'}, status=400)
    except Film.DoesNotExist:
        return JsonResponse({'error': 'Film not found.'}, status=404)

    film_info = {
        'title': film.title,
        'description': film.description,
        'price': film.price,
    }

    return JsonResponse(film_info)


def add_to_cart(request):
    if request.method == 'POST':
        # Retrieve the payload from the request body
        payload = json.loads(request.body)

        # Access the filmId and selectedSeats from the payload
        film_id = payload.get('filmId')
        selected_seats = payload.get('selectedSeats')

        # Perform any necessary validation or processing with the received data

        # Create the order for each selected seat and save them to the database
        for seat_id in selected_seats:
            try:
                seat = Seat.objects.get(id=seat_id)
            except Seat.DoesNotExist:
                return JsonResponse({'error': f'Seat with ID {seat_id} does not exist.'}, status=404)

            order = Order(user=request.user, seat=seat, film_id=film_id)
            order.save()

        # Return a success response
        return JsonResponse({'message': 'Seats added to the shopping cart.'}, status=200)

    # Return an error response for unsupported request methods
    return JsonResponse({'error': 'Unsupported request method.'}, status=405)


def logout_view(request):
    logout(request)
    return redirect('film_list')


def add_movie(request):
    form = MovieForm()
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.save()
            return redirect('film_list')

    context = {'form': form}
    return render(request, 'add_movie.html', context=context)


def delete_movie(request, movie_id):
    movie = get_object_or_404(Film, id=movie_id)
    movie.delete()
    return redirect('film_list')


def about(request):
    film_id = request.GET.get('film_id')
    film = Film.objects.get(id=film_id)
    return render(request, 'about.html', {'film': film})


def home(request):
    films = Film.objects.all()
    return render(request, 'home.html', {'films': films})


def create_order(request):
    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')

        # Check if the seat exists
        try:
            seat = Seat.objects.get(id=seat_id)
        except Seat.DoesNotExist:
            return JsonResponse({'error': 'Seat not found'})

        # Check if an order already exists for the selected seat
        existing_order = Order.objects.filter(user=request.user, seat=seat).first()
        if existing_order:
            return JsonResponse({'error': 'An order already exists for this seat'})

        # Set the seat status to unavailable
        seat.is_available = False
        seat.save()

        # Create the order
        order = Order(user=request.user, seat=seat)

        # Save the order
        order.save()

        # Return a JSON response
        return JsonResponse({'order_id': order.id})
    else:
        return JsonResponse({'error': 'Invalid request method'})


@require_POST
@login_required
def clear_shopping_cart(request):
    # Clear the shopping cart in the session
    if 'shopping_cart' in request.session:
        del request.session['shopping_cart']
        messages.success(request, 'Shopping cart cleared successfully.')
    else:
        messages.error(request, 'No shopping cart found.')

    # Clear the orders in the database for the logged-in user
    Order.objects.filter(user=request.user).delete()
    messages.success(request, 'Orders cleared successfully.')

    return redirect('confirmation')


def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)

    # Get the seat associated with the order
    seat = order.seat

    # Delete the order
    order.delete()

    # Make the seat available again
    seat.is_available = True
    seat.save()

    return redirect('shopping_cart')


def filter_movies(request):
    category = request.GET.get('category')
    filtered_movies = Film.objects.filter(category=category)

    movies = []
    for movie in filtered_movies:
        movies.append({
            'title': movie.title,
            'description': movie.description,
            'price': movie.price,
            'file': movie.file.url,
            'trailer': movie.trailer,
            'category': movie.category
        })

    return JsonResponse(movies, safe=False)
