from app import *

@app.cli.command('dbdeploy')
def dbdeploy():
    db.drop_all()
    db.create_all()
    print('Database recreated!')

@app.cli.command('dbcreate')
def dbcreate():
    db.create_all()
    print('Database created!')

@app.cli.command('dbdrop')
def dbdrop():
    db.drop_all()
    print('Database dropped!')

@app.cli.command('dbseed')
def dbseed():
    user1 = User(name= "Bna Aennett",
                 display_email= "BnaAennett@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197364951-4468b500-d855-4436-adad-5f46ccf363f0.png",
                 about= "I love Angular, plants, and going hard on my Theremin!",
                 zipcode= "80014"
                )
    user2 = User(name= "Kaya Mappen",
                 display_email= "KayaMappen@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197364981-2f242f95-a0b1-4bb0-b2e8-be6946e218cc.png",
                 about= "Local rapper trying to make it happen. This grind can't keep me down! Looking to connect with serious musicians only.",
                 zipcode= "80014"
                )
    user3 = User(name= "Tick Neets",
                 display_email= "TickNeets@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197365009-63810454-9815-479c-a0fe-e071f78833ea.png",
                 about= "I love to teach piano! I'd love to start a band. Connect with me please :)",
                 zipcode= "80014"
                )
    user4 = User(name= "Rwendolyn Guiz",
                 display_email= "RwendolynGuiz@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197365030-6b898eda-506d-44bb-8824-7614417c6922.png",
                 about= "Banging drums is my go to stress reliever.",
                 zipcode= "80014"
                )
    user5 = User(name= "Rmma Eussel",
                 display_email= "RmmaEussel@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197365046-9401a054-9a38-4f8b-8097-de7feaeb6b0f.png",
                 about= "Let's jam soon! lol",
                 zipcode= "80014"
                )
    user6 = User(name= "Bichael Monini",
                 display_email= "BichaelMonini@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197365068-74fc732a-eb69-4a45-826c-6ff39a0af77d.png",
                 about= "Music is my life </3",
                 zipcode= "80014"
                )
    user7 = User(name= "Hared Jardinger",
                 display_email= "HaredJardinger@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197365099-0e35cd61-7448-4e62-9005-087404014c99.png",
                 about= "Classically trained baroque pianist who is baroque. :') I need some gigs y'all. ",
                 zipcode= "80201"
                )
    user8 = User(name= "Bory Cethune",
                 display_email= "BoryCethune@gmail.com",
                 picture_url= "https://user-images.githubusercontent.com/98188684/197365266-ac37398a-f168-4768-8476-5e36b9a068aa.png",
                 about= "!!!MOAR COWBELL!!!",
                 zipcode= "80019"
                )

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.add(user6)
    db.session.add(user7)
    db.session.add(user8)

    inst1 = Instrument(name= "Guitar")
    inst2 = Instrument(name= "Piano")
    inst3 = Instrument(name= "Drums")
    inst4 = Instrument(name= "Flute")
    inst5 = Instrument(name= "Clarinet")
    inst6 = Instrument(name= "Bass")
    inst7 = Instrument(name= "Triangle")
    inst8 = Instrument(name= "Cowbell")
    inst9 = Instrument(name= "Theremin")
    inst10 = Instrument(name= "Saxophone")

    db.session.add(inst1)
    db.session.add(inst2)
    db.session.add(inst3)
    db.session.add(inst4)
    db.session.add(inst5)
    db.session.add(inst6)
    db.session.add(inst7)
    db.session.add(inst8)
    db.session.add(inst9)
    db.session.add(inst10)

    needs_inst1 = NeedsInstrument(name= "Guitar")
    needs_inst2 = NeedsInstrument(name= "Piano")
    needs_inst3 = NeedsInstrument(name= "Drums")
    needs_inst4 = NeedsInstrument(name= "Flute")
    needs_inst5 = NeedsInstrument(name= "Clarinet")
    needs_inst6 = NeedsInstrument(name= "Bass")
    needs_inst7 = NeedsInstrument(name= "Triangle")
    needs_inst8 = NeedsInstrument(name= "Cowbell")
    needs_inst9 = NeedsInstrument(name= "Theremin")
    needs_inst10 = NeedsInstrument(name= "Saxophone")

    db.session.add(needs_inst1)
    db.session.add(needs_inst2)
    db.session.add(needs_inst3)
    db.session.add(needs_inst4)
    db.session.add(needs_inst5)
    db.session.add(needs_inst6)
    db.session.add(needs_inst7)
    db.session.add(needs_inst8)
    db.session.add(needs_inst9)
    db.session.add(needs_inst10)

    genre1 = Genre(name= "Pop")
    genre2 = Genre(name= "Rock")
    genre3 = Genre(name= "Blues")
    genre4 = Genre(name= "Electronic")
    genre5 = Genre(name= "Jam")
    genre6 = Genre(name= "Rap")
    genre7 = Genre(name= "Indie")
    genre8 = Genre(name= "Americana")
    genre9 = Genre(name= "Folk")
    genre10 = Genre(name= "Jazz")

    db.session.add(genre1)
    db.session.add(genre2)
    db.session.add(genre3)
    db.session.add(genre4)
    db.session.add(genre5)
    db.session.add(genre6)
    db.session.add(genre7)
    db.session.add(genre8)
    db.session.add(genre9)
    db.session.add(genre10)

    db.session.commit()
    print('Database seeded!')