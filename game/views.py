from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .hand_detector import detect_hand
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Match
import random
from .models import Match
import json
import base64
import cv2
import numpy as np
from .hand_detector import detect_hand





def home(request):
    return render(request, 'game/home.html')


@csrf_exempt
def predict(request):

    if request.method == "POST":

        data = json.loads(request.body)

        image_data = data["image"]

        image_data = image_data.split(",")[1]

        image_bytes = base64.b64decode(image_data)

        np_arr = np.frombuffer(image_bytes, np.uint8)

        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        gesture = detect_hand(img)

        if gesture in ["Rock", "Paper", "Scissors"]:

            ai_move = random.choice([
                "Rock",
                "Paper",
                "Scissors"
            ])

            result = determine_winner(
                gesture,
                ai_move
            )

            if request.user.is_authenticated:

                Match.objects.create(
                    player=request.user,
                    user_move=gesture,
                    ai_move=ai_move,
                    result=result
                )

            return JsonResponse({
                "prediction": gesture,
                "ai_move": ai_move,
                "result": result
            })

        return JsonResponse({
            "prediction": gesture
        })

    return JsonResponse({
        "prediction": "Invalid Request"
    })
@csrf_exempt
def play(request):

    if request.method == "POST":

        data = json.loads(request.body)

        user_move = data["move"]

        ai_move = random.choice([
            "Rock",
            "Paper",
            "Scissors"
        ])

        result = determine_winner(
            user_move,
            ai_move
        )

        if request.user.is_authenticated:

            Match.objects.create(
                player=request.user,
                user_move=user_move,
                ai_move=ai_move,
                result=result
            )

        return JsonResponse({
            "user_move": user_move,
            "ai_move": ai_move,
            "result": result
        })
def determine_winner(user_move, ai_move):

    if user_move == ai_move:
        return "Draw"

    if (
        (user_move == "Rock" and ai_move == "Scissors") or
        (user_move == "Paper" and ai_move == "Rock") or
        (user_move == "Scissors" and ai_move == "Paper")
    ):
        return "Win"

    return "Loss"




@login_required
def history(request):

    matches = Match.objects.filter(
        player=request.user
    ).order_by('-played_at')

    return render(
        request,
        'game/history.html',
        {
            'matches': matches
        }
    )
@login_required
def dashboard(request):

    matches = Match.objects.filter(
        player=request.user
    )

    total = matches.count()

    wins = matches.filter(
        result='Win'
    ).count()

    losses = matches.filter(
        result='Loss'
    ).count()

    draws = matches.filter(
        result='Draw'
    ).count()

    win_rate = 0

    if total > 0:
        win_rate = round(
            (wins / total) * 100,
            2
        )

    context = {
        'total': total,
        'wins': wins,
        'losses': losses,
        'draws': draws,
        'win_rate': win_rate
    }

    return render(
        request,
        'game/dashboard.html',
        context
    )

def leaderboard(request):

    players = User.objects.all()

    leaderboard_data = []

    for player in players:

        wins = Match.objects.filter(
            player=player,
            result='Win'
        ).count()

        leaderboard_data.append({
            'username': player.username,
            'wins': wins
        })

    leaderboard_data = sorted(
        leaderboard_data,
        key=lambda x: x['wins'],
        reverse=True
    )

    return render(
        request,
        'game/leaderboard.html',
        {
            'players': leaderboard_data
        }
    )