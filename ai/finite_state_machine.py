class FiniteStateMachine:
    """
    This is a simple Finite State Machine.
    """

    def __init__(self):
        """
        Initialize the Finite State Machine.
        :param world_model: Holds data about the world.
        :param control: Used to control the robot.
        :param perception: Used to know what the robot feels.
        :param communication: Handles communication between robots.
        :return:
        """
        self.iteration = -1
        self.stateStack = []

    def push_state(self, state):
        """
        Places a new state on the top of the stack and
        reset the iteration counter. Accepts both a list
        of states or a single state function.
        :param state: A function that takes five arguments
        (iteration, fsm, world_model, control, perception, communication).
        :return:
        """
        self.iteration = -1

        if isinstance(state, list):
            self.stateStack += state
        else:
            self.stateStack.append(state)

    def pop_state(self):
        """
        Removes a state from the top of the stack and
        reset the iteration counter.
        :return:
        """
        self.iteration = -1

        if self.stateStack:
            self.stateStack.pop()

    def pop_all(self):
        """
        Removes all states.
        :return:
        """
        self.iteration = -1
        self.stateStack = []

    def update(self, frame):
        """
        Increment the iteration counter calls the function
        on the top of the state stack.
        :return:
        """
        self.iteration += 1
        
        if self.stateStack:
            self.stateStack[-1](
                self.iteration,
                self,
                frame
            )
        else:
            print("No state!")