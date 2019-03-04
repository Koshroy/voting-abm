from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector


# Average or extremist views
AVERAGE_VIEW = 0
EXTREMIST_VIEW = 1

# Power user or normal user. Power users read more topics
POWER_USER_TYPE = 2
NORMAL_USER_TYPE = 3


class SchellingAgent(Agent):
    """
    Schelling segregation agent
    """

    def __init__(self, pos, model, agent_type):
        """
         Create a new Schelling agent.

         Args:
            unique_id: Unique identifier for the agent.
            x, y: Agent initial location.
            agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type

    def step(self):
        similar = 0
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.type == self.type:
                similar += 1

        # If unhappy, move:
        if similar < self.model.homophily:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1


class ModelAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init(unique_id, model)

    def step(self):
        pass

    def agent_type(self):
        pass


class PostAgent(Agent):
    def __init__(self, pos, model):
        self.score = 0

    def agent_type():
        return "post"


class HumanAgent(Agent):
    def __init__(self, pos, model, views_type, user_type):
        unique_id = "{}_human_{}_{}_{}".format(pos, views_type, user_type)
        super().__init__(unique_id, model)
        self.pos = pos
        self.agent_type = ""
        self.views_type = views_type
        self.user_type = user_type
        self.post_radius = 1 if self.views_type == EXTREMIST_VIEW else 10
        self.threshold = 0 if self.user_type == POWER_USER_TYPE else 10

    def agent_type(self):
        return "human"

    def threshold(self):
        return 0 if self.user_type == POWER_USER_TYPE else 10

    def step(self):
        for cell in self.model.grid.coord_iter():
            contents = cell[0]

            # If there is an agent in this cell
            if contents != self.model.grid.default_val():
                for agent in contents:
                    if agent.agent_type() == "post":
                        if agent.score >= self.threshold():
                            agent.score -= 1

        for neighbor in self.model.grid.neighbor_iter(self.pos, self.post_radius):
            if neighbor.agent_type() == "post":

                # Consider this post because it's above the threshold
                if neighbor.score >= self.threshold():

                    # We sum by 2 to offset the minus 1 we normally gave
                    neighbor.score += 2


class UpvoteDownvote(Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(
        self,
        height=20,
        width=20,
        post_variety=0.3,
        views_variety=0.3,
        extremist_prob=0.01,
        enthusiast_prob=0.1,
    ):
        """
        """

        self.height = height
        self.width = width
        self.post_variety = post_variety
        self.view_variety = view_variety
        self.extremist_prob = extremist_prob
        self.enthusiast_prob = enthusiast_prob

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(height, width, torus=True)

        self.datacollector = DataCollector(
            {"happy": "happy"},  # Model-level count of happy agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]

            if self.random.random() < post_variety:
                agent = SchellingAgent((x, y), self, agent_type)
                self.grid.place_agent(agent, (x, y))
                self.schedule.add(agent)

            # Check if a person with this view should exist
            if self.random.random() < views_variety:
                views = (
                    EXTREMIST_VIEW
                    if self.random.random() < extremist_prob
                    else AVERAGE_VIEW
                )
                user_type = (
                    POWER_USER_TYPE
                    if self.random.random() < enthusiast_prob
                    else NORMAL_USER_TYPE
                )
                human_agent = HumanAgent((x, y), self, views, user_type)
                self.grid.place_agent(human_agent, (x, y))
                self.schedule.add(agent)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False
