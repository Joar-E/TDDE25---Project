class Product:
    def __init__(self, title, price):
        self.title = title 
        self.price = price

    def buy(self):
        print()
        print(f'Thank you for buying {self.title} for ${self.price*2}!')
        print('Your product will arrive shortly!')
        print('(We already have all your personal information)')
        # TODO: Query the database we bought from facebook

    def print_description(self):
        print()
        print(f'{self.title} - Now only ${self.price}!!')


class Book(Product):
    def __init__(self, title, price, author):
        super().__init__(title, price)
        self.author = author

    def print_description(self):
        super().print_description()
        print(f'Written by the renowned author {self.author}')


class VideoGame(Product):
    def __init__(self, title, price, developer, platform):
        super().__init__(title, price)
        self.developer = developer
        self.platform = platform

    def print_description(self):
        super().print_description()
        print(f'Developed by {self.developer} for {self.platform}')

class Pc_Game(Videogame):
    def __init__(self, title, price, developer, platform, requirements):
    self.requirements = requirements
    def print_description(self):
        super().print_description()
        print(f'Requires {self.requirements}')


products = [
    Book('Harry Potter 1', 20, 'J.K. Rowling'),
    VideoGame('Call of Duty 42', 200, 'Treyarch', 'PC')
    Pc_Game('ctf, 20, sg1-09, PC, Intel HD Graphics 4')
]
    


#HejHej
