from network.models import *

user1 = User.objects.first()
user2 = User.objects.filter(id=2)[0]
user3 = User.objects.filter(id=3)[0]
user4 = User.objects.filter(id=4)[0]
user5 = User.objects.filter(id=5)[0]

#user1
post1 = Posts(content="This is my first post", poster=user1)
post2 = Posts(content="This is my second post", poster=user1)
post3 = Posts(content="This is my third post", poster=user1)
post4 = Posts(content="This is my fourth post", poster=user1)
post5 = Posts(content="This is my fifth post", poster=user1)
post6 = Posts(content="This is my sixth post", poster=user1)
post7 = Posts(content="This is my seventh post", poster=user1)
post8 = Posts(content="This is my eight post", poster=user1)
post9 = Posts(content="This is my ninth post", poster=user1)
post10 = Posts(content="This is my tenth post", poster=user1)

#user2
post11 = Posts(content="This is my first post", poster=user2)
post12 = Posts(content="This is my second post", poster=user2)
post13 = Posts(content="This is my third post", poster=user2)
post14 = Posts(content="This is my fourth post", poster=user2)
post15 = Posts(content="This is my fifth post", poster=user2)
post16 = Posts(content="This is my sixth post", poster=user2)
post17 = Posts(content="This is my seventh post", poster=user2)
post18 = Posts(content="This is my eight post", poster=user2)
post19 = Posts(content="This is my ninth post", poster=user2)
post20 = Posts(content="This is my tenth post", poster=user2)

#user3
post21 = Posts(content="This is my first post", poster=user3)
post22 = Posts(content="This is my second post", poster=user3)
post23 = Posts(content="This is my third post", poster=user3)
post24 = Posts(content="This is my fourth post", poster=user3)
post25 = Posts(content="This is my fifth post", poster=user3)
post26 = Posts(content="This is my sixth post", poster=user3)
post27 = Posts(content="This is my seventh post", poster=user3)
post28 = Posts(content="This is my eight post", poster=user3)
post29 = Posts(content="This is my ninth post", poster=user3)
post30 = Posts(content="This is my tenth post", poster=user3)


#followings
following1 = Followings(user=user2, user_followed=user3)
following2 = Followings(user=user3, user_followed=user2)
following3 = Followings(user=user2, user_followed=user)


"""class Followings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"id:{self.user} followed id:{self.user_followed}"
"""
