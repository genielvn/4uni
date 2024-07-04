from main.models import Board, Thread, User, Role, University, Reply

user = Role.objects.create(name="User")
mod = Role.objects.create(name="Moderator")

Board.objects.create(board_id="g", name="General Discussions", description="Discussions that are outside universities").save()
Board.objects.create(board_id="pol", name="Politics", description="Philippine Politcs ba talaga?").save()
Board.objects.create(board_id="ph", name="Philippines", description="Perlas ng Silanganan.").save()
Board.objects.create(board_id="up", name="University of The Philippines", description="Honor, Excellence, Service").save()
Board.objects.create(board_id="pup", name="Polytechnic University of The Philippines", description="Tanglaw ng Bayan").save()
Board.objects.create(board_id="tup", name="Technological University of the Philippines", description="Haligi ng Bayan").save()
Board.objects.create(board_id="pnu", name="Philippine Normal University", description="Truth. Excellence. Service.").save()
Board.objects.create(board_id="ust", name="University of Santo Tomas", description="Veritas in Caritate").save()
Board.objects.create(board_id="ue", name="University of the East", description="Tomorrow Begins in the East").save()
Board.objects.create(board_id="admu", name="Ateneo de Manila University", description="Lux in Domino").save()
Board.objects.create(board_id="dlsu", name="De La Salle College", description="Religio, Mores, Cultura").save()
Board.objects.create(board_id="feu", name="Far Eastern University", description="Love of Fatherland and God").save()

University.objects.create(university_id="up", name="University of The Philippines", verified=True)
uni = University.objects.create(university_id="pup", name="Polytechnic University of The Philippines", verified=True)
uni.save()
University.objects.create(university_id="tup", name="Technological University of the Philippines", verified=True).save()
University.objects.create(university_id="pnu", name="Philippine Normal University", verified=True).save()
University.objects.create(university_id="ust", name="University of Santo Tomas", verified=True).save()
University.objects.create(university_id="ue", name="University of the East", verified=True).save()
University.objects.create(university_id="admu", name="Ateneo de Manila University", verified=True).save()
University.objects.create(university_id="dlsu", name="De La Salle College", verified=True).save()
University.objects.create(university_id="feu", name="Far Eastern University", verified=True).save()

sp = User.objects.create(
    username="SmiliePop",
    role=mod,
    university=uni)

sp.set_password("moderator")
sp.save()

