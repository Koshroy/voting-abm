from operator import attrgetter
from random import random, shuffle


ENTHUSIAST_PROB = 0.1
EXTREMIST_PROB = 0.00

EXTREMIST_RADIUS = 0.01
NORMAL_RADIUS = 0.1


class Entity:
    uuid_counter = 0 # is this going to be unique with subclasses?


    @classmethod
    def _get_uuid(cls):
        uuid = cls.uuid_counter
        cls.uuid_counter += 1
        return uuid


class User(Entity):
    def __init__(self, opinion, opinion_radius, enthusiasm, passionate):
        self.uuid = self._get_uuid()
        self.opinion = opinion
        self.opinion_radius = opinion_radius
        self.enthusiasm = enthusiasm
        self.passionate = passionate


    def vote(self, post):
        if abs(post.opinion - self.opinion) <= self.opinion_radius*self.opinion:
            return 1

        return -1 if self.passionate else 0


class Post(Entity):
    def __init__(self, opinion):
        self.uuid = self._get_uuid()
        self.opinion = opinion
        self.score = 0


def update_loop(user, posts):
    sorted_posts = sorted(posts, key=attrgetter('score'), reverse=True)
    post_count = 0
    for post in sorted_posts:
        if post_count > user.enthusiasm:
            break

        post.score += user.vote(post)
        post_count += 1

    return sorted_posts


def run(num_users, num_runs):
    posts = [Post(random()) for i in range(num_users*10)]
    users = []
    
    for i in range(num_users):
        is_enthusiast = random() < ENTHUSIAST_PROB
        enthusiasm = 100 if is_enthusiast else 10
        passionate = random() < EXTREMIST_PROB
        opinion_radius = EXTREMIST_RADIUS if passionate else NORMAL_RADIUS
        users.append(User(
            random(),
            opinion_radius,
            enthusiasm,
            passionate,
        ))

    new_posts = posts
    shuffle(users) # shuffle the users so we "randomly" activate them

    for i in range(num_runs):
        print('Updating: {}', i+1)
        for u in users:
            new_posts = update_loop(u, new_posts)
        
    sorted_new_posts = sorted(new_posts, key=attrgetter('score'), reverse=True)
    for i in range(20):
        print('Post Score: {} | Opinion: {}'.format(sorted_new_posts[i].score, sorted_new_posts[i].opinion))

    print('Extremist Users:')
    for user in [u for u in users if u.passionate]:
        print('User UUID: {} | Opinion: {}'.format(user.uuid, user.opinion))


def main():
    run(3000, 1)


if __name__ == "__main__":
    main()
