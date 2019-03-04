from entity import Vote


class BaseVotingRules:
    def convert(self, feeling):
        if feeling == Vote.LIKE:
            return 1
        elif feeling == Vote.NEUTRAL:
            return 0
        elif feeling == Vote.DISLIKE:
            return -1
        else:
            return 0


class NoDownvoteRules(BaseVotingRules):
    def convert(self, feeling):
        return 1 if feeling == Vote.LIKE else 0
