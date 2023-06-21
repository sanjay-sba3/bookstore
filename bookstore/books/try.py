id = int(input('enter id: '))
serializer_books_data = [
    {
        "id": 1,
        "title": "Wings of Fire",
        "author": "Dr. Kalam",
        "publication_date": "2005-05-12",
        "price": "599.99",
        "category": 1,
        "user": [
            6
        ]
    },
    {
        "id": 2,
        "title": "Philippa of Hainault- Mother of the English Nation",
        "author": "Kathryn Warner",
        "publication_date": "2022-01-02",
        "price": "999.00",
        "category": 1,
        "user": [
            6,
            8,
            9
        ]
    },
    {
        "id": 3,
        "title": "Most Dope",
        "author": "Paul Cantor",
        "publication_date": "2022-05-12",
        "price": "799.00",
        "category": 1,
        "user": [
            7,
            8
        ]
    },
    {
        "id": 4,
        "title": "Natural Disaster",
        "author": "Ginger Zee",
        "publication_date": "2022-05-31",
        "price": "526.56",
        "category": 1,
        "user": [
            9
        ]
    },
    {
        "id": 5,
        "title": "Vivian Maier Developed",
        "author": "Ann Marks",
        "publication_date": "2021-06-29",
        "price": "355.60",
        "category": 1,
        "user": [
            8,
            9
        ]
    },
    {
        "id": 6,
        "title": "Dreams from my father",
        "author": "Barack Obama, President of US",
        "publication_date": "1996-01-01",
        "price": "100.52",
        "category": 1,
        "user": [
            9
        ]
    }
]
for i in range (len(serializer_books_data)): 
    if id in serializer_books_data[i]["user"]: 
        # book = Book.objects.filter(id=serializer_rating.data[i]["book"])
        print(i)
        print("hello", serializer_books_data[i]["title"] )
