class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        if not isinstance(place, Place):
            raise ValueError("Place must be a valid Place instance.")
        if not isinstance(user, User):
            raise ValueError("User must be a valid User instance.")
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
